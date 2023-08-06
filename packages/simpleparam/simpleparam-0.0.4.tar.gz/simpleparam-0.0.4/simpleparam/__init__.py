"""
Simplified version of the `param` library (https://param.pyviz.org/).

`simpleparam` tries to emulate the best features of `param` by providing a subset of availabel classes/objects while
making it slightly easier to use while also allowing easy expansion
"""
from __future__ import division

import copy
import operator
import re
import sys

from .store import ParameterStore  # noqa
from .utilities import get_occupied_slots
from .utilities import is_number

if sys.version_info[0] == 3:
    unicode = str

__all__ = ["Parameter", "Number", "Integer", "String", "Boolean", "Choice", "Option", "Color", "ParameterStore"]


class Parameter(object):
    """Base class for most of the other classes"""

    __slots__ = ["_value", "_kind", "name", "doc", "saveable", "allow_None", "constant"]

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "param")
        self.doc = kwargs.get("doc", "")
        self._value = kwargs.get("value", None)
        self._kind = kwargs.get("kind", "Parameter")
        self.saveable = self._validate_bool(kwargs.get("saveable", True))
        self.constant = self._validate_bool(kwargs.get("constant", False))
        self.allow_None = self._validate_bool(kwargs.get("allow_None", True))

    def __str__(self):
        return str(self.value)

    #         return "Parameter(name='{}', value={}, doc='{}')".format(self.name, self.value, self.doc)

    def __repr__(self):
        return repr(self.value)

    def __add__(self, other):
        return operator.add(self.value, other)

    def __sub__(self, other):
        return operator.sub(self.value, other)

    def __mul__(self, other):
        return operator.mul(self.value, other)

    def __div__(self, other):
        return operator.div(self.value, other)  # noqa

    def __truediv__(self, other):
        return operator.truediv(self.value, other)

    def __floordiv__(self, other):
        return operator.floordiv(self.value, other)

    def __mod__(self, other):
        return operator.mod(self.value, other)

    def __pow__(self, other):
        return operator.pow(self.value, other)

    def __lt__(self, other):
        return operator.lt(self.value, other)

    def __le__(self, other):
        return operator.le(self.value, other)

    def __eq__(self, other):
        return operator.eq(self.value, other)

    def __ne__(self, other):
        return operator.ne(self.value, other)

    def __ge__(self, other):
        return operator.ge(self.value, other)

    def __gt__(self, other):
        return operator.gt(self.value, other)

    def __neg__(self):
        return operator.neg(self.value)

    def __pos__(self):
        return operator.pos(self.value)

    def __abs__(self):
        return operator.abs(self.value)

    def __lshift__(self, other):
        return operator.lshift(self.value, other)

    def __rshift__(self, other):
        return operator.rshift(self.value, other)

    def __getstate__(self):
        """
        All Parameters have slots, not a dict, so we have to support
        pickle and deepcopy ourselves.
        """
        state = {}
        for slot in get_occupied_slots(self):
            state[slot] = getattr(self, slot)
        return state

    def __setstate__(self, state):
        # set values of __slots__ (instead of in non-existent __dict__)
        for (k, v) in state.items():
            setattr(self, k, v)

    def _validate(self, val):
        """Implements validation for the parameter"""
        return val

    def _validate_bool(self, val):
        """Ensure value is either True/False"""
        if val in [True, False]:
            return val
        raise ValueError("Value must be a Boolean")

    @property
    def value(self):
        """Get `value`"""
        return self._value

    @value.setter
    def value(self, value):
        """Set `value`"""
        self._value = self._validate(value)

    @property
    def kind(self):
        """Get `kind`"""
        return self._kind

    @kind.setter
    def kind(self, value):
        """Set `kind`"""
        self._kind = value


class Number(Parameter):
    """
    A Number (Real) class, with default value and soft- and hard-bounds

    Each `Number` has two sets of bounds, either `softbounds' or 'hardbounds'. As the names suggest,
    `hardbounds` will throw an exception if the the default value is set outside of the bounds (unless
    the `auto_bound` value is set to True). The default bounds are [None, None], meaning there are actually no
    hard bounds. One or both bounds can be set by specifying a value (e.g. hardbounds=[None,10]
    means there is no lower bound, and an upper bound of 10). Bounds are inclusive by default, but exclusivity
    can be specified for each bound by setting inclusive_bounds (e.g. inclusive_bounds=(True,False)
    specifies an exclusive upper bound).

    As a special case, if allow_None=True (which is true by default if the parameter has a default of
    None when declared) then a value of None is also allowed.

    ``softbounds`` are present to indicate the typical range of the parameter, but are not enforced.
    Setting the soft bounds allows, for instance, a GUI to know what values to display on sliders for the Number.

    Example of creating a Number::
    AB = Number(default=0.5, bounds=(None,10), softbounds=(0,1), doc='Distance from A to B.')
    """

    __slots__ = ["_softbounds", "_hardbounds", "inclusive_bounds", "auto_bound", "step"]

    def __init__(self, value, kind="Number", **kwargs):
        super(Number, self).__init__(value=value, kind=kind, **kwargs)

        self._softbounds = self._validate_bounds(kwargs.get("softbounds", None))
        self._hardbounds = self._validate_bounds(kwargs.get("hardbounds", None))
        self.auto_bound = self._validate_bool(kwargs.get("auto_bound", False))
        self.inclusive_bounds = kwargs.get("inclusive_bounds", [True, True])
        self.step = kwargs.get("step", None)

        self.value = self._validate(self._value)

    @property
    def softbounds(self):
        """Get `softbounds`"""
        return self._softbounds

    @softbounds.setter
    def softbounds(self, value):
        """Set `softbounds`"""
        self._softbounds = self._validate_bounds(value)

    @property
    def hardbounds(self):
        """Get `hardbounds`"""
        return self._hardbounds

    @hardbounds.setter
    def hardbounds(self, value):
        """Set `hardbounds`"""
        self._hardbounds = self._validate_bounds(value)

    def _validate(self, val):
        """
        Checks that the value is numeric and that it is within the hard
        bounds; if not, an exception is raised.
        """
        if self.allow_None and val is None:
            return val

        if not is_number(val):
            raise ValueError("Parameter '%s' only takes numeric values" % (self.name))

        if self.auto_bound:
            val = self.crop_to_bounds(val)

        self._check_bounds(val)
        return val

    def _validate_bounds(self, val):
        """Ensure bounds are correctly setup"""
        if val is None:
            return val

        if isinstance(val, tuple):
            val = list(val)

        if isinstance(val, list):
            if len(val) != 2:
                raise ValueError("Bounds must be either set to 'None' or contain 2 values")

        return val

    def _check_bounds(self, val):
        """Check bounds and if outside, thrown an exception"""

        if self.hardbounds is not None:
            vmin, vmax = self.hardbounds
            incmin, incmax = self.inclusive_bounds

            if vmax is not None:
                if incmax is True:
                    if not val <= vmax:
                        raise ValueError("Parameter '{}' must be at most {}".format(self.name, vmax))
                else:
                    if not val < vmax:
                        raise ValueError("Parameter '{}' must be less than {}".format(self.name, vmax))

            if vmin is not None:
                if incmin is True:
                    if not val >= vmin:
                        raise ValueError("Parameter '{}' must be at least {}".format(self.name, vmin))
                else:
                    if not val > vmin:
                        raise ValueError("Parameter '{}' must be greater than {}".format(self.name, vmin))

    def get_soft_bounds(self):
        """
        For each soft bound (upper and lower), if there is a defined bound (not equal to None)
        then it is returned, otherwise it defaults to the hard bound. The hard bound could still be None.
        """
        if self.hardbounds is None:
            hard_lower, hard_upper = (None, None)
        else:
            hard_lower, hard_upper = self.hardbounds

        if self.softbounds is None:
            soft_lower, soft_upper = (None, None)
        else:
            soft_lower, soft_upper = self.softbounds

        if soft_lower is None:
            lower = hard_lower
        else:
            lower = soft_lower

        if soft_upper is None:
            upper = hard_upper
        else:
            upper = soft_upper

        return [lower, upper]

    def crop_to_bounds(self, val):
        """
        Return the given value cropped to be within the hard bounds
        for this parameter.

        If a numeric value is passed in, check it is within the hard
        bounds. If it is larger than the high bound, return the high
        bound. If it's smaller, return the low bound. In either case, the
        returned value could be None.  If a non-numeric value is passed
        in, set to be the default value (which could be None).  In no
        case is an exception raised; all values are accepted.
        """
        # Currently, values outside the bounds are silently cropped to
        # be inside the bounds; it may be appropriate to add a warning
        # in such cases.
        if is_number(val):
            if self.hardbounds is None:
                return val
            vmin, vmax = self.hardbounds
            if vmin is not None:
                if val < vmin:
                    return vmin

            if vmax is not None:
                if val > vmax:
                    return vmax

        elif self.allow_None and val is None:
            return val

        else:
            # non-numeric value sent in: reverts to default value
            return self.value

        return val


class Integer(Number):
    """Numeric Parameter required to be an Integer"""

    __slots__ = []

    def __init__(self, value, kind="Integer", **kwargs):
        super(Integer, self).__init__(value=value, kind=kind, **kwargs)

        self.value = self._validate(self._value)

    def _validate(self, val):
        if self.allow_None and val is None:
            return

        if not isinstance(val, int):
            raise ValueError("Parameter '{}' must be an integer not '{}'".format(self.name, type(val)))

        if self.auto_bound:
            val = self.crop_to_bounds(val)

        self._check_bounds(val)

        return val


class Range(Number):
    """Numeric Parameter which can be either Number or Integer, however, must have two values"""

    __slots__ = []

    def __init__(self, value, kind="Range", **kwargs):
        super(Range, self).__init__(value=value, kind=kind, **kwargs)

        self.value = self._validate(self._value)

    def __getitem__(self, k):
        if isinstance(self.value, list):
            return operator.getitem(self.value, k)
        raise ValueError("Range parameter must be a list to be subscriptable")

    def _validate(self, val):
        """
        Checks that the value is numeric and that it is within the hard
        bounds; if not, an exception is raised.
        """
        if self.allow_None and val is None:
            return val

        if len(val) != 2:
            raise ValueError("Range parameter '%s' must have two values" % (self.name))

        if any([not is_number(_val) for _val in val]):
            raise ValueError("Parameter '%s' only takes numeric values" % (self.name))

        if self.auto_bound:
            val = [self.crop_to_bounds(_val) for _val in val]

        [self._check_bounds(_val) for _val in val]
        return val


class Boolean(Parameter):
    """Binary or tristate Boolean Parameter."""

    __slots__ = []

    def __init__(self, value, kind="Boolean", **kwargs):
        super(Boolean, self).__init__(value=value, kind=kind, **kwargs)

        self.value = self._validate(self._value)

    def __nonzero__(self):
        return self.value

    def __bool__(self):
        return self.value

    def _validate(self, val):
        """Checks to ensure the set value is a boolean or None"""
        if self.allow_None:
            if not isinstance(val, bool) and val is not None:
                if val in [0, 1]:
                    val = bool(val)
                else:
                    raise ValueError("Boolean '%s' only takes a Boolean value or None." % self.name)

            if val is not True and val is not False and val is not None:
                raise ValueError("Boolean '%s' must be True, False, or None." % self.name)
        else:
            if not isinstance(val, bool):
                if val in [0, 1]:
                    val = bool(val)
                else:
                    raise ValueError("Boolean '%s' only takes a Boolean value." % self.name)
        return val


class String(Parameter):
    """String Parameter"""

    __slots__ = ["allow_any", "regex"]

    def __init__(self, value, regex=None, kind="String", **kwargs):
        super(String, self).__init__(value=value, kind=kind, **kwargs)

        self.allow_any = kwargs.get("allow_any", False)
        self.regex = regex
        self.value = self._validate(self._value)

    def __contains__(self, other):
        return operator.contains(self.value, other)

    def __getitem__(self, k):
        return operator.getitem(self.value, k)

    def _validate(self, val):
        """
        Checks that the value is string-like
        """
        if self.allow_None and val is None:
            return val

        if self.allow_any:
            return str(val)

        if not isinstance(val, (str, unicode)):
            raise ValueError("Parameter '{}' only takes string values not '{}'".format(self.name, type(val)))

        if self.regex is not None and re.match(self.regex, val) is None:
            raise ValueError("String '{}': '{}' does not match regex '{}'.".format(self.name, val, self.regex))

        return val


class Color(Parameter):
    """Color parameter defined as a hex RGB string with an optional # prefix."""

    __slots__ = []

    def __init__(self, value=None, kind="Color", **kwargs):
        super(Color, self).__init__(value=value, allow_None=False, kind=kind, **kwargs)
        self.value = self._validate(value)

    def _validate(self, val):
        if not isinstance(val, (str, unicode)):
            raise ValueError("Color '%s' only takes a string value." % self.name)
        if not re.match("^#?(([0-9a-fA-F]{2}){3}|([0-9a-fA-F]){3})$", val):
            raise ValueError("Color '%s' only accepts valid RGB hex codes." % self.name)

        return val


class Option(Parameter):
    """Base class for `Choice` allowing specification of choices"""

    __slots__ = ["_choices"]

    def __init__(self, value=None, kind="Option", **kwargs):
        super(Option, self).__init__(value=value, kind=kind, **kwargs)
        self._choices = kwargs.get("choices", [])

    def __contains__(self, other):
        return operator.contains(self.value, other)

    def _validate(self, val):
        """Implements validation for the parameter"""
        if self.allow_None and val is None:
            return val

        if val in self.choices:
            return val
        raise ValueError("Value `{}` not in the provided choices: {}".format(val, self.choices))

    def _validate_choices(self, val):
        """Ensure choices are a list"""
        if not isinstance(val, list):
            raise ValueError("Choices must be a `list`")
        if hasattr(self, "value"):
            if self.value not in val:
                print("Value not in the choice list")
        return val

    @property
    def choices(self):
        """Get `choices`"""
        return self._choices

    @choices.setter
    def choices(self, value):
        """Set `choices`"""
        value = self._validate_choices(value)
        __ = self._validate(self.value)
        self._choices = value


class Choice(Option):
    """
    Choice class, allowing specifying list of choices and default  value
    """

    __slots__ = []

    def __init__(self, value, choices, kind="Choice", **kwargs):
        super(Choice, self).__init__(value=value, choices=choices, kind=kind, **kwargs)

        self._validate_choices(choices)
        self.value = self._validate(self._value)


class List(Parameter):

    __slots__ = ["_hardbounds"]

    def __init__(self, value=None, kind="List", **kwargs):
        super(List, self).__init__(value=value, kind=kind, **kwargs)
        self._hardbounds = self._validate_bounds(kwargs.get("hardbounds", None))
        self.value = self._validate(value)

    def __contains__(self, other):
        return operator.contains(self.value, other)

    def __getitem__(self, k):
        return operator.getitem(self.value, k)

    def __delitem__(self, k):
        _value = copy.deepcopy(self.value)
        operator.delitem(_value, k)
        self.value = self._validate(_value)

    def __setitem__(self, k, value):
        _value = copy.deepcopy(self.value)
        operator.setitem(_value, k, value)
        self.value = self._validate(_value)

    @property
    def hardbounds(self):
        """Get `hardbounds`"""
        return self._hardbounds

    @hardbounds.setter
    def hardbounds(self, value):
        """Set `hardbounds`"""
        self._hardbounds = self._validate_bounds(value)

    def _validate(self, val):
        """
        Checks that the list is of the right length and has the right contents.
        Otherwise, an exception is raised.
        """
        if self.allow_None and val is None:
            return

        if not isinstance(val, list):
            raise ValueError("List '%s' must be a list." % (self.name))

        self._check_bounds(val)
        return val

    def _validate_bounds(self, val):
        """Ensure bounds are correctly setup"""
        if val is None:
            return val

        if isinstance(val, tuple):
            val = list(val)

        if isinstance(val, list):
            if len(val) != 2:
                raise ValueError("Bounds must be either set to 'None' or contain 2 values")

        return val

    def _check_bounds(self, val):
        """Check bounds and if outside, thrown an exception"""

        if self.hardbounds is not None:
            min_length, max_length = self.hardbounds
            n_items = len(val)
            if min_length is not None and max_length is not None:
                if not (min_length <= n_items <= max_length):
                    raise ValueError(
                        "{}: list length must be between {} and {} (inclusive)".format(
                            self.name, min_length, max_length
                        )
                    )
            elif min_length is not None:
                if not min_length <= n_items:
                    raise ValueError("Parameter '{}' list length must be at least {}.".format(self.name, min_length))
            elif max_length is not None:
                if not n_items <= max_length:
                    raise ValueError("Parameter '{}' list length must be at most {}.".format(self.name, max_length))
