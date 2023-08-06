# -*- coding: utf-8 -*-
"""The package 'namedtupledefs' provides a patched version of *collections.namedtuple* 
with field defaults for *namedtuple*.

This package provides the syntax release *Python3*.
"""

#
# Original Code: Copyright (c) 2001-2018 Python Software Foundation. All rights reserved.
# Original License: PSF LICENSE AGREEMENT FOR PYTHON
# Patches: Copyright (c) 2019 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez. 
#          All rights reserved.
# Patches License: Artistic-License-2.0 + Forced-Fairplay-Constraints
#         Exception for the public integration into the standard library *collections* 
#         by the PSF, than for the integrated public patches: 
#              PSF LICENSE AGREEMENT FOR PYTHON.  
#
# Platform: Python-2
#   For the Python2 refer to the package namedtupledefs2.
#   
#   This package requires the *exec* statement/function, due to it's size it is
#   separated into two variants instead of using shared code.  
#
# Changes:
# 
# 0. The template for the created tuple class:
#    1. Added member variable _fielddefaults - for documentation and online use.
#    2. Changed the call parameters of __new__ to {new_args} - with default values.
#       This is the only and one actual relevant code change of the created tuple class.
# 
# 1. The fabric code:
#    1. Added documentation in functions doc-string. 
#    2. Added code block for the creation of the call argument string of '__new__'.
#    3. Added 'new_args' and '_fielddefaults' to the format parameters of
#       the class template.  
#          


import sys as _sys

from operator import itemgetter as _itemgetter
from keyword import iskeyword as _iskeyword

from collections import OrderedDict


__author__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (c) 2001-2018 Python Software Foundation. + " \
                "Copyright (C) 2019 Arno-Can Uestuensoez" \
                "@Ingenieurbuero Arno-Can Uestuensoez" \
                "All rights reserved."
__version__ = '0.1.1'
__uuid__ = "19683f50-48f2-4e1e-953f-640455e97340"

__docformat__ = "restructuredtext en"


################################################################################
### namedtuple
################################################################################

class NamedTupleError(Exception):
    pass


_class_template = """\
from builtins import property as _property, tuple as _tuple
from operator import itemgetter as _itemgetter
from collections import OrderedDict
from copy import copy

import namedtupledefs

class {typename}(tuple):
    '''{typename}({arg_list}) 
    with optional default values fielddefaults={field_defaults} => {typename}({new_args})'''

    __slots__ = ()

    _fields = {field_names!r}
    _fielddefaults = {field_defaults}

    def __new__(_cls, {new_args}):
        'Create new instance of {typename}({new_args})'
        return _tuple.__new__(_cls, ({arg_list}))

    @classmethod
    def _make(cls, iterable, new=tuple.__new__, len=len):
        'Make a new {typename} object from a sequence or iterable'
        result = new(cls, iterable)
        if len(result) != {num_fields:d}:
            raise TypeError('Expected {num_fields:d} arguments, got %d' % len(result))
        return result

    def _replace(_self, **kwds):
        'Return a new {typename} object replacing specified fields with new values'
        result = _self._make(map(kwds.pop, {field_names!r}, _self))
        if kwds:
            raise ValueError('Got unexpected field names: %r' % list(kwds))
        return result

    def __repr__(self):
        'Return a nicely formatted representation string'
        return self.__class__.__name__ + '({repr_fmt})' % self

    def _asdict(self):
        'Return a new OrderedDict which maps field names to their values.'
        return OrderedDict(zip(self._fields, self))

    def __getnewargs__(self):
        'Return self as a plain tuple.  Used by copy and pickle. Does not need the fielddefaults.'
        return tuple(self)

    __dict__ = _property(_asdict)

    def __getstate__(self):
        'Exclude the OrderedDict from pickling'
        pass

    def _merge(self, typename, *others):
        'Add multiple "namedtuple" resulting in a new "namedtuple" of class "typename".'
        _fn = copy(self._fields)
        _fd = copy(self._fielddefaults)  # spare None-check
        _t = ()
        for o in others:
            if not hasattr(o, '_fields') or not hasattr(o, '_fielddefaults'):
                raise ValueError(
                    "supports only classes from: namedtupledefs.namedtuple " + str(o))
            # check for non-scattered function style default values
            if _fd and (not o._fielddefaults or len(o._fielddefaults) != len(o._fields)):
                raise ValueError(
                    "default values are right bound and must not be scattered: %s / %s"
                    %(str(o._fields), str(o._fielddefaults))
                    )
            _fn += o._fields
            _fd += o._fielddefaults
            _t  += o  # want the tuple values without fiddling
        # resulting names have to be valid - the tuple will check finally 
        tp = namedtupledefs.namedtuple(typename, _fn, fielddefaults=_fd)
        return tp(*tuple.__add__(self, _t))

{field_defs}
"""

_repr_template = '{name}=%r'
 
_field_template = '''\
    {name} = _property(_itemgetter({index:d}), doc='Alias for field number {index:d}')    
'''

def namedtuple(typename, field_names, *, verbose=False, rename=False, module=None, **kargs):

    """Returns a new subclass of tuple with named fields.

    >>> Point = namedtuple('Point', ['x', 'y'])
    >>> Point.__doc__                   # docstring for the new class
    'Point(x, y)'
    >>> p = Point(11, y=22)             # instantiate with positional args or keywords
    >>> p[0] + p[1]                     # indexable like a plain tuple
    33
    >>> x, y = p                        # unpack like a regular tuple
    >>> x, y
    (11, 22)
    >>> p.x + p.y                       # fields also accessible by name
    33
    >>> d = p._asdict()                 # convert to a dictionary
    >>> d['x']
    11
    >>> Point(**d)                      # convert from a dictionary
    Point(x=11, y=22)
    >>> p._replace(x=100)               # _replace() is like str.replace() but targets named fields
    Point(x=100, y=22)

    Provides optional default values with similar behaviour to function parameters.
    
    >>> Point = namedtuple('Point', ['x', 'y', 'z'], fielddefaults=(22, 33))

    >>> Point.__doc__                   # docstring for the new class with defaults

    'Point(x, y, z)\n    with optional default values fielddefaults=(22, 33)'
    
    >>> Point(11)                       # instantiate with partial positional args or keywords
    Point(x=11, y=22, z=33)
    >>> Point(11, y=22)                 # instantiate with partial positional args or keywords
    Point(x=11, y=22, z=33)
    >>> p = Point(11, y=22)             # instantiate with positional args or keywords
    >>> p[0] + p[1] + p[2]              # indexable like a plain tuple
    66
    >>> x, y, z = p                     # unpack like a regular tuple
    >>> x, y, z
    (11, 22, 33)
    >>> p.x + p.y + p.z                 # fields also accessible by name
    66
    >>> d = p._asdict()                 # convert to a dictionary
    >>> d['z']
    33
    >>> Point(**d)                      # convert from a dictionary
    Point(x=11, y=22, z=33)
    >>> p._replace(x=100)               # _replace() is like str.replace() but targets named fields
    Point(x=100, y=22, z=33)
    >>> p._replace(z=100)               # _replace() works for fields with default values as well
    Point(x=11, y=22, z=100)

    """

    # Validate the field names.  At the user's option, either generate an error
    # message or automatically replace the field name with a valid name.
    if isinstance(field_names, str):
        field_names = field_names.replace(',', ' ').split()
    field_names = [str(x) for x in field_names]

    typename = str(typename)
    if rename:
        seen = set()
        for index, name in enumerate(field_names):
            if (not all(c.isalnum() or c=='_' for c in name)
                or _iskeyword(name)
                or not name
                or name[0].isdigit()
                or name.startswith('_')
                or name in seen):
                field_names[index] = '_%d' % index
            seen.add(name)
    for name in [typename] + field_names:
        if type(name) != str:
            raise TypeError('Type names and field names must be strings')
        if not all(c.isalnum() or c=='_' for c in name):
            raise ValueError('Type names and field names can only contain '
                             'alphanumeric characters and underscores: %r' % name)
        if _iskeyword(name):
            raise ValueError('Type names and field names cannot be a '
                             'keyword: %r' % name)
        if name[0].isdigit():
            raise ValueError('Type names and field names cannot start with '
                             'a number: %r' % name)
    seen = set()
    for name in field_names:
        if name.startswith('_') and not rename:
            raise ValueError('Field names cannot start with an underscore: '
                             '%r' % name)
        if name in seen:
            raise ValueError('Encountered duplicate field name: %r' % name)
        seen.add(name)

    # add default values for the '__new__' call and store default values for eventual
    # processing in the member variable '_fielddefaults'
    _field_defaults = kargs.get('fielddefaults')
    _new_args = field_names[:]
    if _field_defaults:
        if len(_field_defaults) > len(field_names):
            raise ValueError('More defaults than fields: ' + str(len(_field_defaults) - len(field_names)))
        if not isinstance(_field_defaults, (tuple, list)):
            raise TypeError("Requires a 'tuple' or 'list' for 'fielddefaults'.")
        field_defaults = str(tuple(_field_defaults))  # strip off derived classes
        _new_args = field_names[:]
        for d in range(len(_field_defaults), 0, -1):
            if isinstance(_field_defaults[-1 * d], str):
                _new_args[-1 * d] += '="' + str(_field_defaults[-1 * d] + '"') 
            else:
                _new_args[-1 * d] += '=' + str(_field_defaults[-1 * d]) 
    else:
        field_defaults = None

    # Fill-in the class template
    class_definition = _class_template.format(
        typename = typename,
        field_names = tuple(field_names),
        field_defaults = field_defaults,
        new_args = repr(tuple(_new_args)).replace("'", "")[1:-1],
        num_fields = len(field_names),
        arg_list = repr(tuple(field_names)).replace("'", "")[1:-1],
        repr_fmt = ', '.join(_repr_template.format(name=name)
                             for name in field_names),
        field_defs = '\n'.join(_field_template.format(index=index, name=name)
                               for index, name in enumerate(field_names))
    )
    if verbose:
        print(class_definition)

    # Execute the template string in a temporary namespace and support
    # tracing utilities by setting a value for frame.f_globals['__name__']
    namespace = dict(__name__='namedtuple_%s' % typename)

    try:
        exec(class_definition, namespace)
    except SyntaxError as e:
        raise SyntaxError(e.message + ':\n' + class_definition)
    result = namespace[typename]

    result._source = class_definition
    if verbose:
        print(result._source)

    # For pickling to work, the __module__ variable needs to be set to the frame
    # where the named tuple is created.  Bypass this step in environments where
    # sys._getframe is not defined (Jython for example) or sys._getframe is not
    # defined for arguments greater than 0 (IronPython).
    if module is None:
        try:
            module = _sys._getframe(1).f_globals.get('__name__', '__main__')
        except (AttributeError, ValueError):
            pass
    if module is not None:
        result.__module__ = module

    return result

