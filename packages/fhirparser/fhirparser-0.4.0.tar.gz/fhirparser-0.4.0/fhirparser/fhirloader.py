#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os.path
from fhirparser.logger import logger


class FHIRLoader(object):
    """ Class to download the files needed for the generator.
    
    The `needs` dictionary contains as key the local file needed and how to
    get it from the specification URL.
    """
    needs = {
        'version.info': 'version.info',
        'profiles-resources.json': 'examples-json.zip',
    }
    
    def __init__(self, settings, cache, force_download: bool, force_cache: bool):
        self.settings = settings
        self.base_url = settings.specification_url
        self.cache = cache
        self.force_download = force_download
        self.force_cache = force_cache
    
    def load(self):
        """ Makes sure all the files needed have been downloaded.
        
        :returns: The path to the directory with all our files.
        """
        if self.force_download: assert not self.force_cache

        # If we're not forcing anything, see whether our cached version matches what is on the server
        version_path = os.path.join(self.cache, 'version.info')
        if not (self.force_download or self.force_cache):
            from fhirparser.fhirspec import FHIRVersionInfo
            cached_version = FHIRVersionInfo(None, self.cache) \
                if not self.force_cache and os.path.exists(version_path) else None
            self.download('version.info')
            server_version = FHIRVersionInfo(None, self.cache)
            if cached_version.version != server_version.version:
                logger.info(f"Server version ({server_version.version}) "
                            f"doesn't match cache ({cached_version.version}) - Reloading cache")
                self.force_download = True

        if os.path.isdir(self.cache) and self.force_download:
            import shutil
            shutil.rmtree(self.cache)

        if not os.path.isdir(self.cache):
            os.mkdir(self.cache)

        # check all files and download if missing
        uses_cache = False
        for local, remote in self.__class__.needs.items():
            path = os.path.join(self.cache, local)
            
            if not os.path.exists(path):
                if self.force_cache:
                    raise Exception('Resource missing from cache: {}'.format(local))
                logger.info('Downloading {}'.format(remote))
                filename = self.download(remote)
                
                # unzip
                if '.zip' == filename[-4:]:
                    logger.info('Extracting {}'.format(filename))
                    self.expand(filename)
            else:
                if local == 'version.info':
                    uses_cache = True
        
        if uses_cache:
            logger.info('Using cached resources, supply "-f" to re-download')
        
        return self.cache
    
    def download(self, filename):
        """ Download the given file located on the server.
        
        :returns: The local file name in our cache directory the file was
            downloaded to
        """
        import requests     # import here as we can bypass its use with a manual download
        
        url = self.base_url+'/'+filename
        path = os.path.join(self.cache, filename)
        
        ret = requests.get(url)
        if not ret.ok:
            raise Exception("Failed to download {}".format(url))
        with io.open(path, 'wb') as handle:
            for chunk in ret.iter_content():
                handle.write(chunk)
        
        return filename
    
    def expand(self, local):
        """ Expand the ZIP file at the given path to the cache directory.
        """
        path = os.path.join(self.cache, local)
        assert os.path.exists(path)
        import zipfile      # import here as we can bypass its use with a manual unzip
        
        with zipfile.ZipFile(path) as z:
            z.extractall(self.cache)

