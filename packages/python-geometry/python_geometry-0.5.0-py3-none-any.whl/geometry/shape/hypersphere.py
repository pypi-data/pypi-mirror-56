"""Hypersphere class."""
from warnings import warn

from attr import attrib, attrs
from numpy import asanyarray, cos, isclose, linspace, newaxis, pi
from numpy import round as round_
from numpy import sin, sqrt, stack
from numpy.linalg import norm
from scipy.special import gamma

from ..config import ISCLOSE_KWARGS
from .base import IsConvexMixin, Shape
from .iso_hyperrectangle import IsoHyperrectangle


@attrs
class Hypersphere(IsConvexMixin, Shape):
    """Class representing a hypersphere."""

    center = attrib(converter=asanyarray)
    radius = attrib()

    @property
    def number_of_dimensions(self):
        """Return the number of dimensions."""
        return len(self.center)

    def has_on_boundary(self, point, isclose_kwargs=None):
        """Return whether given point is on the boundary."""
        isclose_kwargs = isclose_kwargs or ISCLOSE_KWARGS
        if __debug__:
            factor = 0.001
            if ISCLOSE_KWARGS["atol"] > factor * self.radius:
                warn(
                    (
                        "Absolute tolerance configuration (= {atol:.4e}) is larger "
                        "than {factor} times the radius of the hypersphere "
                        "({factor}*{radius:.4e} = {reduced_radius:.4e})"
                    ).format(
                        factor=factor,
                        atol=ISCLOSE_KWARGS["atol"],
                        radius=self.radius,
                        reduced_radius=factor * self.radius,
                    )
                )
        return isclose(
            norm(point - self.center, axis=-1), self.radius, **isclose_kwargs
        )

    def _has_on_bounded_side(self, point, isclose_kwargs=None):
        """Return whether given point is on the bounded side."""
        return norm(point - self.center, axis=-1) < self.radius

    @property
    def area(self):
        """Return the area."""
        number_of_surface_dimensions = self.number_of_dimensions - 1
        return (
            2
            * pi ** ((number_of_surface_dimensions + 1) / 2)
            / gamma((number_of_surface_dimensions + 1) / 2)
            * self.radius ** number_of_surface_dimensions
        )

    @property
    def volume(self):
        """Return the volume."""
        number_of_dimensions = self.number_of_dimensions
        return (
            pi ** (number_of_dimensions / 2)
            / gamma(number_of_dimensions / 2 + 1)
            * self.radius ** number_of_dimensions
        )

    def points_on_surface(self, area_per_point):
        """Return equally spaced points on the surface."""
        if self.number_of_dimensions == 3:
            number_of_points = round_(self.area / area_per_point).astype(int)
            points_on_unit_sphere = _get_equally_spaced_points_on_unit_sphere_3d(
                number_of_points
            )
            points = self.radius * points_on_unit_sphere + self.center[newaxis, :]
        else:
            raise NotImplementedError(
                "Points on edges is not implemented for {} dimensions.".format(
                    self.number_of_dimensions
                )
            )
        return points

    @property
    def bounding_box(self):
        """Return the bounding box of the shape."""
        bounding_box = IsoHyperrectangle(
            min=self.center - self.radius, max=self.center + self.radius
        )
        return bounding_box


def _get_equally_spaced_points_on_unit_sphere_3d(number_of_points):
    """Return approximately equally spaced points on the unit sphere."""
    longitudes = linspace(
        0, number_of_points * pi * (3 - sqrt(5)), number_of_points, endpoint=False
    )
    z_coordinates = linspace(
        -1 + 1 / number_of_points, 1 - 1 / number_of_points, number_of_points
    )
    radii_for_z_coordinate = sqrt(1 - z_coordinates ** 2)
    points = stack(
        (
            radii_for_z_coordinate * cos(longitudes),
            radii_for_z_coordinate * sin(longitudes),
            z_coordinates,
        ),
        axis=-1,
    )
    return points
