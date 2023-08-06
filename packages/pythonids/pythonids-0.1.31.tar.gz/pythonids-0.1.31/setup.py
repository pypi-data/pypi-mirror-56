# -*- coding: utf-8 -*-
"""Distribute 'pythonids', a common enumeration library for Python syntax and
implementation releases.

Additional Args:
   build_docx: 
       Creates Sphinx based documentation with embeded javadoc-style
       API documentation by epydoc, html only.

   dist_docx: 
       Creates distribution packages for offline documents.

   install_docx: 
       Install a local copy of the previously build documents in
       accordance to PEP-370. Calls 'create_sphinx.sh' and 'epydoc'.

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

   --help-pythonids: 
       Displays this help.

"""
from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import re

from setuptools import setup, find_packages  # basically forces CPython as prerequisite


# documents
from setupdocx.build_docx import BuildDocX
from setupdocx.dist_docx import DistDocX
from setupdocx.install_docx import InstallDocX

# unittests
from setuptestx.testx import TestX

from rdbg.start import start_remote_debug    # load a slim bootstrap module
start_remote_debug()                         # check whether '--rdbg' option is present, if so accomplish bootstrap

__author__ = 'Arno-Can Uestuensoez'
__author_email__ = 'acue_sf2@sourceforge.net'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2019 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez"
__uuid__ = "7add5ded-c39b-4b6e-8c87-1b3a1c150ee9"

__vers__ = [0, 1, 31,]
__version__ = "%02d.%02d.%03d"%(__vers__[0],__vers__[1],__vers__[2],)
__release__ = "%d.%d.%d" % (__vers__[0], __vers__[1], __vers__[2],) + '-rc0'
__status__ = 'beta'

__sdk = False
"""Set by the option "--sdk". Controls the installation environment."""
if '--sdk' in sys.argv:
    _sdk = True
    sys.argv.remove('--sdk')

# required for various interfaces, thus just do it
_mypath = os.path.dirname(os.path.abspath(__file__))
"""Path of this file."""
sys.path.insert(0,os.path.abspath(_mypath))



#--------------------------------------
#
# Package parameters for setuptools
#
#--------------------------------------

_name='pythonids'
"""package name"""

__pkgname__ = "pythonids"
"""package name"""

_version = "%d.%d.%d"%(__vers__[0],__vers__[1],__vers__[2],)
"""assembled version string"""

_author = __author__
"""author of the package"""

_author_email = __author_email__
"""author's email """

_license = __license__
"""license"""

_packages = find_packages(include=['pythonids', ])
"""Python packages to be installed."""

_packages_sdk = find_packages(include=['pythonids'] )
"""Python packages to be installed."""

_scripts = [
]
"""Scripts to be installed."""

_package_data = {
    'pythonids': [
        'README.md','ArtisticLicense20.html', 'licenses-amendments.txt',
    ],
}
"""Provided data of the package."""

_url='https://sourceforge.net/projects/pythonids/'
"""URL of this package"""

#_download_url="https://github.com/ArnoCan/pythonids/"
_download_url="https://sourceforge.net/projects/pythonids/files/"

_install_requires = []
"""prerequired non-standard packages"""

_keywords  = ' platforms Python OS identifier '
_keywords += ' CPython IPython IronPython Jython PyPy '
_keywords += ' Python2 Python3 '
_keywords += ' bitmask hexvalue '
_keywords += ' Linux Unix Windows OS-X MacOS BSD '
_keywords += ' FreeBSD OpenBSD NetBSD DragonFlyBSD '
_keywords += ' SnowLeopard Darwin'
_keywords += ' Solaris SunOS SunOS5 Aix HP-UX '
_keywords += ' CentOS RHEL Fedora Debian Ubuntu SuSE OpenSUSE SLES '
_keywords += ' ArchLinux BlackArchLinux BlackArch Arch '
_keywords += ' AlpineLinux Alpine '
_keywords += ' ScientificLinux Scientific '
_keywords += ' Armbian Raspbian '
_keywords += ' Gentoo '
_keywords += ' OpenWRT Kali KaliLinux '
_keywords += ' Minix Minx3 '
_keywords += ' Cygwin '
_keywords += ' Windows10 Windows7 WindowsXP '
_keywords += ' Windows2003 Windows2008 Windows2010 Windows2012 Windows2016 Windows2019 '
_keywords += ' ReactOS '
_keywords += ' WSL  '

_description=(
    "The 'pythonids' package provides the identification and enumeration of Python syntax and implementation."
)

_README = os.path.join(os.path.dirname(__file__), 'README.md')
_long_description = open(_README).read() + 'nn'
"""detailed description of this package"""

_classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Environment :: MacOS X",
    "Environment :: Other Environment",
    "Environment :: Win32 (MS Windows)",
    "Environment :: X11 Applications",
    "Framework :: IPython",
    "Intended Audience :: Developers",
    "Intended Audience :: System Administrators",
    "License :: Free To Use But Restricted",
    "License :: OSI Approved :: Artistic License",
    "Natural Language :: English",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: Other OS",
    "Operating System :: POSIX :: BSD :: FreeBSD",
    "Operating System :: POSIX :: BSD :: OpenBSD",
    "Operating System :: POSIX :: Linux",
    "Operating System :: POSIX :: Other",
    "Operating System :: POSIX :: SunOS/Solaris",
    "Operating System :: POSIX",
    "Operating System :: Unix",
    "Programming Language :: C",
    "Programming Language :: C++",
    "Programming Language :: Cython",
    "Programming Language :: Java",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: IronPython",
    "Programming Language :: Python :: Implementation :: Jython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Programming Language :: Python",
    "Programming Language :: Unix Shell",
    "Topic :: Home Automation",
    "Topic :: Internet",
    "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
    "Topic :: Scientific/Engineering",
    "Topic :: Security",
    "Topic :: Software Development :: Build Tools",
    "Topic :: Software Development :: Code Generators",
    "Topic :: Software Development :: Compilers",
    "Topic :: Software Development :: Debuggers",
    "Topic :: Software Development :: Embedded Systems",
    "Topic :: Software Development :: Interpreters",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: Software Development :: Libraries :: Java Libraries",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Software Development :: Libraries :: pygame",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Pre-processors",
    "Topic :: Software Development :: Testing",
    "Topic :: Software Development",
    "Topic :: System :: Distributed Computing",
    "Topic :: System :: Installation/Setup",
    "Topic :: System :: Logging",
    "Topic :: System :: Monitoring",
    "Topic :: System :: Networking",
    "Topic :: System :: Operating System",
    "Topic :: System :: Shells",
    "Topic :: System :: Software Distribution",
    "Topic :: System :: System Shells",
    "Topic :: System :: Systems Administration",
    "Topic :: Utilities",
]
"""the classification of this package"""

_epydoc_api_patchlist = [
    'shortcuts.html',
    'config.html',
    'os_categorization.html',
]
"""Patch list of Sphinx documents for the insertion of links to API documentation."""

_profiling_components = _mypath+os.sep+'bin'+os.sep+'*.py '+_mypath+os.sep+__pkgname__+os.sep+'*.py'
"""Components to be used for the creation of profiling information for Epydoc."""

_doc_subpath='en'+os.path.sep+'html'+os.path.sep+'man7'
"""Relative path under the documents directory."""


_install_requires=[
    'setuplib >= 0.1.0',
    ]

if __sdk: # pragma: no cover
    _install_requires.extend(
        [
            'sphinx >= 1.4',
            'epydoc >= 3.0',
        ]
    )

_test_suite="tests.CallCase"



# Intentional HACK: ignore (online) dependencies, mainly foreseen for developement
__no_install_requires = False
if '--no-install-requires' in sys.argv:
    __no_install_requires = True
    sys.argv.remove('--no-install-requires')

# Intentional HACK: offline only, mainly foreseen for developement
__offline = False
if '--offline' in sys.argv:
    __offline = True
    __no_install_requires = True
    sys.argv.remove('--offline')


if __no_install_requires:
    print("#")
    print("# Changed to offline mode, ignore install dependencies completely.")
    print("# Requires appropriate PYTHONPATH.")
    print("# Ignored dependencies are:")
    print("#")
    for ir in _install_requires:
        print("#   "+str(ir))
    print("#")
    _install_requires=[]


class build_docx(BuildDocX):
    def __init__(self, *args, **kargs):
        self.name = 'pythonids'
        self.copyright = __copyright__
        self.status = __status__
        self.release = __release__
        BuildDocX.__init__(self, *args, **kargs)

    def join_sphinx_mod_sphinx(self, dirpath):
        """Integrates links for *epydoc* into the the sidebar of the default style,
        and adds links to *sphinx* into the output of *epydoc*.

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

        pt = '<h4>Next topic</h4>'
        rp  = r'<h4>API</h4><p class="topless"><a href="epydoc/index.html" title="API">Programming Interface</a></p>'
        rp += pt
        fn = dirpath + '/index.html'
        sed(fn, pt, rp, re.MULTILINE)  # @UndefinedVariable

        pt = '<h4>Previous topic</h4>'
        rp  = r'<h4>API</h4><p class="topless"><a href="epydoc/index.html" title="API">Programming Interface</a></p>'
        rp += pt

        patchlist_sphinx = [
            'shortcuts.html',
            'package_init.html',
            'pythonids.html',
            'pythonids.pythondist.html',
        ]
        for px in patchlist_sphinx:
            fn = dirpath + os.sep+px
            sed(fn, pt, rp, re.MULTILINE)  # @UndefinedVariable
    
        
class dist_docx(DistDocX):
    def __init__(self, *args, **kargs):
        self.name = 'pythonids'
        self.copyright = __copyright__
        self.status = __status__
        self.release = __release__
        DistDocX.__init__(self, *args, **kargs)


class install_docx(InstallDocX):
    def __init__(self, *args, **kargs):
        self.name = 'pythonids'
        self.copyright = __copyright__
        self.status = __status__
        self.release = __release__
        InstallDocX.__init__(self, *args, **kargs)


class testx(TestX):
    def __init__(self, *args, **kargs):
        self.name = 'pythonids'
        self.copyright = __copyright__
        self.status = __status__
        self.release = __release__
        TestX.__init__(self, *args, **kargs)

setup(
    author=_author,
    author_email=_author_email,
    classifiers=_classifiers,
    description=_description,
    download_url=_download_url,
    install_requires=_install_requires,
    keywords=_keywords,
    license=_license,
    long_description=_long_description,
    name=_name,
    package_data=_package_data,
    packages=_packages,
    scripts=_scripts,
    url=_url,
    version=_version,
    zip_safe=False,
    cmdclass={
        'build_docx': build_docx,
        'dist_docx': dist_docx,
        'install_docx': install_docx,
        'testx': testx,
    },
)


if '--help' in sys.argv:
    print()
    print("Help on usage extensions by "+str(_name))
    print("   --help-"+str(_name))
    print()

