# -*- coding: utf-8 -*-
"""Distribute 'setuplib', the missing commands for *setup.py*.

Use this file itself as an example.

Additional Args:
    setuplib: 
        Provide information on available commands.

   testx: 
       Runs PyUnit tests by discovery of 'tests'.

Additional Options:
   --sdk:
       Requires sphinx, epydoc, and dot-graphics.

   --no-install-requires: 
       Suppresses installation dependency checks,
       requires appropriate PYTHONPATH.

   --offline: 
       Sets online dependencies to offline, or ignores online
       dependencies.

"""
from __future__ import absolute_import
from __future__ import print_function

try:
    #
    # optional remote debug only
    #
    from rdbg import start        # load a slim bootstrap module
    start.start_remote_debug()    # check whether '--rdbg' option is present, if so accomplish bootstrap
except:
    pass


import os
import sys
import re

import setuptools

#
# setup extension modules
#

import yapyutils.files.utilities

# setup library functions
# import setuplib.setuplib
from setuplib.setuplib import SetupLibX
#
# setup extension modules
#
import setupdocx

# documents
from setupdocx.build_docx import BuildDocX
from setupdocx.dist_docx import DistDocX
from setupdocx.install_docx import InstallDocX
from setupdocx.build_apiref import BuildApirefX
from setupdocx.build_apidoc import BuildApidocX

# unittests
from setuptestx.testx import TestX

# unittests
import setuptestx.testx


__author__ = 'Arno-Can Uestuensoez'
__author_email__ = 'acue_sf2@sourceforge.net'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2019 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez"
__uuid__ = "1ba7bffb-c00b-4691-a3e9-e392f968e437"

__vers__ = [0, 1, 2, ]
__version__ = "%02d.%02d.%03d" % (__vers__[0], __vers__[1], __vers__[2],)
__release__ = "%d.%d.%d" % (__vers__[0], __vers__[1], __vers__[2],) + '-rc0'
__status__ = 'beta'


__sdk = False
"""Set by the option "--sdk". Controls the installation environment."""
if '--sdk' in sys.argv:
    __sdk = True
    sys.argv.remove('--sdk')


# required for various interfaces, thus just do it
_mypath = os.path.dirname(os.path.abspath(__file__))
"""Path of this file."""
sys.path.insert(0, os.path.abspath(_mypath))


#--------------------------------------
#
# Package parameters for setuptools
#
#--------------------------------------

_name = 'setuplib'
"""package name"""

__pkgname__ = _name
"""package name"""

_version = "%d.%d.%d" % (__vers__[0], __vers__[1], __vers__[2],)
"""assembled version string"""

_author = __author__
"""author of the package"""

_author_email = __author_email__
"""author's email """

_license = __license__
"""license"""

#_packages = setuptools.find_packages(include=['setuplib', 'setuplib.*', 'setup'])
_packages = setuptools.find_packages('setuplib')
"""Python packages to be installed."""
#_packages_sdk = setuptools.find_packages(include=['setuplib'])
_packages_sdk = _packages

_scripts = [
]
"""Scripts to be installed."""

_package_data = {
    'setuplib': [
        'README.md', 'ArtisticLicense20.html', 'licenses-amendments.txt',
    ],
}
"""Provided data of the package."""

_url = 'https://sourceforge.net/projects/setuplib/'
"""URL of this package"""

# _download_url="https://github.com/ArnoCan/setuplib/"
_download_url = "https://sourceforge.net/projects/setuplib/files/"


_install_requires = [
    'pythonids >= 1.0',
    'yapyutils >= 1.0',
    'sourceinfo >= 1.0',
]
"""prerequired non-standard packages"""


_description = (
    "Support core library and management functions for the family of 'setuplib' - extensions "
    "for setuptools / distutils."
)

_README = os.path.join(os.path.dirname(__file__), 'README.md')
_long_description = open(_README).read()
"""detailed description of this package"""


_epydoc_api_patchlist = [
    'shortcuts.html',
    'config.html',
    'os_categorization.html',
]
"""Patch list of Sphinx documents for the insertion of links to API documentation."""

_profiling_components = _mypath + os.sep + 'bin' + os.sep + '*.py ' + _mypath + os.sep + __pkgname__ + os.sep + '*.py'
"""Components to be used for the creation of profiling information for Epydoc."""

_doc_subpath = 'en' + os.path.sep + 'html' + os.path.sep + 'man7'
"""Relative path under the documents directory."""

if __sdk:  # pragma: no cover
    try:
        import sphinx_rtd_theme  # @UnusedImport
    except:
        sys.stderr.write("WARNING: Cannot import package 'sphinx_rtd_theme', cannot create local 'ReadTheDocs' style.")

    _install_requires.extend(
        [
            'pythonids',
            'sphinx >= 1.4',
            'epydoc >= 3.0',
        ]
    )

    _packages = _packages_sdk

_test_suite = "tests.CallCase"

__no_install_requires = False
if '--no-install-requires' in sys.argv:
    __no_install_requires = True
    sys.argv.remove('--no-install-requires')

__offline = False
if '--offline' in sys.argv:
    __offline = True
    __no_install_requires = True
    sys.argv.remove('--offline')

# # Help on addons.
# if '--help-setuplib' in sys.argv:
#     setuplib.usage('setup')
#     sys.exit(0)

if __no_install_requires:
    print("#")
    print("# Changed to offline mode, ignore install dependencies completely.")
    print("# Requires appropriate PYTHONPATH.")
    print("# Ignored dependencies are:")
    print("#")
    for ir in _install_requires:
        print("#   " + str(ir))
    print("#")
    _install_requires = []


class setuplibx(SetupLibX):
    """Defines the package name.
    """

    def __init__(self, *args, **kargs):
        self.name = _name
        self.copyright = __copyright__
        self.status = __status__
        self.release = __release__
        SetupLibX.__init__(self, *args, **kargs)

class build_docx(BuildDocX):
    """Defines additional text processing.
    """
    
    def __init__(self, *args, **kargs):
        self.name = _name
        self.copyright = __copyright__
        self.status = __status__
        self.release = __release__
        BuildDocX.__init__(self, *args, **kargs)

    def join_sphinx_mod_sphinx(self, dirpath):
        """Integrates links for *epydoc* into the the sidebar of the default style,
        and adds links to *sphinx* into the output of *epydoc*. This method needs to 
        be adapted to the actual used theme and templates by the application. Thus
        no generic method is supported, but a call interface. The call is activated
        when the option *--apiref* is set.  

        Adds the following entries before the "Table of Contents" to 
        the *sphinx* document:

        * API
          Before "Previous topic", "Next topic"

        .. note::

           This method is subject to be changed.
           Current version is hardcoded, see documents.
           Following releases will add customization.
        
        Args:
            **dirpath**:
                Directory path to the file 'index.html'.
        
        Returns;
            None

        Raises:
            None
                
        """
    
        if self.verbose > 0:
            print('\nStart post-create document patches\n')
        
        pt = re.compile(r'(<span class="codelink"><a href=".*?' + str(self.name) + '[^#]*?[#][^"]+">source[&]nbsp;code</a></span>)')

        def rpfunc(match):
            rp  = r'[<span class="codelink"><a href="../api.html#" target="_top">api</a></span>]&nbsp;'
            rp += match.group(1)
            return rp
        
        for flst in os.walk(dirpath + '/epydoc/'):
            for fn in flst[2]:
                if fn[-5:] == '.html':
                    if self.verbose > 0:
                        print("process: " + str(fn))
                    yapyutils.files.utilities.sed(flst[0]+os.path.sep+fn, pt, rpfunc)


class install_docx(InstallDocX):
    """Defines the package name.
    """

    def __init__(self, *args, **kargs):
        self.name = _name
        self.copyright = __copyright__
        self.status = __status__
        self.release = __release__
        InstallDocX.__init__(self, *args, **kargs)


class dist_docx(DistDocX):
    """Defines the package name.
    """

    def __init__(self, *args, **kargs):
        self.name = _name
        self.copyright = __copyright__
        self.status = __status__
        self.release = __release__
        DistDocX.__init__(self, *args, **kargs)


class build_apidoc(BuildApidocX):
    """Defines the package name.
    """

    def __init__(self, *args, **kargs):
        self.name = _name
        self.copyright = __copyright__
        self.status = __status__
        self.release = __release__
        BuildApidocX.__init__(self, *args, **kargs)


class build_apiref(BuildApirefX):
    """Defines the package name.
    """

    def __init__(self, *args, **kargs):
        self.name = _name
        self.copyright = __copyright__
        self.status = __status__
        self.release = __release__
        BuildApirefX.__init__(self, *args, **kargs)


class testx(setuptestx.testx.TestX):
    """Defines the package name.
    """

    def __init__(self, *args, **kargs):
        self.name = _name
        self.copyright = __copyright__
        self.status = __status__
        self.release = __release__
        setuptestx.testx.TestX.__init__(self, *args, **kargs)


#
# see setup.py for remaining parameters
#
setuptools.setup(
    author=_author,
    author_email=_author_email,
    cmdclass={
        'build_apidoc': build_apidoc,
        'build_apiref': build_apiref,
        'build_docx': build_docx,
        'dist_docx': dist_docx,
        'install_docx': install_docx,
        'setuplib': setuplibx,
        'testx': testx,
    },
    description=_description,
#    distclass=setuplib.dist.Distribution,  # extends the standard help-display of setuptools
    download_url=_download_url,
    install_requires=_install_requires,
    license=_license,
    long_description=_long_description,
    name=_name,
    package_data=_package_data,
    packages=_packages,
    scripts=_scripts,
    url=_url,
    version=_version,
    zip_safe=False,
)

#
# REMINDER: the own help of setuplib is a common global option 
#
# if '--help' in sys.argv:
#     print()
#     print("Help on provided package extensions by " + str(_name))
#     print("   --help-" + str(_name))
#     print()

sys.exit(0)


