# -*- coding: utf-8 -*-
"""*pythonids* provides common information about the Python syntax.
"""
#############################################
#
# See manuals for the detailed API.
#
#############################################

import sys
import os
import re


__author__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2010-2018 Arno-Can Uestuensoez" \
                " @Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.1.31'
__uuid__ = "5624dc41-775a-4d17-ac42-14a0d5c41d1a"

__docformat__ = "restructuredtext en"


_debug = 0
_verbose = 0


class PythonIDsError(Exception):
    """Subsystem *PythonIDs*.
    """
    pass


class PythonIDsImplementationError(Exception):
    """Python implementation not supported.
    """
    pass


def decode_pysyntax_16bit_to_str(xyz, form="%d.%d.%d"):
    """Decodes the compressed version 16bit integer bitmask
    into the corresponding string.
    
    The optional format string *form* provides the formatting
    of a 3-value interger tuple. E.g. *form="%02d.%02d.%03d"*.
    
    Due to the spared error checks the string has to be correct!
    
    """
    return form % (
       (xyz >> 13) &   7,  # bit 15 - 13 - see version_info[0] - PythonX
       (xyz >>  8) &  31,  # bit 12 -  8 - see version_info[1] - Pythonx.Y
        xyz        & 255,  # bit  7 -  0 - see version_info[2] - Pythonx.y - x.y.Y
    )


def decode_pysyntax_16bit_to_tuple(xyz):
    """   Decodes the compressed version 16bit integer bitmask
    into the corresponding tuple of integer values.
    
    """
    return (
       (xyz >> 13) &   7,  # bit 15 - 13 - see version_info[0] - PythonX
       (xyz >>  8) &  31,  # bit 12 -  8 - see version_info[1] - Pythonx.Y
        xyz        & 255,  # bit  7 -  0 - see version_info[2] - Pythonx.y - x.y.Y
    )


def decode_pysyntax_16bit_to_tuple_str(xyz):
    """Decodes the compressed version 16bit integer bitmask
    into the corresponding tuple of integer values.
    
    """
    return (
        str((xyz >> 13) &   7),  # bit 15 - 13 - see version_info[0] - PythonX
        str((xyz >>  8) &  31),  # bit 12 -  8 - see version_info[1] - Pythonx.Y
        str(xyz        & 255),   # bit  7 -  0 - see version_info[2] - Pythonx.y - x.y.Y
    )


def decode_pysyntax_str_to_num(v):
    """   Split a version string separated by '.' into an integer 
    tuple. ::
       
        decode_pysyntax_str_to_num('1.22.17')  =>  (1, 22, 17)
    
    A tiny utility - frequently required.
    
    Args:
    
        Version string 'x.y.z'.
    
    Returns:
    
        Integer tuple (x, y, z)
    
    Raises:
    
        ValueError

    """
    return tuple(int(x) for x in v.split('.'))


def encode_pysyntax_to_16bit(x=0, y=0, z=0):
    """   Encodes the version by calculating the 16bit integer 
    bitmask for the provided Python release values.
    
    Args:
        x:
            The major version number. ::
        
                0 <= x
                
                0 <= x0 < 8  # internal low-level 16-bit optimization threshold 
        
        y:
            The minor version number. ::
        
                0 <= y < 32
        
        z:
               The numeric relase-build tag. ::
        
                    0 <= z < 256
    
    Returns:
    
        The bitmask.
    
    Raises:
       
        pass-through
    
    """
    return (
          (x &   7) << 13  # bit 15 - 13 - see version_info[0] - PythonX
        | (y &  31) << 8   # bit 12 -  8 - see version_info[1] - Pythonx.Y
        | (z & 255)        # bit  7 -  0 - see version_info[2] - Pythonx.y - x.y.Z
       )


#
# official API
#
PYV2 =      16384  #: 16384 = encode_pysyntax_to_16bit(2,)
PYV27 =     18176  #: 18176 = encode_pysyntax_to_16bit(2, 7)
PYV3 =      24576  #: 24576 = encode_pysyntax_to_16bit(3,)
PYV33 =     25344  #: 25344 = encode_pysyntax_to_16bit(3, 3)
PYV35 =     25856  #: 25856 = encode_pysyntax_to_16bit(3, 5)
PYV36 =     26112  #: 26112 = encode_pysyntax_to_16bit(3, 6)
PYV37 =     26368  #: 26368 = encode_pysyntax_to_16bit(3, 7, 0)
PYV38 =     26624  #: 26624 = encode_pysyntax_to_16bit(3, 8, 0)
PYV39 =     26880  #: 26880 = encode_pysyntax_to_16bit(3, 9, 0)


#
# short term development support
#
PYV2715 =   18191  #: 18191 = encode_pysyntax_to_16bit(2, 7, 15)
PYV2716 =   18192  #: 18192 = encode_pysyntax_to_16bit(2, 7, 16)
PYV31 =     24832  #: 24832 = encode_pysyntax_to_16bit(3, 1)
PYV32 =     25088  #: 25088 = encode_pysyntax_to_16bit(3, 2)
PYV34 =     25600  #: 25600 = encode_pysyntax_to_16bit(3, 4)
PYV362 =    26114  #: 26114 = encode_pysyntax_to_16bit(3, 6, 2)
PYV365 =    26117  #: 26117 = encode_pysyntax_to_16bit(3, 6, 5)
PYV366 =    26118  #: 26118 = encode_pysyntax_to_16bit(3, 6, 6)
PYV367 =    26119  #: 26119 = encode_pysyntax_to_16bit(3, 6, 7)
PYV368 =    26120  #: 26120 = encode_pysyntax_to_16bit(3, 6, 8)
PYV369 =    26121  #: 26121 = encode_pysyntax_to_16bit(3, 6, 9)
PYV371 =    26369  #: 26369 = encode_pysyntax_to_16bit(3, 7, 1)
PYV372 =    26370  #: 26370 = encode_pysyntax_to_16bit(3, 7, 2)
PYV373 =    26371  #: 26371 = encode_pysyntax_to_16bit(3, 7, 3)
PYV374 =    26372  #: 26372 = encode_pysyntax_to_16bit(3, 7, 4)
PYV375 =    26373  #: 26373 = encode_pysyntax_to_16bit(3, 7, 5)
PYV376 =    26374  #: 26374 = encode_pysyntax_to_16bit(3, 7, 6)
PYV381 =    26625  #: 26625 = ncode_pysyntax_to_16bit(3, 8, 1)

#: The 3-value Python final release of the current process in accordance to PEP440.
#: The location of the implementation information varies, see *pythonids.pythondist*.
PYVxyz = encode_pysyntax_to_16bit(*sys.version_info[:3])

#:
#: Adjust to current major Python version to Python3 vs. Python2.
#:
PYV27X = PYVxyz & PYV27 == PYV27  #: Python2.7
PYV3X = PYVxyz >= PYV3  #: Python3 
PYV3X3 = PYVxyz >= PYV3 and PYVxyz < PYV34 #: Python3.0 - Python3.3  
PYV35Plus = PYVxyz >= PYV35  #: Python3.5+ - all following

if PYV35Plus:
    ISSTR = (str, bytes)  #: string and unicode
    ISSTRBASE = (str,)  #: str

    #: Superpose for generic Python3 compatibility.
    unicode = str  # @ReservedAssignment

elif PYV3X:
    ISSTR = (str, bytes)  #: string and unicode
    ISSTRBASE = (str,)  #: str

    #: Superpose for generic Python3 compatibility.
    unicode = str  # @ReservedAssignment

elif PYV27X:
    ISSTR = (str, unicode)  #: string and unicode
    ISSTRBASE = (str, unicode,)  #: basestring
    unicode = unicode  # @ReservedAssignment

else:
    raise PythonIDsError(
        "Requires Python 2.7+, or 3.5+, current: " 
        + str(sys.version_info[:2]))
