import os
from argparse import ArgumentParser, ArgumentError
from types import ModuleType
from typing import List, Optional

import sys

from fhirparser import fhirloader
from fhirparser import fhirspec
from fhirparser.logger import logger
from fhirparser.fhirrenderer import FHIRRenderer

_cache = 'downloads'

# Settings attributes that are relative to location of settings file and opts override if exists
relative_settings_paths = [
    ('tpl_base', 'templatedir'),
    ('tpl_resource_target', 'outputdir'),
    ('tpl_resource_source', None),
    ('tpl_codesystems_source', None),
    ('tpl_factory_source', None),
    ('tpl_factory_target', None),
    ('tpl_dependencies_source', None),
    ('tpl_dependencies_target', None),
    ('tpl_unittest_source', None),
    ('tpl_unittest_target', None)
]


def genargs() -> ArgumentParser:
    """
    Create a command line parser

    :return: parser
    """
    parser = ArgumentParser(prog="fhirparser")
    parser.add_argument("settings", help="Location of the settings file. Default is settings.py",
                        default="settings.py")
    parser.add_argument("-f", "--force", help="Force download of the spec", action="store_true")
    parser.add_argument("-c", "--cached", help='Force use of the cached spec (incompatible with "-f")',
                        action="store_true")
    parser.add_argument("-lo", "--loadonly", help="Load the spec but do not parse or write resources",
                        action="store_true")
    parser.add_argument("-po", "--parseonly", help="Load and parse but do not write resources", action="store_true")
    parser.add_argument("-u", "--fhirurl", help="FHIR Specification URL (overrides settings.specifications_url)")
    parser.add_argument("-td", "--templatedir", help="Templates base directory (overrides settings.tpl_base)")
    parser.add_argument("-o", "--outputdir",
                        help = "Directory for generated class models. (overrides settings.tpl_resource_target)")
    parser.add_argument("-cd", "--cachedir", help = f"Cache directory (default: {_cache})", default=_cache)
    parser.add_argument("--nosort", help="If set, do not sort resource properties alphabetically", action="store_true")
    return parser


def adjust_source_target_paths(settings, opts):
    for settings_parm, opts_parm in relative_settings_paths:
        if opts_parm and getattr(opts, opts_parm):
            setattr(settings, settings_parm, getattr(opts, opts_parm))
        else:
            setattr(settings, settings_parm, FHIRRenderer.rel_to_settings_path(opts, getattr(settings, settings_parm)))


def generator(args: List[str]) -> Optional[int]:
    cwd = os.getcwd()
    opts = genargs().parse_args(args)
    if opts.force and opts.cached:
        raise ArgumentError('force and cached options cannot both be true')
    
    # Load the settings
    if os.path.isdir(opts.settings):
        opts.settings = os.path.join(opts.settings, 'settings.py')
    opts.settings_dir = os.path.abspath(os.path.dirname(opts.settings))
    logger.info(f"Loading settings from {opts.settings}")
    with open(opts.settings) as f:
        settings_py = f.read()
    settings = ModuleType('settings')
    exec(settings_py, settings.__dict__)

    settings.settings_dir = opts.settings_dir
    
    # Sort option -- default if not in the settings directory
    if opts.nosort:
        settings.sort_resources = False
    elif getattr(settings, "sort_resources", None) is None:
        settings.sort_resources = True
    if settings.sort_resources:
        logger.info("Sorting resource properties")
    else:
        logger.info("Resource properties are not sorted")
    if opts.fhirurl:
        settings.specification_url = opts.fhirurl

    adjust_source_target_paths(settings, opts)
    logger.info(f"Specification: {settings.specification_url}")
    logger.info(f"Template directory: {os.path.relpath(settings.tpl_base, cwd)}")
    logger.info(f"Output directory: {os.path.relpath(settings.tpl_resource_target, cwd)}")
    if settings.write_unittests:
        logger.info(f"Unit test directory: {os.path.relpath(settings.tpl_unittest_target, cwd)}")
    logger.info(f"Cache directory: {opts.cachedir}")
    loader = fhirloader.FHIRLoader(settings, opts.cachedir, force_download=opts.force, force_cache= opts.cached)
    spec_source = loader.load()
    if not opts.loadonly:
        spec = fhirspec.FHIRSpec(spec_source, settings, loader)
        if not opts.parseonly:
            spec.write()
    return 0


def main() -> int:
    generator(sys.argv[1:])

if '__main__' == __name__:
    sys.exit(main())
