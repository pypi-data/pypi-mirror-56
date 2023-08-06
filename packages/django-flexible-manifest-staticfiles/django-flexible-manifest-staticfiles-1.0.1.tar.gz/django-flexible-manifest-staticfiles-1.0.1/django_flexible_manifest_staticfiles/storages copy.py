import os
import posixpath
import re

from collections import OrderedDict
from urllib.parse import unquote, urldefrag, urlsplit, urlunsplit

from django.conf import settings
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from django.contrib.staticfiles.utils import matches_patterns
from django.core.files.base import ContentFile

class FlexibleManifestStaticFilesStorage(ManifestStaticFilesStorage):

    whitelisted_patterns = getattr(settings, "STATICFILES_VERSIONED_INCLUDE", ['.*'])
    blacklisted_patterns = getattr(settings, "STATICFILES_VERSIONED_EXCLUDE", [])

    def _post_process(self, paths, adjustable_paths, hashed_files):

        filtered_paths = OrderedDict()
        filtered_adjustable_paths = []

        # if len(hashed_files) > 0:
        #     print("abort")
        #     return super()._post_process(filtered_paths, filtered_adjustable_paths, hashed_files)

        for name, val in paths.items():
            if any(re.search(wp, name) for wp in self.whitelisted_patterns):
                if not any(re.search(wp, name) for wp in self.blacklisted_patterns):
                    filtered_paths[name] = val

        for name in adjustable_paths:
            if any(re.search(wp, name) for wp in self.whitelisted_patterns):
                if not any(re.search(wp, name) for wp in self.blacklisted_patterns):
                    filtered_adjustable_paths.append(name)
        
        return super()._post_process(filtered_paths, filtered_adjustable_paths, hashed_files)


    def url_converter(self, name, hashed_files, template=None):

        super_converter = super().url_converter(name, hashed_files, template)

        def converter(matchobj):
            """
            Convert the matched URL to a normalized and hashed URL.

            This requires figuring out which files the matched URL resolves
            to and calling the url() method of the storage.
            """
            matched, url = matchobj.groups()

            print("matched")
            print(matched)
            print(url)
            should_convert = False

            if any(re.search(wp, url) for wp in self.whitelisted_patterns):
                if not any(re.search(wp, url) for wp in self.blacklisted_patterns):
                    # return "KEEP AS IS"
                    return matched
                    should_convert = True

            if not should_convert:
                return matched

            return super_converter

        return converter

        # def converter(matchobj):
        #     """
        #     Convert the matched URL to a normalized and hashed URL.

        #     This requires figuring out which files the matched URL resolves
        #     to and calling the url() method of the storage.
        #     """
        #     matched, url = matchobj.groups()

        #     print("matched")
        #     print(matched)
        #     print(url)
        #     should_convert = False

        #     if any(re.search(wp, url) for wp in self.whitelisted_patterns):
        #         if not any(re.search(wp, url) for wp in self.blacklisted_patterns):
        #             # return "KEEP AS IS"
        #             return matched
        #             should_convert = True

        #     if not should_convert:
        #         return matched

        #     # Ignore absolute/protocol-relative and data-uri URLs.
        #     if re.match(r'^[a-z]+:', url):
        #         return matched

        #     # Ignore absolute URLs that don't point to a static file (dynamic
        #     # CSS / JS?). Note that STATIC_URL cannot be empty.
        #     if url.startswith('/') and not url.startswith(settings.STATIC_URL):
        #         return matched

        #     # Strip off the fragment so a path-like fragment won't interfere.
        #     url_path, fragment = urldefrag(url)

        #     if url_path.startswith('/'):
        #         # Otherwise the condition above would have returned prematurely.
        #         assert url_path.startswith(settings.STATIC_URL)
        #         target_name = url_path[len(settings.STATIC_URL):]
        #     else:
        #         # We're using the posixpath module to mix paths and URLs conveniently.
        #         source_name = name if os.sep == '/' else name.replace(os.sep, '/')
        #         target_name = posixpath.join(posixpath.dirname(source_name), url_path)

        #     # Determine the hashed name of the target file with the storage backend.
        #     hashed_url = self._url(
        #         self._stored_name, unquote(target_name),
        #         force=True, hashed_files=hashed_files,
        #     )

        #     transformed_url = '/'.join(url_path.split('/')[:-1] + hashed_url.split('/')[-1:])

        #     # Restore the fragment that was stripped off earlier.
        #     if fragment:
        #         transformed_url += ('?#' if '?#' in url else '#') + fragment

        #     # Return the hashed version to the file
        #     return template % unquote(transformed_url)

        # return converter

    # def url_converter(self, name, hashed_files, template=None):

    #     replace_converter = False

    #     print(name)

    #     if any(re.search(wp, name) for wp in self.whitelisted_patterns):
    #         if not any(re.search(wp, name) for wp in self.blacklisted_patterns):
    #             replace_converter = True
    #             print("WILL REPLACE")

    #     print("")

    #     if replace_converter:
    #         def converter(matchobj):
                
    #             matched, url = matchobj.groups()
    #             print("matched:")
    #             print(matched)

    #             return matched

    #         return converter

    #     return super().url_converter(name, hashed_files, template)
