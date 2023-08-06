# -*- coding: utf-8 -*-
"""*pythonids.pythondist* provides information about the Python implementation.

Raises 'pythonids.PythonIDsImplementationError' when implementation is not supported.
"""
#############################################
#
# See manuals for the detailed API.
#
#############################################

import sys
try:
    import platform
    import re

except:
    #
    # missing *platform* and/or *re* requires various special code-sections
    # possible supported are currently MicroPython and CircuitPython
    # see 'pythonids.implementation'
    #

    from pythonids import PythonIDsImplementationError
    try:
        raise PythonIDsImplementationError("use implementation module for: " + str(sys.implementation))  # @UndefinedVariable
    except:
        raise PythonIDsImplementationError("implementation is not supported")

from collections import namedtuple

from pythonids import PythonIDsError, ISSTR, decode_pysyntax_str_to_num


__author__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2010-2018 Arno-Can Uestuensoez" \
                " @Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.1.31'
__uuid__ = "5624dc41-775a-4d17-ac42-14a0d5c41d1a"

__docformat__ = "restructuredtext en"


#
# separation masks 
#
# the combined vector semantics is separative
# thus no hierarchical semantics
#

# category type bits - for structural integrity
PYE_CATEGORY = 0x80000000  # bit 31 only - constant 1 for Python

# syntax type bits
PYE_SYNTAXTYPE = 0x7f800000  # major + minor
PYE_SYNTAXTYPE_MAJOR = 0x70000000  # major
PYE_SYNTAXTYPE_MINOR = 0x0f800000  # minor

# distribution type bits
PYE_DIST = 0x007c0000  # dist enum

# distribution release version bits
PYE_DISTREL = 0x0003ffff  # major + minor + micro
PYE_DISTREL_MAJOR = 0x0003f000  # major
PYE_DISTREL_MINOR = 0x00000fc0  # minor
PYE_DISTREL_MICRO = 0x0000003f  # micro


#
# category: constant PYE_PYTHOPN
#
# : CPython is basically the reference implementation of the Python Foundation @python.org 
#
PYE_PYTHON = 0x80000000  # this value is ignored
PYE_PYTHON_PRETTY = 'Python'
PYE_PYTHON_NAME = 'python'

#
# disttype - the predefined values cover the major and minor version only
# see manual: pythonids/python_categorization.html#bit-mask-layout
#
PYE_PYTHON27 = 0x23800000  # Python2.7
PYE_PYTHON35 = 0x32800000  # Python3.5
PYE_PYTHON36 = 0x33000000  # Python3.6
PYE_PYTHON37 = 0x33800000  # Python3.7
PYE_PYTHON38 = 0x34000000  # Python3.8
PYE_PYTHON39 = 0x34800000  # Python3.9

#
# dist - the distribution may define it's own variant of the core reference syntax including another set of stdlibs
#

# : CPython is basically the reference implementation of the Python Foundation @python.org 
PYE_CPYTHON = 0x00040000  # nr: 1
PYE_CPYTHON_PRETTY = 'CPython'
PYE_CPYTHON_NAME = 'cpython'

# : The variant of MicroPython for tiney devices and IoT by Adafruit inc.
PYE_CIRCUITPYTHON = 0x00080000  # nr: 2
PYE_CIRCUITPYTHON_PRETTY = 'CircuitPython'
PYE_CIRCUITPYTHON_NAME = 'circuitpython'

# : Python with extensions compilation into C-like results 
PYE_CYTHON = 0x000c0000  # nr: 3
PYE_CYTHON_PRETTY = 'Cython'
PYE_CYTHON_NAME = 'cython'

# : Pynteractive Python with a smart command line interface too - beneath it's GUI capabilities.
PYE_IPYTHON = 0x00100000  # nr: 4
PYE_IPYTHON_PRETTY = 'iPython'
PYE_IPYTHON_NAME = 'ipython'

# : The Python variant specialized on .NET and mono runtime platforms - so basically targeting Windows environments
PYE_IRONPYTHON = 0x00140000  # nr: 5
PYE_IRONPYTHON_PRETTY = 'IronPython'
PYE_IRONPYTHON_NAME = 'ironpython'

# : Java JVM and JIT based Python
PYE_JYTHON = 0x00180000  # nr: 6
PYE_JYTHON_PRETTY = 'Jython'
PYE_JYTHON_NAME = 'jython'

# : The crowd funded variant of Python with a schedular, basically replacing a shell and OS by pure and only Python with optional C-plugins 
PYE_MICROPYTHON = 0x001c0000  # nr: 7
PYE_MICROPYTHON_PRETTY = 'MicroPython'
PYE_MICROPYTHON_NAME = 'micropython'

PYE_PYPY = 0x00200000  # nr: 8
PYE_PYPY_PRETTY = 'PyPy'
PYE_PYPY_NAME = 'pypy'

#
# Some reference values of 32bit hexrelease for test and validation.
# E.g. valid as:
#
#   pythonids.pydist.PythonDist.hexrelease
#
PYE_PYDIST_CPYTHON2715 = 0xa38421cf  #: CPython-2.7.15   - Python2.7
PYE_PYDIST_CPYTHON372 = 0xb38431c2  #: CPython-3.7.2    - Python3.7
PYE_PYDIST_IPYTHON550 = 0xA3905140  #: IPython-5.5.0    - Python2.7
PYE_PYDIST_IPYTHON560 = 0xA3905180  # IPython-5.6.0    - Python2.7
PYE_PYDIST_IRONPYTHON277 = 0xA39421C7  #: IRonPython-2.7.7 - Python2.7
PYE_PYDIST_IRONPYTHON279 = 0xA39421C9  #: IRonPython-2.7.9 - Python2.7
PYE_PYDIST_JYTHON270 = 0xA39821C0  #: Jython-2.7.0     - Python2.7
PYE_PYDIST_JYTHON271 = 0xA39821C1  #: Jython-2.7.1     - Python2.7
PYE_PYDIST_PYPY580 = 0xA3A05200  #: PyPy-5.8.0       - Python2.7
PYE_PYDIST_PYPY60027 = 0xA3A06000  #: PyPy-6.0.0       - Python2.7
PYE_PYDIST_PYPY60035 = 0xB2A06000  #: PyPy-6.0.0       - Python3.5
PYE_PYDIST_PYPY70036 = 0xB3207000  #: PyPy-7.0.0       - Python3.6

dist2num = {
    PYE_CIRCUITPYTHON: PYE_CIRCUITPYTHON,
    PYE_CIRCUITPYTHON_NAME: PYE_CIRCUITPYTHON,
    PYE_CIRCUITPYTHON_PRETTY: PYE_CIRCUITPYTHON,
    PYE_CPYTHON: PYE_CPYTHON,
    PYE_CPYTHON_NAME: PYE_CPYTHON,
    PYE_CPYTHON_PRETTY: PYE_CPYTHON,
    PYE_CYTHON: PYE_CYTHON,
    PYE_CYTHON_NAME: PYE_CYTHON,
    PYE_CYTHON_PRETTY: PYE_CYTHON,
    PYE_IPYTHON: PYE_IPYTHON,
    PYE_IPYTHON_NAME: PYE_IPYTHON,
    PYE_IPYTHON_PRETTY: PYE_IPYTHON,
    PYE_IRONPYTHON: PYE_IRONPYTHON,
    PYE_IRONPYTHON_NAME: PYE_IRONPYTHON,
    PYE_IRONPYTHON_PRETTY: PYE_IRONPYTHON,
    PYE_JYTHON: PYE_JYTHON,
    PYE_JYTHON_NAME: PYE_JYTHON,
    PYE_JYTHON_PRETTY: PYE_JYTHON,
    PYE_MICROPYTHON: PYE_MICROPYTHON,
    PYE_MICROPYTHON_NAME: PYE_MICROPYTHON,
    PYE_MICROPYTHON_PRETTY: PYE_MICROPYTHON,
    PYE_PYPY: PYE_PYPY,
    PYE_PYPY_NAME: PYE_PYPY,
    PYE_PYPY_PRETTY: PYE_PYPY,
    PYE_PYTHON: PYE_PYTHON,
    PYE_PYTHON_PRETTY: PYE_PYTHON,
    PYE_PYTHON_NAME: PYE_PYTHON,
    PYE_PYTHON27: PYE_PYTHON27,
    PYE_PYTHON35: PYE_PYTHON35,
    PYE_PYTHON36: PYE_PYTHON36,
    PYE_PYTHON37: PYE_PYTHON37,
    PYE_PYTHON38: PYE_PYTHON38,
    PYE_PYTHON39: PYE_PYTHON39,
}

num2name = {
    PYE_CPYTHON: PYE_CPYTHON_NAME,
    PYE_IPYTHON: PYE_IPYTHON_NAME,
    PYE_IRONPYTHON: PYE_IRONPYTHON_NAME,
    PYE_JYTHON: PYE_JYTHON_NAME,
    PYE_PYPY: PYE_PYPY_NAME,
    PYE_PYTHON: PYE_PYTHON_NAME,
    PYE_PYTHON27: "python2.7",
    PYE_PYTHON35: "python3.5",
    PYE_PYTHON36: "python3.6",
    PYE_PYTHON37: "python3.7",
    PYE_PYTHON38: "python3.8",
    PYE_PYTHON39: "python3.9",
}

num2pretty = {
    PYE_CPYTHON: PYE_CPYTHON_PRETTY,
    PYE_IPYTHON: PYE_IPYTHON_PRETTY,
    PYE_IRONPYTHON: PYE_IRONPYTHON_PRETTY,
    PYE_JYTHON: PYE_JYTHON_PRETTY,
    PYE_PYPY: PYE_PYPY_PRETTY,
    PYE_PYTHON: PYE_PYTHON_PRETTY,
    PYE_PYTHON27: "Python-2.7",
    PYE_PYTHON35: "Python-3.5",
    PYE_PYTHON36: "Python-3.6",
    PYE_PYTHON37: "Python-3.7",
    PYE_PYTHON38: "Python-3.8",
    PYE_PYTHON39: "Python-3.9",
}

#
# static parsers
#
SPLITVERS = re.compile(r'(?s)(^[0-9]+)[.]([0-9]*)[.]([0-9]*).*')
SPLITVERS2 = re.compile(r'(?s)(^[0-9]+)[.]([0-9]*).*')
STR2DISTREL = re.compile(r'([0-9.]*)[^0-9]*')

# : The corresponding *bash* environment names.
bash_map = {
    'category': "PYDIST_CATEGORY",
    'disttype': "PYDIST_DISTTYPE",
    'dist': "PYDIST_DIST",
    'distrel': "PYDIST_DISTREL",
    'hexrelease': "PYDIST_DISTREL_HEXVERSION",
    'compiler': "PYDIST_COMPILER",
    'compiler_version': "PYDIST_COMPILER_VERSION",
    'c_libc_version': "PYDIST_C_LIBC_VERSION",
    'c_compiler': "PYDIST_C_COMPILER",
    'c_compiler_version': "PYDIST_C_COMPILER_VERSION",
}

# : The mapping of attributes to values.
attribute_map = {
    'category': "category",
    'disttype': "disttype",
    'dist': "dist",
    'distrel': "distrel",
    'hexrelease': "hexrelease",
    'compiler': "compiler",
    'compiler_version': "compiler_version",
    'c_libc_version': "c_libc_version",
    'c_compiler': "c_compiler",
    'c_compiler_version': "c_compiler_version",
}


#: Named tuple for structured results. See *collections.namedtuple*.
PyDist = namedtuple('PyDist', ('category', 'disttype', 'dist', 'distrel')) 

#: Named tuple for structured results as sub-parts. See *collections.namedtuple*.
PyDistSegments = namedtuple('PyDistSegments', ('category', 'disttype', 'dist', 'distrel')) 

#: Named tuple for structured results as *str*. See *collections.namedtuple*.
PyDistStr = namedtuple('PyDistStr', ('category', 'disttype', 'dist', 'distrel')) 

class PythonDistError(PythonIDsError):
    pass


def _encode_distrel_bitmask(dx=0, dy=0, dz=0):
    return (
          (dx & 63) << 12  # bit 17 - 12 - see version_info[0]
        | (dy & 63) << 6  # bit 11 -  6 - see version_info[1]
        | (dz & 63)  # bit  5 -  0 - see version_info[2] 
       )


def _encode_distrel_str_bitmask(sxyz=''):
    res = STR2DISTREL.sub(r'\1', sxyz).split('.')  # variable length
    if len(res) == 3:
        return (
              (int(res[0]) & 63) << 12  # bit 17 - 12 - see version_info[0]
            | (int(res[1]) & 63) << 6  # bit 11 -  6 - see version_info[1]
            | (int(res[2]) & 63)  # bit  5 -  0 - see version_info[2] 
           )
    elif len(res) == 2:
        return (
              (int(res[0]) & 63) << 12  # bit 17 - 12 - see version_info[0]
            | (int(res[1]) & 63) << 6  # bit 11 -  6 - see version_info[1]
           )
    elif len(res) == 1:
        return (
              (int(res[0]) & 63) << 12  # bit 17 - 12 - see version_info[0]
           )
    return ()


def _encode_disttype_bitmask(sma=0, smi=0):
    return (
          (sma & 7) << 28  # bit 30 - 28 - see version_info[0]
        | (smi & 31) << 23  # bit 27 - 23 - see version_info[1]
       )


def _encode_disttype_str_bitmask(sxy=''):
    res = STR2DISTREL.sub(r'\1', sxy).split('.')  # variable length
    if len(res) >= 2:
        return (
              (int(res[0]) & 7) << 28  # bit 17 - 12 - see version_info[0]
            | (int(res[1]) & 31) << 23  # bit 11 -  6 - see version_info[1]
           )
    elif len(res) == 1:
        return (
              (int(res[0]) & 63) << 12  # bit 17 - 12 - see version_info[0]
           )
    return ()

def decode_pydist_32bit_to_tuple_str(ddat=0):
    """   Decodes the 32bit hex representation of the Python distribution
    into a dict structure with str names and str representation of releases.
    
    Args:
    
        ddat:
        
            The 32bit value.
    
    Returns:
    
        Dictionary with components: ::
       
            result := {
               'category': 'python',
               'styntaxtype': <str-syntax-release>,
               'dist': <dist-name>,
               'distrel': <str-dist-release>
            }
            
            category:            canonical str name
            str-syntax-release:  string representation
            dist:                canonical str name
            str-dist-release:    string representation
    
    Raises:
    
        pass-through

    """
    try:
        _syn = num2name[ddat & PYE_SYNTAXTYPE]
    except KeyError:
        _syn = ''
    
    try:
        _dis = num2name[ddat & PYE_DIST]
    except KeyError:
        _dis = ''

    if _dis or (ddat & PYE_DISTREL):
        _disrel = "%d.%d.%d" % (
            (ddat & PYE_DISTREL_MAJOR) >> 12,
            (ddat & PYE_DISTREL_MINOR) >> 6,
            ddat & PYE_DISTREL_MICRO,
        )
    else:
        _disrel = ''

    return PyDistStr(
        PYE_PYTHON_NAME,
        _syn,
        _dis,
        _disrel,
    )


def decode_pydist_32bit_to_tuple_segments(ddat=0):
    """   Decodes the 32bit hex representation of the Python distribution
    into a dict structure with str names and numeric release vectors.
    
    Args:
    
        ddat:
        
            The 32bit value.
    
    Returns:
    
        Nametupel with the components: ::
         
            PyDist = namedtuple('PyDist', ('category', 'disttype', 'dist', 'distrel'))
            
            result := PyDist(
               PYE_PYTHON, (<syntax-major>,<syntax-minor>), <32bit-dist>, (<dist-major>, <dist-minor>, <dist-micro>)
             )
            
            PYE_PYTHON:            32bit-enum for category
            32bit-syntax-release:  32bit-value for syntax release
            32bit-dist:            32bit-enum for distribution
            32bit-dist-release:    32bit-value for distribution release
    
        Dictionary with components: ::
       
            result := {
               'category': 'python',
               'styntaxtype': (<syntax-major>,<syntax-minor>),
               'dist': <dist-name>,
               'distrel': (<dist-major>, <dist-minor>, <dist-micro>)
            }
            
            category:      canonical str name
            syntax-major:  int value
            syntax-minor:  int value
            dist:          canonical str name
            dist-major:    int value
            dist-minor:    int value
            dist-micro:    int value
    
    Raises:
    
        pass-through

    """
    return PyDistSegments(
        PYE_PYTHON >> 31,  # the only and one
        (
            (ddat & PYE_SYNTAXTYPE_MAJOR) >> 28,
            (ddat & PYE_SYNTAXTYPE_MINOR) >> 23,
        ),
        (ddat & PYE_DIST) >> 18,
        (
            (ddat & PYE_DISTREL_MAJOR) >> 12,
            (ddat & PYE_DISTREL_MINOR) >> 6,
            ddat & PYE_DISTREL_MICRO,
        )
    )


def decode_pydist_32bit_to_tuple(ddat=0):
    """   Decodes the 32bit hex representation of the Python distribution
    into a flat tuple of numbers.
    
    Args:
    
        ddat:
        
            The 32bit value.
    
    Returns:
    
        Nametupel with the components: ::
         
            PyDist = namedtuple('PyDist', ('category', 'disttype', 'dist', 'distrel'))
            
            result := PyDist(
               PYE_PYTHON, <32bit-syntax-release>, <32bit-dist>, <32bit-dist-release>
             )
            
            PYE_PYTHON:            32bit-enum for category
            32bit-syntax-release:  32bit-value for syntax release
            32bit-dist:            32bit-enum for distribution
            32bit-dist-release:    32bit-value for distribution release

    Raises:
    
        pass-through

    """
    return PyDist(
        ddat & PYE_CATEGORY,
        ddat & PYE_SYNTAXTYPE,
        ddat & PYE_DIST,
        ddat & PYE_DISTREL,
       )


def encode_pydist_to_32bit(d=0, dx=0, dy=0, dz=0, sma=0, smi=0):
    """   Encodes the Python distribution by calculating the 32bit integer 
    bitmask for the provided Python distribution and syntax
    release information.
    
    Args:
        d:
            The numeric enum value of the distribution with original bit-positions.
        
        dx:
            The major distribution version number.
        
        dy:
            The minor distribution version number.
        
        dz:
            The micro distribution version number.
        
        sma:
            The major syntax version number.
        
        smi:
            The minor syntax version number.
    
    Returns:
    
       The 32bit bitmask.
       
            See `Python Distribution Categorization <python_categorization.html>`_.
    
    Raises:
          
        pass-through

    """
    return (
        PYE_PYTHON  # here anything is category=Python
        | d  # distribution enum in it's original bit positions
        | (dx & 63) << 12  # bit 17 - 12 - see version_info[0]
        | (dy & 63) << 6  # bit 11 -  6 - see version_info[1]
        | (dz & 63)  # bit  5 -  0 - see version_info[2] 
        | (sma & 7) << 28  # bit 30 - 28 - see version_info[0]
        | (smi & 31) << 23  # bit 27 - 23 - see version_info[1]
       )


def encode_pydist_segments_to_32bit(**kargs):
    """   Encodes the 32bit bitmask of the compressed platform information
    by the provided values of the sub fields. Non-provided values are
    set to *0*, and though ignored.
    
    This function is mainly designed and foreseen for cache preparation and test 
    environments, though it inherently requires some of the systems performance.
    Thus do not use it within repetitive calls for performance critical large 
    scale loops with small code sections.
    
    Args:
    
        kargs:
        
            category:
            
                The category. The only  and one permitted is *Python*: ::
            
                    category := (
                           PYE_PYTHON  # enum
                         | 'Python'    # Pretty name
                         | 'python'    # key
                         | 0           # None
                    )
            
                default := 0
            
            dist:
            
                The dist: ::
            
                    dist := (
                           PYE_CPYTHON | PYE_IPYTHON | PYE_IRONPYTHON
                         | PYE_JYTHON  | PYE_PYPY
                         | PYE_CIRCUITPYTHON | PYE_MICROPYTHON
                         | <known-name-of-dist>
                         | 0
                    )
                    known-name-of-dist := "case insensitive name or pretty name of the distribution"
                    0 := None
            
                    default:=0
            
            distrel:
            
                The distrel: ::
            
                    distrel := (
                           <int-val>
                         | (<major>, <minor>, <micro>)
                         | 0
                    )
                    int-val := the relative integer value of the distrel bits
                    (<major>, <minor>, <micro>):= the tuple of the Python distribution release
                    0 := None
            
                default := 0

            disttype:
            
                The disttype: ::
            
                    disttype := (
                           <int-val>
                         | (<major>, <minor>)
                         | 0
                    )
                    int-val := the relative integer value of the disttype bits
                    (<major>, <minor>) := the tuple of Python syntax version
                    0 := None
            
                default := 0
                
    Returns:
    
        The 32bit compressed bitmask of the of the distribution.
    
    Raises:
    
        pass-through

    """
    category = kargs.get('category', 0)

    if kargs.get('category'):
        category = 1

    dist = kargs.get('dist', 0)
    try:
        if isinstance(dist, ISSTR):
            dist = dist2num[dist.lower()]
    except KeyError as e:
        # sys.stderr.write("ERROR: unknown dist: " + str(dist))
        e += "\nERROR: unknown dist: %s\n" % (str(dist))
        raise
          
    distrel = kargs.get('distrel', 0)
    if isinstance(distrel, (tuple, list)):
        distrel = distrel[0] << 12 | distrel[1] << 6 | distrel[2]
    elif isinstance(distrel, ISSTR):
        distrel = decode_pysyntax_str_to_num(distrel)

    disttype = kargs.get('disttype', 0)
    if isinstance(disttype, (tuple, list)):
        disttype = int(disttype[0]) << 5 | int(disttype[1])
    elif isinstance(disttype, ISSTR):
        disttype = decode_pysyntax_str_to_num(disttype)
        disttype = int(disttype[0]) << 5 | int(disttype[1])  # ignore [3]

    return (
        category << 31 | disttype << 23 | dist | distrel
    )


class PythonDist(object):

    def __init__(self, *args, **kargs):
        """   Creates an empty object. The instance could be
        either initialized by the provided parameters, 
        or remains empty - which is zero *0*.
        
        Provides *PythonDist.scan()* for the readout of 
        the implementation information. The *scan()* is 
        not called automatic. Each call of *scan()* 
        replaces the previous values. 
        
        Args:
        
            args:
            
                Optional positional parameters in the following order.
                The corresponding keyword-arguments dominate. ::
                
                    *args := [category [, disttype [, dist [, distrel]]]]
            
            kargs:
        
                category:
                
                    The registered *category* for initialization.
                    
                    default := 0
                
                disttype:
                
                    The registered *disttype* for initialization.
                    
                    default := 0
                
                dist:
                
                    The registered *dist* for initialization.
                    
                    default := 0
                
                distrel:
                
                    The registered *distrel* for initialization.
                    
                    default := 0
                
                forceall:
                
                    Controls the default for the scan of content: ::
                    
                        forceall := (
                             True    # scan distribution and compiler
                           | False   # scan distribution only
                        )
                    
                    default := False
        
        Returns:
        
            Initial instance, optionally initialized by the provided
            parameters. 
        
        Raises:
            PythonIDsError
            
            pass-through
    
    """
        
        self.category = PYE_PYTHON  # : the category ID
        self.disttype = 0  # : the type ID of the syntax
        self.hexrelease = 0  # : the resulting hex release
        self.dist = 0  # : the distribution ID
        self.distrel = 0  # : the release of the distribution

        self.compiler = ''
        self.compiler_version = 0
        self.compiler_version_tuple = (0, 0, 0,)

        self.c_libc_version = 0
        self.c_compiler = ''
        self.c_compiler_version = 0

        self.forceall = kargs.get('forceall', False)  # : control the optional part of the scan
        
        self.osrel_sp = []

        if args:
            
            try:
                # 0
                _x = args[0]
                try:
                    # the category, currently only one: Python
                    self.category = dist2num[_x] & PYE_CATEGORY
                except KeyError:
                    raise PythonIDsError("'category' not registered: " + str(_x))

                try:
                    # 1
                    _x = args[1]
                    try:
                        # the syntax type of the distribution
                        # defined by Python syntax version <major>.<minor>
                        self.disttype = dist2num[_x] & PYE_SYNTAXTYPE
                    except KeyError:
                            if not type(_x) is int:
                                # cannot map  
                                raise PythonIDsError("'disttype' not registered: " + str(_x))
                            self.dist = _x & PYE_SYNTAXTYPE

                    try:
                        # 2
                        _x = args[2]
                        try:
                            # the implementation, current supported: CPython, IPython, IronPython, Jython, PyPy
                            self.dist = dist2num[_x] & PYE_DIST
                        except KeyError:
                            raise PythonIDsError("'dist' not registered: " + str(_x))

                        try:
                            # 3
                            _x = args[3]
                            try:
                                # the release version <major>.<minor>.<micro>
                                self.distrel = dist2num[_x] & PYE_DISTREL
                            except KeyError:
                                if not type(_x) is int:  
                                    # cannot be mapped
                                    raise PythonIDsError("'distrel' not registered: " + str(_x))
                                # any release version is supported
                                self.distrel = _x & PYE_DISTREL
                        
                        except KeyError:
                            pass
                    except KeyError:
                        pass
                except KeyError:
                    pass
            except KeyError:
                pass

            
        # keyword arguments dominate
        self.category = kargs.get('category', self.category)
        self.disttype = kargs.get('disttype', self.disttype)
        self.dist = kargs.get('dist', self.dist)
        self.distrel = kargs.get('distrel', self.distrel)
        
        self.hexrelease = self.get_hexrelease()
    
    def get_distribution(self, rtype=PyDist):
        """   Reads out the distribution data into a tuple of selected type.
   
        Args:
            rtype:
                The return type:
              
                    .. parsed-literal::
                    
                        rtype := (
                             :ref:`PyDist <SPEC_PyDist_Class>`
                           | :ref:`PyDistSegments <SPEC_PyDistSegments>`
                           | :ref:`PyDistStr <SPEC_PyDistStr>`
                           | tuple
                           | <user-defined-tuple-type>
                        )
                    
                default := :ref:`PyDist <SPEC_PyDist_Class>`
        
        Returns:
            Returns a tuple of the provided attributes: ::
        
                (
                   category,
                   disttype,
                   dist,
                   distrel
                )
        
        Raises:
            pass-through

    """
        if rtype == PyDist:
            return PyDist(
                self.category,
                self.disttype,
                self.dist,
                self.distrel,
            )
            
        elif rtype == PyDistStr:
            return PyDistStr(
                str(self.category),
                str(self.disttype),
                str(self.dist),
                str(self.distrel),
            )
            
        elif rtype == PyDistSegments:
            return decode_pydist_32bit_to_tuple_segments(self.get_hexrelease())
        
        else:
            # expect a pure tuple type
            return rtype(
                self.category,
                self.disttype,
                self.dist,
                self.distrel,
            )

        
    def scan(self, forceall=None):
        """Scans local platform for attributes specifying the platform.
    Supports: ::
       
        CPython, iPython, IronPython, Jython, PyPy
    
    Args:
        forceall:
            Controls the scan content:  ::
       
                forceall := (
                     True    # scan distribution and compiler
                   | False   # scan distribution only
                )
    
            default := None
    
    Returns:
        Superposes the following mandatory attributes by the scanned values:
       
        * The tuple of Python identifiers: ::
       
            category
            disttype
            dist
            distrel
    
        * Additional shortcuts prepared for direct processing: :: 
       
            hexrelease
       
        * In addition the optional, but strongly supported attributes.
          These are scanned only in case of *forceall==True*. ::
       
            c_libc_version
            c_compiler
            c_compiler_version
    
          Returns the value of *hexrelease*.
       
    Raises:
    
        PythonDistError        

    """
        if forceall == None:
            _forceall = self.forceall
        else:
            _forceall = forceall

        #
        # syntax category
        #
        self.category = PYE_PYTHON  # the only and one supported, contain it for pattern consistance

        #
        # reference syntax
        #
        # _syntaxrel = platform.python_version()
        _syntaxrel_tuple = platform.python_version_tuple()
        self.disttype = _encode_disttype_bitmask(int(_syntaxrel_tuple[0]), int(_syntaxrel_tuple[1]))

        #
        # distribution
        #
        _d = platform.python_implementation()
        try:
            _dist = self.dist = dist2num[_d]
        except KeyError:
            raise PythonDistError("Distribution is not supported: " + str(_d))

        if _dist in (PYE_CPYTHON, PYE_IPYTHON,):  # does not distinguish CPython and IPython - which is a interactive-addon

            # see docu: [ARTICLESTACKOFLOWIPYTHON]_
            try:
                __IPYTHON__  # @UndefinedVariable
                # running under control of IPython addons
                
            except NameError:
                # the standard interpreter and the reference, thus syntaxrel == distrel
                try:
                    self.distrel = _encode_distrel_bitmask(*(int(x) for x in _syntaxrel_tuple[0:3]))
                
                except ValueError:
                    # handle pre-releases, e.g. '3.8.0a5' - these are basically not supported...
                    # these are treated with their version numbers only by dropping any alpha, beta, etc. appendix
                    # though the pythondist package targets production system components only
                    self.distrel = _encode_distrel_bitmask(*(int(x) for x in (
                        _syntaxrel_tuple[0],
                        _syntaxrel_tuple[1], 
                        re.sub(r'^([0-9]).*', r'\1', _syntaxrel_tuple[2])
                        )))

            else:
                _dist = PYE_IPYTHON
                # provided by the core module __version__
                self.distrel = _encode_distrel_bitmask(*(int(x) for x in sys.modules['IPython'].__version__.split('.')))

        elif _dist == PYE_PYPY:
            #
            # contained in the compile string
            #
            # e.g. '2.7.13 (c925e73810367cd960a32592dd7f728f436c125c, Dec 14 2017, 12:47:11)\n[PyPy 5.8.0 with GCC 7.2.1 20170915 (Red Hat 7.2.1-2)]'
            #       ^^^^^^                                                                          ^^^^^      ^^^ ^^^^^
            #
            _c = sys.version
            _cprep = re.sub(
                r'^([0-9.]+).*\n.*PyPy *([0-9.]+) [^ ]+ ([^ ]+) +([0-9.]+).*$', r'\1@@\2@@\3@@\4', 
                _c, flags=re.MULTILINE)  # @UndefinedVariable
            _python_version, _distrel, self.c_compiler, _c_compiler_version = _cprep.split('@@')

            self.distrel = _encode_distrel_str_bitmask(_distrel)

            if _forceall:
                self.c_compiler_version_tuple = tuple(int(i) for i in _c_compiler_version.split('.')) 
                self.c_libc_version = platform.libc_ver()  # default is current instance itself

                self.compiler = "Python" 
                # self.compiler_version = platform.python_version()
                # self.compiler_version = _python_version
                self.compiler_version_tuple = sys.version_info[:3]
                pass

#             else:
#                 self.compiler = "Python" 
#                 self.compiler_version = sys.version_info[:3]

        elif _dist == PYE_IRONPYTHON:
            #
            # >>> platform.python_compiler()
            # '.NET 4.0.30319.42000 (64-bit)'
            #
            # The sys.version seems to be compatible to the python-syntax, but
            # in sync only with major and minor version.
            # The micro version seems to be independent from Python-Syntax/CPython.
            # Current version for simplicity just takes the whole version literally as the syntax version.
            #
            self.distrel = _encode_distrel_bitmask(*(int(x) for x in _syntaxrel_tuple[0:3]))
        
        elif _dist == PYE_JYTHON:
            #
            # the distrel seems to be the same as sys.version
            # and platform.python_version_tuple / platform.python_version 
            #
            self.distrel = _encode_distrel_bitmask(*(int(x) for x in _syntaxrel_tuple[0:3]))

            # the compiler is defined by the jre
            # libc is empty
            #
            # >>> platform.python_compiler()  -> variable JIT
            # 'java1.7.0_65 ( ==linux2 for targets )'
            if _forceall:
                #
                # extra value for the build release, due to it's importance for java-rte
                #
                _c = platform.python_compiler()  # e.g. "str: java1.8.0_181"
                self.c_compiler, self.c_compiler_version = re.sub(r'^([^0-9]*)([0-9.]*)_([0-9]*).*$', r'\1:\2.\3', _c).split(':')
                self.c_compiler_version_tuple = tuple(int(i) for i in self.c_compiler_version.split('.'))
                self.c_libc_version = ('', (0, 0, 0, 0))

                self.compiler = "Java" 
                # self.compiler_version = platform.python_compiler()[4:] 
                # self.compiler_version_tuple = tuple(int(i) for i in self.c_compiler_version.split('.'))
                self.compiler_version_tuple = self.c_compiler_version_tuple

        if _forceall and _dist in (PYE_CPYTHON, PYE_CYTHON, PYE_IPYTHON, PYE_IRONPYTHON):
            _c = platform.python_compiler()
            try:
                # e.g. 'GCC 7.3.1 20180303 (Red Hat 7.3.1-5)'
                self.c_compiler, self.c_compiler_version = re.sub(r'^([^ ]*)[^0-9]*([0-9.]*) .*$', r'\1:\2', _c).split(':')
                self.c_compiler_version_tuple = tuple(int(i) for i in self.c_compiler_version.split('.'))
            except:
                # SunOS
                self.c_compiler = 'C'
                self.c_compiler_version = '' 
                self.c_compiler_version_tuple = (0, 0, 0,)
                
            self.c_libc_version = platform.libc_ver()  # default is current instance itself
            self.compiler = self.c_compiler 
            self.compiler_version = self.c_compiler_version 

        # requires all of them to be set
        self.hexrelease = self.category | self.disttype | self.dist | self.distrel
        
        return self.hexrelease

    def __str__(self):
        ''
        res = ""
        try:
            res += "category           = %s\n" % str(num2name[self.category])
        except KeyError:
            res += "category           = \n"

        try:
            res += "disttype           = %s\n" % (num2name[self.disttype])
        except KeyError:
            res += "disttype           = \n"

        try:
            res += "dist               = %s\n" % (num2name[self.dist])
        except KeyError:
            res += "dist               = \n"

        res += "distrel            = %s\n" % (decode_pydist_32bit_to_tuple_str(self.distrel).distrel)
        res += "hexrelease         = 0x%08x\n" % (self.hexrelease)

        if self.forceall:
            res += "compiler           = %s\n" % (self.compiler)
            res += "compiler_version   = %s\n" % '.'.join(str(i) for i in self.compiler_version_tuple)
            if PYDIST & PYE_DIST == PYE_PYPY:
                res += "c_compiler         = %s\n" % (self.c_compiler)
                res += "c_compiler_version = %s\n" % '.'.join(str(i) for i in self.c_compiler_version_tuple)
                
        return res

    def __getattr__(self, name):
        """Gets the selected attribute."""
        return self.__dict__[name] 
        
    def __setattr__(self, name, value):
        """Sets the selected attribute and synchronizes dependent."""
        self.__dict__[name] = value
        if name != 'hexrelease':
            self.__dict__['hexrelease'] = self.get_hexrelease()

    def __getitem__(self, key):
        ""
        return self.__dict__[key] 

    def __int__(self):
        """   The cast operator into the bitmask which is the *hexrelease*.
        The cache is used without new calculation if *self.hexrelease*
        is present, else created by calling  *get_hexrelease*.
        For the forced calculation only use *get_hexrelease*. ::
           
            int(self) == self-bitmask
        
        Args:
            none
        
        Returns:
            The resulting bitmask of self as numeric value.
        
        Raises:
        
            pass-through

        """
        if not self.hexrelease:
            self.hexrelease = self.get_hexrelease()
        return self.hexrelease

    def __iter__(self):
        """Iterates the non-private attribute names."""
        for k in self.__dict__.keys():
            if k[0] != '_':
                yield k 
    
    def __setitem__(self, key, value):
        """Sets the selected attribute and synchronizes dependent."""
        self.__dict__[key] = value
        if key != 'hexrelease':
            self.__dict__['hexrelease'] = self.get_hexrelease()

    def items(self):
        """Gets the list of key-value tupels."""
        if self.forceall:
            for ix in (
                'category',
                'disttype',
                'dist',
                'distrel',
                'hexrelease',
                'compiler',
                'compiler_version',
                'c_libc_version',
                'c_compiler',
                'c_compiler_version',
                ):
                yield (ix, self[ix])
        else:
            for ix in (
                'category',
                'disttype',
                'dist',
                'distrel',
                'hexrelease',
                ):
                yield (ix, self[ix])

    def keys(self):
        """Gets the list of attribute names."""
        if self.forceall:
            for ix in (
                'category',
                'disttype',
                'dist',
                'distrel',
                'hexrelease',
                'compiler',
                'compiler_version',
                'c_libc_version',
                'c_compiler',
                'c_compiler_version',
                ):
                yield ix
        else:
            for ix in (
                'category',
                'disttype',
                'dist',
                'distrel',
                'hexrelease',
                ):
                yield ix

    def values(self):
        """Gets the list of attribute values."""
        if self.forceall:
            for ix in (
                'category',
                'disttype',
                'dist',
                'distrel',
                'hexrelease',
                'compiler',
                'compiler_version',
                'c_libc_version',
                'c_compiler',
                'c_compiler_version',
                ):
                yield self[ix]
        else:
            for ix in (
                'category',
                'disttype',
                'dist',
                'distrel',
                'hexrelease',
                ):
                yield self[ix]

    def __eq__(self, other): 
        """   Supports standard comparison with the types
        *PythonDist*, and *dict*. In case of
        a *dict* the attributes are used as keys literally.
        
        Synchronizes the hex-value of the release, and compares it with
        the resulting value from *other*.
        
        Args:
            other:
                The instannce to be compared. ::
               
                    other := (
                         <int-16bit-mask>                   # compare with hexversion 
                       | <dictionary>)                      # compare keys only
                       | <tuple>)                           # compare key-index only
                       | <instance-of-PythonDist>           # compare both hexversions
                    )
        
        Returns:
            True or False.
        
        Raises:
            KeyError
           
            AttributeError
        
        """
        
        res = False
        
        if type(other) is int:
            # some special type comparison
            # hex id of dist and/or distrel
            if self.hexrelease == other:
                return True
            return False

        elif isinstance(other, PythonDist):
            return self.hexrelease == other.get_hexrelease()

        elif isinstance(other, dict):
            # compare selected keys only
            res = True
            for k, v in other.items():
                try:
                    if k in ("osrel_sp", "wProductType", "wSuiteMask"):
                        if self.disttype in ('nt', 'cygwin'):
                            res &= self.__dict__[k] == v
                        else:
                            res = False 
                    elif k in ("distrel_version", "osrel_version",):
                        res &= self.__dict__['distrel_version'][:len(v)] == v
                    elif k == "distrel":
                        res &= self.__dict__['distrel'].startswith(v)
                    else:
                        res &= self.__dict__[k] == v 
                except KeyError:
                    res = False

        elif isinstance(other, tuple):
            # compare selected keys only

            res = True
            self.osrel_sp = []
            _myargs = list(other)
            if _myargs:
                res &= self.category == _myargs[0]
                _myargs.pop(0)
            if _myargs:
                res &= self.disttype == _myargs[0]
                _myargs.pop(0)
            if _myargs:
                res &= self.dist == _myargs[0]
                _myargs.pop(0)
            if _myargs:
                res &= self.distrel == _myargs[0]
                _myargs.pop(0)

        try:
            # jython - 32bit is a long(unsigned int)
            if isinstance(other, long) and self.hexrelease == other:  # @UndefinedVariable
                return True
        except NameError:
            pass
            
        return res

    def __ne__(self, other):
        ''
        return not self.__eq__(other)
    
    def __ge__(self, other):
        """The *>=* operator for the resulting *hexversion*: ::
             
            self-bitmask >= other-bitmask
        
        Args:
            other:
                The bitmask for operations. ::
        
                    other := (
                         <int-16bit-mask>               # compare with hexversion 
                       | <dictionary>)                  # compare keys only
                       | <tuple>)                       # compare key-index only
                       | <instance-of-PythonDist>       # compare both hexversions
                    )
           
        Returns:
            True or False.
        
        Raises:
        
            pass-through

        """
        
        if not self.hexrelease:
            self.hexrelease = self.get_hexrelease()

        if isinstance(other, int):
            return self.hexrelease >= other

        elif isinstance(other, PythonDist):
            return self.hexrelease >= other.get_hexrelease()

        elif isinstance(other, dict):
            # use other as init parameters - simply trust or pass exception
            return self.hexrelease >= PythonDist(**other).get_hexrelease()

        elif isinstance(other, tuple):
            return self.hexrelease >= PythonDist(*other).get_hexrelease()

        try:
            # jython - 32bit is a long(unsigned int)
            if isinstance(other, long):  # @UndefinedVariable
                return self.hexrelease >= other
        except NameError:
            pass

        raise PythonIDsError("type not supported: other = " + str(other))
    
    def __le__(self, other):
        """The *<=* operator for the resulting *hexversion*: ::
        
            self-bitmask <= other-bitmask
   
        Args:
            other:
                The bitmask for operations. ::
        
                    other := (
                         <int-16bit-mask>               # compare with hexversion 
                       | <dictionary>)                  # compare keys only
                       | <tuple>)                       # compare key-index only
                       | <instance-of-PythonDist>       # compare both hexversions
                    )
           
        Returns:
            The resulting bitmask as numeric value.
        
        Raises:
        
            pass-through
   
        """
        if not self.hexrelease:
            self.hexrelease = self.get_hexrelease()

        if isinstance(other, int):
            return self.hexrelease <= other

        elif isinstance(other, PythonDist):
            return self.hexrelease <= other.get_hexrelease()

        elif isinstance(other, dict):
            # use other as init parameters - simply trust or pass exception
            return self.hexrelease <= PythonDist(**other).get_hexrelease()

        elif isinstance(other, tuple):
            return self.hexrelease <= PythonDist(*other).get_hexrelease()

        try:
            # jython - 32bit is a long(unsigned int)
            if isinstance(other, long):  # @UndefinedVariable
                return self.hexrelease <= other
        except NameError:
            pass

        raise PythonIDsError("type not supported: other = " + str(other))
    
    def __gt__(self, other):
        """The *>* operator for the resulting *hexversion*: ::
        
            self-bitmask > other-bitmask
   
        Args:
            other:
                The bitmask for operations. ::

                    other := (
                         <int-16bit-mask>               # compare with hexversion 
                       | <dictionary>)                  # compare keys only
                       | <tuple>)                       # compare key-index only
                       | <instance-of-PythonDist>       # compare both hexversions
                    )
           
        Returns:
            True or False.
        
        Raises:
        
            pass-through

        """
        if not self.hexrelease:
            self.hexrelease = self.get_hexrelease()

        if isinstance(other, int):
            return self.hexrelease > other

        elif isinstance(other, PythonDist):
            return self.hexrelease > other.get_hexrelease()

        elif isinstance(other, dict):
            # use other as init parameters - simply trust or pass exception
            return self.hexrelease > PythonDist(**other).get_hexrelease()

        elif isinstance(other, tuple):
            return self.hexrelease > PythonDist(*other).get_hexrelease()

        try:
            # jython - 32bit is a long(unsigned int)
            if isinstance(other, long):  # @UndefinedVariable
                return self.hexrelease > other
        except NameError:
            pass

        raise PythonIDsError("type not supported: other = " + str(other))
    
    def __lt__(self, other):
        """The *<* operator for the resulting *hexversion*: ::
        
            self-bitmask < other-bitmask
   
        Args:
            other:
                The bitmask for operations. ::

                    other := (
                         <int-16bit-mask>               # compare with hexversion 
                       | <dictionary>)                  # compare keys only
                       | <tuple>)                       # compare key-index only
                       | <instance-of-PythonDist>       # compare both hexversions
                    )
           
        Returns:
            True or False.
        
        Raises:
        
            pass-through
   
        """
        if not self.hexrelease:
            self.hexrelease = self.get_hexrelease()

        if isinstance(other, int):
            return self.hexrelease < other

        elif isinstance(other, PythonDist):
            return self.hexrelease < other.get_hexrelease()

        elif isinstance(other, dict):
            # use other as init parameters - simply trust or pass exception
            return self.hexrelease < PythonDist(**other).get_hexrelease()

        elif isinstance(other, tuple):
            return self.hexrelease < PythonDist(*other).get_hexrelease()

        try:
            # jython - 32bit is a long(unsigned int)
            if isinstance(other, long):  # @UndefinedVariable
                return self.hexrelease < other
        except NameError:
            pass

        raise PythonIDsError("type not supported: other = " + str(other))
    
    def __repr__(self):
        """The standard representation. The contained attributes are represented as 
        numeric 32bit-enums and values, for example: ::
        
            res = {"category": 2147483648, "disttype": 0, "dist": 0, "distrel": 595591168, "hexrelease": 2743074816}

        """
        res = (
            '{"category": 0x%08x, "disttype": 0x%08x, "dist": 0x%08x, '
            '"distrel": 0x%08x, "hexrelease": 0x%08x') % (
                self.category,
                self.disttype,
                self.dist,
                self.distrel,
                self.hexrelease,
            )
        if self.forceall:
            res += ', "compiler": "%s"' % (self.compiler)
            res += ', "compiler_version": "%s"' % (self.compiler_version)
            if PYDIST & PYE_DIST == PYE_PYPY:
                res += ', "c_compiler": "%s"' % (self.c_compiler)
                res += ', "c_compiler_version": "%s"' % (self.c_compiler_version)

        res += "}"
 
        return res
 
    def __and__(self, other):
        """The *&* operator for the resulting *hexversion*: ::

            self-bitmask & other-bitmask
        
        Args:
            other:
                The bitmask for operations. ::

                   other := (
                        <int-16bit-mask>                   # compare with hexversion 
                      | <dictionary>)                      # compare keys only
                      | <tuple>)                           # compare key-index only
                      | <instance-of-PythonDist>     # compare both hexversions
                   )
           
        Returns:
            The resulting bitmask as numeric value.
        
        Raises:
        
            pass-through

        """

        if not self.hexrelease:
            self.hexrelease = self.get_hexrelease()

        if isinstance(other, int):
            return self.hexrelease & other

        elif isinstance(other, PythonDist):
            return self.hexrelease & other.get_hexrelease()

        elif isinstance(other, dict):
            # use other as init parameters - simply trust or pass exception
            return self.hexrelease & PythonDist(**other).get_hexrelease()

        elif isinstance(other, tuple):
            return self.hexrelease & PythonDist(*other).get_hexrelease()

        try:
            # jython - 32bit is a long(unsigned int)
            if isinstance(other, long):  # @UndefinedVariable
                return self.hexrelease & other
        except NameError:
            pass

        raise PythonIDsError("type not supported: other = " + str(other))
    
    def __iand__(self, other):
        """The in-place *&* operator for the resulting *hexversion*: ::
     
            self-bitmask &= other-bitmask
   
        Args:
            other:
                The bitmask for operations. ::
        
                    other := (
                         <int-16bit-mask>               # compare with hexversion 
                       | <dictionary>)                  # compare keys only
                       | <tuple>)                       # compare key-index only
                       | <instance-of-PythonDist>       # compare both hexversions
                    )
           
        Returns:
            The resulting bitmask as numeric value.
        
        Raises:
        
            pass-through

        """
        if not self.hexrelease:
            self.hexrelease = self.get_hexrelease()

        if isinstance(other, int):
            self.hexrelease &= other

        elif isinstance(other, PythonDist):
            self.hexrelease &= other.get_hexrelease()

        elif isinstance(other, dict):
            self.hexrelease &= PythonDist(**other).get_hexrelease()

        elif isinstance(other, tuple):
            self.hexrelease &= PythonDist(*other).get_hexrelease()
        else:
            raise PythonIDsError("type not supported: other = " + str(other))
        
        try:
            # jython - 32bit is a long(unsigned int)
            if isinstance(other, long):  # @UndefinedVariable
                self.hexrelease &= other
        except NameError:
            pass

        self.category, self.disttype, self.dist, self.distrel = decode_pydist_32bit_to_tuple(self.hexrelease)
        return self

    def __ior__(self, other):
        """The in-place *|* operator for the resulting *hexversion*: ::
        
            self-bitmask |= other-bitmask
   
        Args:
            other:
                The bitmask for operations. ::

                    other := (
                         <int-16bit-mask>               # compare with hexversion 
                       | <dictionary>)                  # compare keys only
                       | <tuple>)                       # compare key-index only
                       | <instance-of-PythonDist>       # compare both hexversions
                    )
           
        Returns:
            The resulting bitmask as numeric value.
        
        Raises:
        
            pass-through

        """
        if not self.hexrelease:
            self.hexrelease = self.get_hexrelease()

        if isinstance(other, int):
            self.hexrelease |= other
            return self

        elif isinstance(other, PythonDist):
            self.hexrelease |= other.get_hexrelease()
            return self

        elif isinstance(other, dict):
            self.hexrelease |= PythonDist(**other).get_hexrelease()
            return self

        elif isinstance(other, tuple):
            self.hexrelease |= PythonDist(*other).get_hexrelease()
            return self

        try:
            # jython - 32bit is a long(unsigned int)
            if isinstance(other, long):  # @UndefinedVariable
                self.hexrelease |= other
                return self
        except NameError:
            pass
        
        raise PythonIDsError("type not supported: other = " + str(other))

    def __or__(self, other):
        """The *|* operator for the resulting *hexversion*: ::
        
            self-bitmask | other-bitmask
   
        Args:
            other:
                The bitmask for operations. ::

                    other := (
                         <int-16bit-mask>               # compare with hexversion 
                       | <dictionary>)                  # compare keys only
                       | <tuple>)                       # compare key-index only
                       | <instance-of-PythonDist>       # compare both hexversions
                    )
           
        Returns:
            The resulting bitmask as numeric value.
        
        Raises:
        
            pass-through

        """
        if not self.hexrelease:
            self.hexrelease = self.get_hexrelease()

        if isinstance(other, int):
            return self.hexrelease | other

        elif isinstance(other, PythonDist):
            return self.hexrelease | other.get_hexrelease()

        elif isinstance(other, dict):
            # use other as init parameters - simply trust or pass exception
            return self.hexrelease | PythonDist(**other).get_hexrelease()

        elif isinstance(other, tuple):
            return self.hexrelease | PythonDist(*other).get_hexrelease()

        try:
            # jython - 32bit is a long(unsigned int)
            if isinstance(other, long):  # @UndefinedVariable
                return self.hexrelease | other
        except NameError:
            pass

        raise PythonIDsError("type not supported: other = " + str(other))
    
    def __rand__(self, other):
        """The r-side *&* operator for the resulting *hexversion*: ::
        
            other-bitmask & self-bitmask
   
        Args:
            other:
                The bitmask for operations. ::
        
                    other := (
                         <int-16bit-mask>               # compare with hexversion 
                       | <dictionary>)                  # compare keys only
                       | <tuple>)                       # compare key-index only
                       | <instance-of-PythonDist>       # compare both hexversions
                    )
           
        Returns:
            The resulting bitmask as numeric value.
        
        Raises:
        
            pass-through

        """
        return self.__and__(other)

    def __ror__(self, other):
        """The right-side *|* operator for the resulting *hexversion*: ::
        
            other-bitmask | self-bitmask
   
        Args:
            other:
               The bitmask for operations. ::

                    other := (
                         <int-16bit-mask>               # compare with hexversion 
                       | <dictionary>)                  # compare keys only
                       | <tuple>)                       # compare key-index only
                       | <instance-of-PythonDist>       # compare both hexversions
                    )
           
        Returns:
            The resulting bitmask as numeric value.
        
        Raises:
        
            pass-through

        """
        return self.__or__(other)
   
    def get_hexrelease(self):
        """   Returns the dynamically calculated hex version
        resulting from current values of the member attributes.
        When not all present, uses the available stack attributes.
        Does not use cached values, nor stores the result. 
        For the use and recreation of cached values call  *__int__*. 
        """
        try:
            return self.category | self.disttype | self.dist | self.distrel
        except (TypeError, KeyError):
            # basically for bootstrap of __init__ only
            res = 0
            try:
                res |= self.category
            except:
                pass
            try:
                res |= self.disttype
            except:
                pass
            try:
                res |= self.dist
            except:
                pass
            try:
                res |= self.distrel
            except:
                pass
            return res

            
#
# the default is with core attributes only - which almost for sure must not raise exceptions at all
#
PYDIST_DATA = PythonDist(forceall=True)  #: Creates the object for the current runtime environment and scans the parameters.
PYDIST_DATA.scan()


PYDIST = PYDIST_DATA.get_hexrelease()  #: Sets the hex value for fast access based on PYDIST_DATA,

if (PYDIST & PYE_DIST) == PYE_JYTHON:
    # Jython knows the type long - and casts to it from 32bit on
    isJython = True
    ISINT = (int, long,)  # @UndefinedVariable
    ISNUM = (int, float, long,)  # @UndefinedVariable
    
else:
    isJython = False
    ISINT = (int,)
    ISNUM = (int, float,)  # @UndefinedVariable

