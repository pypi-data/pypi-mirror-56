# -*- coding: utf-8 -*-
"""pysourceinfo.helper - miscellaneous utilities - details see manuals
"""
from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import re
from inspect import stack
from imp import PY_SOURCE, PY_COMPILED, C_EXTENSION, PKG_DIRECTORY, C_BUILTIN, PY_FROZEN

from platformids import V3K
from sourceinfo import SourceInfoError, \
    presolve, P_FIRST, P_LAST, P_LONGEST, P_SHORTEST, P_IGNORE0

if V3K:
    # pylint: disable-msg=F0401
    from importlib.machinery import SOURCE_SUFFIXES, DEBUG_BYTECODE_SUFFIXES, OPTIMIZED_BYTECODE_SUFFIXES, BYTECODE_SUFFIXES, EXTENSION_SUFFIXES  # @UnresolvedImport
    from importlib import util  # @UnresolvedImport
    # pylint: enable-msg=F0401
else:
    from inspect import getmoduleinfo  # @UnresolvedImport


__author__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2010-2017 Arno-Can Uestuensoez" \
    " @Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.1.21'
__uuid__ = '9de52399-7752-4633-9fdc-66c87a9200b8'

__docformat__ = "restructuredtext en"


# redundant for dependency reduction - keep in sync with pysourceinfo.objectinfo
__MT_UNKNOWN = 0
__MT_SOURCE = 1  # PY_SOURCE #1
__MT_COMPILED = 2  # PY_COMPILED #2
__MT_EXTENSION = 3  # C_EXTENSION #3
__MT_DIRECTORY = 5  # PKG_DIRECTORY #5
__MT_BUILTIN = 6  # C_BUILTIN #6
__MT_FROZEN = 7  # PY_FROZEN #7
__MT_COMPILED_OPT1 = 10  # PY_COMPILED | <opt1> # 2 | 8
__MT_COMPILED_OPT2 = 18  # PY_COMPILED | <opt2> # 2 | 16
__MT_COMPILED_DEBUG = 34  # PY_COMPILED # 2


_scname = re.compile(
    r'''.*[\\\\/]([^.]+)[.]([^-]+)-([0-9]{2})[.](opt-[012])*([.].+)$''')


def getfilepathname_type(fpath):
    """Type for stored module as defined by *imp*."""

    if not V3K:  # for now the more frequent call
        if not os.path.exists(fpath):
            return
        ret = getmoduleinfo(fpath)
        if ret and ret[3] in (PY_SOURCE, PY_COMPILED, C_EXTENSION, PKG_DIRECTORY, C_BUILTIN, PY_FROZEN):
            return ret[3]

    else:
        if not os.path.exists(fpath):
            return

        #
        # the redundnacy of type-postfixes requires now prefix-analysis by '_scname'
        #
        
        # In [1]: from importlib.machinery import SOURCE_SUFFIXES, DEBUG_BYTECODE_SUFFIXES
        #    ...: , OPTIMIZED_BYTECODE_SUFFIXES, BYTECODE_SUFFIXES, EXTENSION_SUFFIXES
        # 
        # In [3]: SOURCE_SUFFIXES
        # Out[3]: ['.py']
        # 
        # In [4]: DEBUG_BYTECODE_SUFFIXES
        # Out[4]: ['.pyc']
        # 
        # In [5]: OPTIMIZED_BYTECODE_SUFFIXES
        # Out[5]: ['.pyc']
        # 
        # In [6]: BYTECODE_SUFFIXES
        # Out[6]: ['.pyc']
        # 
        # In [7]: EXTENSION_SUFFIXES
        # Out[7]: ['.cpython-36m-x86_64-linux-gnu.so', '.abi3.so', '.so']

        x = _scname.findall(fpath)
        if x:
            x = x[0]  # trust...
        else:
            x = os.path.splitext(fpath)

        if x[-1] in SOURCE_SUFFIXES:
            return __MT_SOURCE
        elif x[-1] in EXTENSION_SUFFIXES:
            return __MT_EXTENSION
        elif x[-1] in BYTECODE_SUFFIXES and not x[-2]:
            return __MT_COMPILED
        elif x[-1] in OPTIMIZED_BYTECODE_SUFFIXES and x[-2]:
            if x[-2] == 'opt-1':
                return __MT_COMPILED_OPT1
            if x[-2] == 'opt-2':
                return __MT_COMPILED_OPT2
            raise SourceInfoError(
                "Unknown opt:" + str(x[-2]) + " " + str(fpath))
        elif x[-1] in DEBUG_BYTECODE_SUFFIXES:
            return __MT_COMPILED_DEBUG
    return __MT_UNKNOWN


def get_oid_filepathname(oid, spath=None):
    """File path name for OID."""
    find_spec = util.find_spec(oid, spath)
    if not find_spec is None:
        return find_spec.origin


def getpythonpath(pname, plist=None, **kw):
    """Matches prefix from sys.path.
    
    Args:
        **pname**:
            Path name to be searched an appropriate
            pythonpath prefix for, either absolute
            or relative to an item of *plist*.

        **plist**:
            Alternative to *sys.path*.
            
            *default := sys.path*

        kw:
            **ispre**:
                If *True* adds a postfix path separator.

            **presolve**:
                The type of path resolution: ::

                   presolve := (
                        P_FIRST
                      | P_LAST
                      | P_LONGEST
                      | P_SHORTEST
                   )

                *default := pysourceinfo.presolve(P_FIRST)*

            **verify**:
                Verify against the filesystem, else no checks
                are done.
                
                *default := True*

    Returns:
        First matched path from *sys.path* as normalized
        path.
        Else:
            ispre == True: returns empty str - ''
            else:          returns None

    Raises:
        SourceInfoError

        pass-through

    """
    _pre = kw.get('ispre')
    _verify = kw.get('verify', True) 
    if not pname:
        # shortcut for empty/None - so following check know a parameter is provided
        if _verify:
            raise SourceInfoError('no valid param pname = "%s"' % (str(pname)))
        if _pre:
            return ''
        return None
    if not plist:
        plist = sys.path

    _presolve = kw.get('presolve', presolve)

    # path or object name
    try:
        _fp = os.path.normpath(pname)
    except TypeError:
        try:
            _fp = os.path.normpath(pname.__file__)
        except:
            if _verify:
                raise SourceInfoError('not valid pname = %s' % (str(pname)))

    #
    # now shure, 'pname' is s.th. valid
    #
    
    if os.path.isabs(_fp):
        if pname in plist:
            # is a search path itself

            if _verify and not os.path.exists(pname):
                # absolute is has to exist itself
                raise SourceInfoError('does not exist: \n   abs: %s' % (str(pname)))

            # simply not searched
            if _pre:
                return _fp + os.sep
            return _fp

        if _verify:
            _fplst = []
            for x in plist:
                if _fp.startswith(x) and os.path.exists(x):
                    _fplst.append(x)

        else:
            _fplst = [x for x in plist if _fp.startswith(x)]

    else:
        _fplst = []
        for _sp in plist:
            if _verify and not os.path.exists(_sp + os.sep + _fp):
                continue

            if _pre:
                _fplst.append(_sp + os.sep)
            else:
                _fplst.append(_sp)

    if _verify and not _fplst:
        raise SourceInfoError('does not exist: %s' % (str(pname)))

    if _presolve == P_FIRST:
        if _verify and not os.path.exists(_fplst[0]):
            raise SourceInfoError('does not exist: %s' % (str(_fplst[0])))
        return _fplst[0]

    elif _presolve == P_LAST:
        if _verify and not os.path.exists(_fplst[-1]):
            raise SourceInfoError('does not exist: %s' % (str(_fplst[-1])))
        return _fplst[-1]

    elif _presolve == P_LONGEST:
        _fpnew = ''
        for x in _fplst:
            if _verify and not os.path.exists(x):
                continue

            if len(x.split(os.sep)) > len(_fpnew.split(os.sep)):  # number of path-items
                _fpnew = x

    elif _presolve == P_SHORTEST:
        _fpnew = ''
        for x in _fplst:
            if _verify and not os.path.exists(x):
                continue

            if not _fpnew:
                _fpnew = x 

            elif len(x.split(os.sep)) < len(_fpnew.split(os.sep)):  # number of path-items
                _fpnew = x

    else:
        raise SourceInfoError("unknown presolve = " + str(presolve))


    if _verify and not _fpnew:
        raise SourceInfoError('does not exist: %s' % (str(pname)))

    return _fpnew


def getpythonpath_rel(pname, plist=None, **kw):
    """Verifies an absolute or relative path name to be
    reachable as a relative path to one item of the search
    list *plist*.
    
    Args:
        **pname**:
            Path name of a path searched for relative to
            an item of *plist*. Absolute is cut, relative
            is searched literally.

        **plist**:
            Alternative to *sys.path*.
            
            *default := sys.path*

        kargs:
            **presolve**:
                The type of path resolution: ::

                   pname is relative:

                       presolve := (
                           P_FIRST
                       )

                   pname is absolute:

                      presolve := (
                           P_FIRST
                         | P_LAST
                         | P_LONGEST
                         | P_SHORTEST
                      )

                *default := pysourceinfo.presolve(P_FIRST)*

            **verify**:
                Verify against the file system, else no checks
                are done.
                
                *default := True*

    Returns:
        First matched path from *sys.path* as normalized path.
        Else:
            if PYTHONPATH[i] == pname:   returns empty str - ''
            else:
                if verify:               raise SourceInfoError 
                else:                    returns None

    Raises:
        SourceInfoError

        pass-through
        
    """
    _verify = kw.get('verify') 
    if not pname:
        # shortcut for empty/None - so following check know a parameter is provided
        if _verify:
            raise SourceInfoError('no valid param pname = "%s"' % (str(pname)))
        return pname
    if not plist:
        plist = sys.path

    if os.path.isabs(pname):
        _presolve = kw.get('presolve', presolve)
    else:
        _presolve = P_FIRST


    # path or object name
    try:
        _fp = os.path.normpath(pname)
    except TypeError:
        try:
            _fp = os.path.normpath(pname.__file__)
        except:
            if _verify:
                raise SourceInfoError('not valid pname = %s' % (str(pname)))

    #
    # now shure, 'pname' is s.th. valid
    #
    if os.path.isabs(_fp):
        if pname in plist:
            # is a search path itself

            if _verify and not os.path.exists(pname):
                # absolute is has to exist itself
                raise SourceInfoError('does not exist: \n   abs: %s' % (str(pname)))
            if pname == _fp:
                return ''
            return _fp

        # for now assume x=='' is not valid
        _fplst = [x for x in plist if x and _fp.startswith(x)]

    else:
        _fplst = []
        for _sp in plist:
            if _sp + os.sep + _fp:
                _fplst.append(_sp)
            else:
                continue
    
    # no plist
    if not _fplst:
        if pname == '':
            if not _verify:
                return ''
        if not _verify:
            return
        raise SourceInfoError('does not exist: %s' % (str(pname)))

    if _presolve == P_FIRST:
        if _verify and not os.path.exists(_fplst[0]):
            raise SourceInfoError('does not exist: %s' % (str(_fplst[0])))
        if os.path.isabs(_fp):
            _ret = _fp[len(_fplst[0]):]
            if os.path.isabs(_ret):
                return _ret[1:]
        else:
            return _fp

    elif _presolve == P_LAST:
        if _verify and not os.path.exists(_fplst[-1]):
            raise SourceInfoError('does not exist: %s' % (str(_fplst[-1])))
        if os.path.isabs(_fp):
            _ret = _fp[len(_fplst[-1]):]
            if os.path.isabs(_ret):
                return _ret[1:]
        else:
            return _fp

    elif _presolve == P_LONGEST:
        _fpnew = ''

        _shortest = ''
        for x in _fplst:
            if _verify and not os.path.exists(x):
                continue

            if not _shortest:
                _shortest = x

            for y in plist:
                if x.startswith(y):
                    if y and len(y.split(os.sep)) < len(_shortest.split(os.sep)):  
                        _shortest = y

            if not _fpnew:
                _fpnew = x 

            elif len(x.split(os.sep)) < len(_fpnew.split(os.sep)):  
                # number of path-items - search longest relative sub, neef shortest python path
                _fpnew = x


        if _fpnew:
            if _fpnew[-1] == os.sep:
                return pname[len(_fpnew):]
            return pname[len(_fpnew) + 1:]

    elif _presolve == P_SHORTEST:
        # simple literal static sub directories only
        kw['presolve'] = P_LONGEST
        _longest = getpythonpath(_fp, plist, **kw)
        _sp = _fp[len(_longest):]

        if os.path.isabs(_sp):
            return _sp[1:]
        return _sp

    else:
        raise SourceInfoError("unknown presolve = " + str(presolve))

    if _verify and not _fpnew:
        raise SourceInfoError('does not exist: %s' % (str(pname)))

    return _fpnew


def getstack_frame(spos=1, fromtop=False):
    """List of current mem-addresses on stack frames."""
    if fromtop:
        return stack()[-1 * spos]
    return stack()[spos]


def getstack_len():
    """Length of current stack."""
    return len(stack())

def matchpath(path, pathlist=None, pmatch=P_FIRST):
    """Match a file pathname of pathname on a pathlist."""
    _buf = None
    if pathlist == None:
        pathlist = sys.path
        
    if pmatch & P_IGNORE0:
        _pl = pathlist[1:]
    else:
        _pl = pathlist
    for sx in _pl:
        p0 = os.path.normpath(sx)
        if path.startswith(p0):
            if pmatch & P_FIRST:
                return p0
            elif pmatch & P_LAST:
                _buf = p0
            elif pmatch & P_LONGEST:
                if len(p0) > len(_buf):
                    _buf = p0
            elif pmatch & P_SHORTEST:
                if len(p0) < len(_buf) or not _buf:
                    _buf = p0
    return _buf

