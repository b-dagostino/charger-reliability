from enum import Enum    

class MultiValueEnum(Enum):
    # Support multi-value enums
    # From https://stackoverflow.com/a/43210118
    def __new__(cls, *values):
        obj = object.__new__(cls)
        # first value is canonical value
        obj._value_ = values[0]
        for other_value in values[1:]:
            cls._value2member_map_[other_value] = obj
        obj._all_values = values
        return obj

    # Support multi-value enums
    # From https://stackoverflow.com/a/43210118
    def __repr__(self):
        return "<%s.%s: %s>" % (
            self.__class__.__name__,
            self._name_,
            ", ".join([repr(v) for v in self._all_values]),
        )