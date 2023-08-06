"""Implementation of a vector."""
from attr import attrib, attrs
from numpy import all as all_
from numpy import asarray, isclose, number

from .validators import SubDTypeValidator


@attrs(cmp=False)
class Vector:
    """A vector."""

    _vector = attrib(converter=asarray, validator=SubDTypeValidator(number))

    def __array__(self):
        return self._vector

    def __eq__(self, other):
        if isinstance(other, Vector):
            return all_(isclose(self, other), axis=-1)
        return False

    def __neg__(self):
        return Vector(-self._vector)
