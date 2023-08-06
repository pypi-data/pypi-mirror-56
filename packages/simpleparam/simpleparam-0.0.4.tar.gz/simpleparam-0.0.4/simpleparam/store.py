"""General class for storing parameters"""
PROTECTED = ["_name"]
N_PROTECTED = len(PROTECTED)


class ParameterStore(object):
    """Parameter store"""

    def __init__(self, name="ParameterStore"):
        """Parameter store

        Parameters
        ----------
        name : str, optional
            name of the parameters store, by default "ParameterStore"
        """

        self._name = name

    def __setattr__(self, name, val):
        if name in self.__dict__:
            if hasattr(self.__dict__[name], "value"):
                if hasattr(self.__dict__[name], "constant") and self.__dict__[name].constant:
                    raise ValueError("Parameter `%s` cannot be modified" % name)
                self.__dict__[name].value = val
            else:
                self.__dict__[name] = val
        else:
            self.__dict__[name] = val

    def __repr__(self):
        return "{}(count={})".format(self._name, len(self.__dict__) - N_PROTECTED)

    def __str__(self):
        """Return a short representation of the name and class of this object."""
        return "<{} {}>".format(self.__class__.__name__, self._name)

    def __iter__(self):
        return iter(self.__dict__)

    def export_as_dict(self):
        """Exports current instance as dictionary"""
        _export = dict()

        for name, parameter in self.__dict__.items():
            # ignore reserved names
            if name in PROTECTED:
                continue

            # a typical config might have some values which are not actually params, those cannot be exported as JSON
            if not hasattr(parameter, "saveable"):
                continue

            # only export saveable objects
            if parameter.saveable:
                # base attributes of all parameters
                _export[name] = dict(
                    name=parameter.name,
                    value=parameter.value,
                    doc=parameter.doc,
                    kind=parameter.kind,
                    allow_None=parameter.allow_None,
                )
                # kind-specific attributes
                if parameter.kind in ["Number", "Integer", "Range"]:
                    _export[name].update(
                        dict(
                            auto_bound=parameter.auto_bound,
                            softbounds=parameter.softbounds,
                            hardbounds=parameter.hardbounds,
                            inclusive_bounds=parameter.inclusive_bounds,
                            step=parameter.step,
                            allow_None=parameter.allow_None,
                        )
                    )
                elif parameter.kind in ["String"]:
                    _export[name].update(dict(allow_any=parameter.allow_any, regex=parameter.regex))
                elif parameter.kind in ["Option", "Choice"]:
                    _export[name].update(dict(choices=parameter.choices))
                elif parameter.kind in ["Color"]:
                    _export[name].pop("allow_None")
                elif parameter.kind in ["List"]:
                    _export[name].update(dict(hardbounds=parameter.hardbounds))

        # return data
        return _export

    def load_from_dict(self, dict_obj, ignored_attributes=None, allowed_attributes=None):
        """Restore values from dictionary object with setting some restrictions

        Parameters
        ----------
        dict_obj : dict
            dictionary containing parameters and their individual attributes, usually read by reading configuration file
        ignored_attributes : list, optional
            list of attributes which should be ignored (e.g. you might want to preserve 'doc' or 'bounds'),
            by default None
        allowed_attributes : list, optional
            list of attributes which should be set (while ignoring others),
            by default None

        Raises
        ------
        ValueError
            Raised if both 'ignored_attributes' and 'allowed_attributes' are set
        """

        def check_allowed_attribute(attr_name):
            """Checks whether attribute is in the allowed list

            Parameters
            ----------
            attr_name : str
                name of the attribute to be checked

            Returns
            -------
            bool
                flag to either allow or not setting of the attribute
            """
            if allowed_attributes:
                if attr_name not in allowed_attributes:
                    return False
            return True

        def check_ignored_attribute(attr_name):
            """Checks whether attribute is in the ignore list

            Parameters
            ----------
            attr_name : str
                name of the attribute to be checked

            Returns
            -------
            bool
                flag to either allow or not setting of the attribute
            """
            if ignored_attributes:
                if attr_name in ignored_attributes:
                    return False
            return True

        if ignored_attributes is None or not isinstance(ignored_attributes, list):
            ignored_attributes = []

        if allowed_attributes is None or not isinstance(allowed_attributes, list):
            allowed_attributes = []

        if ignored_attributes and allowed_attributes:
            raise ValueError("You should only set one of the 'ignored_attributes' or 'allowed_attributes'")

        for param, values in dict_obj.items():
            if param in PROTECTED:
                continue

            if param in self.__dict__:
                for attr_name, value in values.items():
                    # certain attributes can be protected
                    if not check_allowed_attribute(attr_name) or not check_ignored_attribute(attr_name):
                        continue
                    setattr(self.__dict__[param], attr_name, value)
