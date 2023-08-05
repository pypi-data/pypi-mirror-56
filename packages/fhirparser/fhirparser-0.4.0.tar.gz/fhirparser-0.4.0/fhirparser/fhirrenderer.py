#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import re
import shutil
import textwrap
from typing import Optional

from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from jinja2.filters import environmentfilter

from fhirparser.logger import logger


class FHIRRenderer(object):
    """ Superclass for all renderer implementations.
    """
    
    def __init__(self, spec, settings):
        self.spec = spec
        self.settings = settings
        self.clean_settings()
        self.jinjaenv = Environment(loader=FileSystemLoader(self.settings.tpl_base))
        self.jinjaenv.filters['wordwrap'] = do_wordwrap

    @staticmethod
    def rel_to_settings_path(opts, path: Optional[str]) -> Optional[str]:
        """ Return the absolute path of path relative to the settings directory """
        if path is None or os.path.isabs(path):
            return path
        return os.path.abspath(os.path.join(opts.settings_dir, path))

    @staticmethod
    def clean_it(path: str) -> str:
        return ('/' if path and path[0] == '/' else '') + os.path.join(*path.split('/'))

    def clean_settings(self) -> None:
        """ Splits paths at '/' and re-joins them using os.path.join().
        """
        self.settings.tpl_base = self.clean_it(self.settings.tpl_base)
        self.settings.tpl_resource_target = self.clean_it(self.settings.tpl_resource_target)
        self.settings.tpl_factory_target = self.clean_it(self.settings.tpl_factory_target)
        self.settings.tpl_unittest_target = self.clean_it(self.settings.tpl_unittest_target)
    
    def render(self):
        """ The main rendering start point, for subclasses to override.
        """
        raise Exception("Cannot use abstract superclass' `render` method")
    
    def do_render(self, data, template_name, target_path):
        """ Render the given data using a Jinja2 template, writing to the file
        at the target path.
        
        :param template_name: The Jinja2 template to render, located in settings.tpl_base
        :param target_path: Output path
        """
        try:
            template = self.jinjaenv.get_template(os.path.basename(template_name))
        except TemplateNotFound as e:
            logger.error("Template \"{}\" not found in «{}», cannot render"
                .format(template_name, self.settings.tpl_base))
            return
        
        if not target_path:
            raise Exception("No target filepath provided")
        dirpath = os.path.dirname(target_path)
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)
        
        with io.open(target_path, 'w', encoding='utf-8') as handle:
            logger.info('Writing {}'.format(target_path))
            rendered = template.render(data)
            handle.write(rendered)
            # handle.write(rendered.encode('utf-8'))


class FHIRStructureDefinitionRenderer(FHIRRenderer):
    """ Write classes for a profile/structure-definition.
    """    
    def copy_files(self, target_dir):
        """ Copy base resources to the target location, according to settings.
        """
        for origpath, module, contains in self.settings.manual_profiles:
            if not origpath:
                continue
            origpath = self.rel_to_settings_path(self.settings, self.clean_it(origpath))
            if os.path.exists(origpath):
                tgt = os.path.join(target_dir, os.path.basename(origpath))
                logger.info("Copying manual profiles in {} to {}".format(os.path.basename(origpath), tgt))
                os.makedirs(os.path.dirname(tgt), exist_ok=True)
                shutil.copyfile(origpath, tgt)
            else:
                logger.error(f"Manual profile {origpath} does not exits")

    @staticmethod
    def set_forwards(imports, classes) -> None:
        import_names = [i.name for i in imports]
        seen = []
        for c in classes[::-1]:
            for p in c.properties:
                p.is_forward = not p.is_native and p.enum is None and p.class_name not in import_names \
                               and p.class_name not in seen
            seen.append(c.name)
    
    def render(self):
        for profile in self.spec.writable_profiles():
            classes = profile.writable_classes()
            if self.settings.sort_resources:
                classes = sorted(classes, key=lambda x: x.name)
            if 0 == len(classes):
                if profile.url is not None:        # manual profiles have no url and usually write no classes
                    logger.info('Profile "{}" returns zero writable classes, skipping'.format(profile.url))
                continue
            
            imports = profile.needed_external_classes()
            self.set_forwards(imports, classes)
            data = {
                'profile': profile,
                'info': self.spec.info,
                'imports': imports,
                'classes': classes
            }
            
            ptrn = profile.targetname.lower() if self.settings.resource_modules_lowercase else profile.targetname
            source_path = self.settings.tpl_resource_source
            target_name = self.settings.tpl_resource_target_ptrn.format(ptrn)
            target_path = os.path.join(self.settings.tpl_resource_target, target_name)
            self.do_render(data, source_path, target_path)

        self.copy_files(self.settings.tpl_resource_target)


class FHIRFactoryRenderer(FHIRRenderer):
    """ Write factories for FHIR classes.
    """
    def render(self):
        classes = []
        for profile in self.spec.writable_profiles():
            classes.extend(profile.writable_classes())
        
        data = {
            'info': self.spec.info,
            'classes': sorted(classes, key=lambda x: x.name) if self.settings.sort_resources else classes,
        }
        self.do_render(data, self.settings.tpl_factory_source, self.settings.tpl_factory_target)


class FHIRDependencyRenderer(FHIRRenderer):
    """ Puts down dependencies for each of the FHIR resources. Per resource
    class will grab all class/resource names that are needed for its
    properties and add them to the "imports" key. Will also check 
    classes/resources may appear in references and list those in the
    "references" key.
    """
    def render(self):
        data = {'info': self.spec.info}
        resources = []
        for profile in self.spec.writable_profiles():
            resources.append({
                'name': profile.targetname,
                'imports': profile.needed_external_classes(),
                'references': profile.referenced_classes(),
            })
        data['resources'] = sorted(resources, key=lambda x: x['name']) if self.settings.sort_resources else resources
        self.do_render(data, self.settings.tpl_dependencies_source, self.settings.tpl_dependencies_target)


class FHIRValueSetRenderer(FHIRRenderer):
    """ Write ValueSet and CodeSystem contained in the FHIR spec.
    """
    def render(self):
        if not self.settings.tpl_codesystems_source:
            logger.info("Not rendering value sets and code systems since `tpl_codesystems_source` is not set")
            return
        
        systems = [v for k,v in self.spec.codesystems.items()]
        data = {
            'info': self.spec.info,
            'systems': sorted(systems, key=lambda x: x.name) if self.settings.sort_resources else systems,
        }
        target_name = self.settings.tpl_codesystems_target_name
        target_path = os.path.join(self.settings.tpl_resource_target, target_name)
        self.do_render(data, self.settings.tpl_codesystems_source, target_path)


class FHIRUnitTestRenderer(FHIRRenderer):
    """ Write unit tests.
    """
    def render(self):
        if self.spec.unit_tests is None:
            return
        
        # render all unit test collections
        for coll in self.spec.unit_tests:
            data = {
                'info': self.spec.info,
                'class': coll.klass,
                'tests': coll.tests,
            }
            
            file_pattern = coll.klass.name
            if self.settings.resource_modules_lowercase:
                file_pattern = file_pattern.lower()
            file_name = self.settings.tpl_unittest_target_ptrn.format(file_pattern)
            file_path = os.path.join(self.settings.tpl_unittest_target, file_name)
            
            self.do_render(data, self.settings.tpl_unittest_source, file_path)
        
        # copy unit test files, if any
        if self.settings.unittest_copyfiles is not None:
            for origfile in self.settings.unittest_copyfiles:
                utfile = os.path.join(*origfile.split('/'))
                if os.path.exists(utfile):
                    target = os.path.join(self.settings.tpl_unittest_target, os.path.basename(utfile))
                    logger.info('Copying unittest file {} to {}'.format(os.path.basename(utfile), target))
                    shutil.copyfile(utfile, target)
                else:
                    logger.warning("Unit test file \"{}\" configured in `unittest_copyfiles` does not exist"
                        .format(utfile))


# There is a bug in Jinja's wordwrap (inherited from `textwrap`) in that it
# ignores existing linebreaks when applying the wrap:
# https://github.com/mitsuhiko/jinja2/issues/175
# Here's the workaround:
@environmentfilter
def do_wordwrap(environment, s, width=79, break_long_words=True, wrapstring=None):
    """
    Return a copy of the string passed to the filter wrapped after
    ``79`` characters.  You can override this default using the first
    parameter.  If you set the second parameter to `false` Jinja will not
    split words apart if they are longer than `width`.
    """
    if not s:
        return s
    
    if not wrapstring:
        wrapstring = environment.newline_sequence
    
    accumulator = []
    # Workaround: pre-split the string on \r, \r\n and \n
    for component in re.split(r"\r\n|\n|\r", s):
        # textwrap will eat empty strings for breakfirst. Therefore we route them around it.
        if len(component) == 0:
            accumulator.append(component)
            continue
        accumulator.extend(
            textwrap.wrap(component, width=width, expand_tabs=False,
                replace_whitespace=False,
                break_long_words=break_long_words)
        )
    return wrapstring.join(accumulator)

