"""Validators for geometric objects."""
from attr import attrib, attrs
from numpy import issctype, issubdtype


def _validate_dtype(instance, attribute, value):
    """Validate the given dtype attribute."""
    if not issctype(value):
        raise ValueError(f"Invalid dtype: {value!r}")


@attrs
class SubDTypeValidator:
    """Validator that checks the dtype of an attribute."""

    dtype = attrib(validator=_validate_dtype)

    def __call__(self, instance, attribute, value):
        """Validate the dtype of the attribute."""
        if not issubdtype(value.dtype, self.dtype):
            raise ValueError(
                f"Given dtype {value.dtype} of {type(instance).__qualname__}."
                f"{attribute.name} is not subtype of {self.dtype!r}."
            )
