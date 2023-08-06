"""Utilities"""
import inspect
import numbers


def is_number(obj):
    """Check if value is a number"""
    if isinstance(obj, numbers.Number):
        return True
    # The extra check is for classes that behave like numbers, such as those
    # found in numpy, gmpy, etc.
    elif hasattr(obj, "__int__") and hasattr(obj, "__add__"):
        return True
    return False


def classlist(class_):
    """
    Return a list of the class hierarchy above (and including) the given class.

    Same as inspect.getmro(class_)[::-1]
    """
    return inspect.getmro(class_)[::-1]


def get_all_slots(class_):
    """
    Return a list of slot names for slots defined in class_ and its
    superclasses.
    """
    # A subclass's __slots__ attribute does not contain slots defined
    # in its superclass (the superclass' __slots__ end up as
    # attributes of the subclass).
    all_slots = []
    parent_param_classes = [c for c in classlist(class_)[1::]]
    for c in parent_param_classes:
        if hasattr(c, "__slots__"):
            all_slots += c.__slots__
    return all_slots


def get_occupied_slots(instance):
    """
    Return a list of slots for which values have been set.

    (While a slot might be defined, if a value for that slot hasn't
    been set, then it's an AttributeError to request the slot's
    value.)
    """
    return [slot for slot in get_all_slots(type(instance)) if hasattr(instance, slot)]


# CLS_MATCH = {"Integer": Integer, "Number": Number, "String": String,
#              "Choice": Choice, "Option": Option, "Boolean": Boolean, "Range": Range,
#              "Color": Color}


# def _validate_parameter(values):
#     """Validate and create parameter

#     Parameters
#     ----------
#     values : dict
#         dictionary containing standard Parameter values

#     Returns
#     -------
#     Parameter
#         Parameter object based on values defined in the `values` object
#     """

#     obj_cls = values.get("kind", None)
#     try:
#         return cls_match.get(obj_cls, None)
#     except ValueError:
#         return None
