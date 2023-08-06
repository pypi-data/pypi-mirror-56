"""Working with ellipses."""
from attr import attrib, attrs
from numpy import asanyarray, cos, newaxis, pi, sin


@attrs
class Ellipse:
    """Parametrized ellipsis."""

    # pylint: disable=too-few-public-methods

    center = attrib(converter=asanyarray)
    semi_major_axis = attrib(converter=asanyarray)
    semi_minor_axis = attrib(converter=asanyarray)

    def __call__(self, evaluation_points):
        """Return the interpolated values at given evaluation points."""
        evaluation_points = asanyarray(evaluation_points)
        evaluation_angles = 2 * pi * evaluation_points
        vertices = (
            self.center[newaxis, :]
            + self.semi_major_axis[newaxis, :] * cos(evaluation_angles)[:, newaxis]
            + self.semi_minor_axis[newaxis, :] * sin(evaluation_angles)[:, newaxis]
        )
        return vertices
