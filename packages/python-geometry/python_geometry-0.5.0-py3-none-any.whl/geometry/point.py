"""Implementation of a point."""
from attr import attrib, attrs
from numpy import all as all_
from numpy import asarray, isclose, number, subtract

from .validators import SubDTypeValidator
from .vector import Vector


@attrs(cmp=False)
class Point:
    """A point."""

    _point = attrib(converter=asarray, validator=SubDTypeValidator(number))

    def __array__(self):
        return self._point

    def __eq__(self, other):
        if isinstance(other, Point):
            return all_(isclose(self, other), axis=-1)
        return False

    def __sub__(self, other):
        if isinstance(other, Point):
            return Vector(subtract(self, other))

        return NotImplemented
