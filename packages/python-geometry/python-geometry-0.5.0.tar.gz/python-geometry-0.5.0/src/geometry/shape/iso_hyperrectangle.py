"""Iso hyperrectangle class."""

from itertools import combinations, permutations, product

from attr import attrib, attrs
from numpy import all as all_
from numpy import any as any_
from numpy import (
    array,
    asanyarray,
    concatenate,
    isclose,
    logical_and,
    logical_or,
    maximum,
    meshgrid,
    minimum,
    newaxis,
    prod,
    sqrt,
    stack,
)
from numpy import sum as sum_
from numpy import zeros_like

from ..config import ISCLOSE_KWARGS
from ..core import get_equally_spaced_points
from .base import IsConvexMixin, Shape


@attrs
class IsoHyperrectangle(IsConvexMixin, Shape):
    """Class representing a iso hyperrectangle."""

    min = attrib(converter=asanyarray)
    max = attrib(converter=asanyarray)

    def __attrs_post_init__(self):
        if not self.min.shape == self.max.shape:
            raise ValueError("Min and max must have the same number of dimensions.")
        self.min, self.max = minimum(self.min, self.max), maximum(self.min, self.max)

    @property
    def number_of_dimensions(self):
        """Return the number of dimensions."""
        return len(self.min)

    def has_on_boundary(self, point, isclose_kwargs=None):
        """Return whether given point is on the boundary."""
        isclose_kwargs = isclose_kwargs or ISCLOSE_KWARGS
        return any_(
            logical_or(
                isclose(self.min, point, **isclose_kwargs),
                isclose(self.max, point, **isclose_kwargs),
            ),
            axis=-1,
        )

    def _has_on_bounded_side(self, point, isclose_kwargs=None):
        """Return whether given point is on the bounded side."""
        return all_(logical_and(self.min < point, point < self.max), axis=-1)

    @property
    def center(self):
        """Return the center."""
        return 0.5 * (self.min + self.max)

    @property
    def area(self):
        """Return the area."""
        edge_lengths = self.max - self.min
        area = 2 * sum_(
            prod(
                list(combinations(edge_lengths, self.number_of_dimensions - 1)), axis=-1
            )
        )
        return area

    @property
    def volume(self):
        """Return the volume."""
        edge_lengths = self.max - self.min
        return prod(edge_lengths)

    @property
    def vertices(self):
        """Return the vertices."""
        return asanyarray(list(product(*stack((self.min, self.max), axis=-1))))

    def points_on_surface(self, area_per_point):
        """Return equally spaced points on the surface."""
        average_point_distance = sqrt(area_per_point)
        coordinates = [
            get_equally_spaced_points(
                min_, max_, average_point_distance, minimum_number_of_points=2
            )
            for min_, max_ in zip(self.min, self.max)
        ]
        points = [[self.min]]
        for axis_to_leave_out in range(self.number_of_dimensions):
            meshgrid_args = []
            slices = []
            for axis in range(self.number_of_dimensions):
                if axis == axis_to_leave_out:
                    meshgrid_args.append(array([self.min[axis], self.max[axis]]))
                else:
                    meshgrid_args.append(coordinates[axis])

                if axis < axis_to_leave_out:
                    slices.append(slice(1, -1))
                else:
                    slices.append(slice(None))
            slices = tuple(slices)
            points_on_surface = stack(meshgrid(*meshgrid_args, indexing="ij"), axis=-1)[
                slices
            ].reshape((-1, 3))
            points.append(points_on_surface)
        points = concatenate(points, axis=0)
        return points

    def points_on_edges_spaced(self, average_point_distance):
        """Return points on the surface with an average distance."""
        coordinates = [
            get_equally_spaced_points(
                min_, max_, average_point_distance, minimum_number_of_points=2
            )
            for min_, max_ in zip(self.min, self.max)
        ]
        points = [self.vertices]
        for axes in permutations(range(self.number_of_dimensions)):
            current_point = self.min
            for axis in axes:
                axis_vector = zeros_like(current_point)
                # pylint: disable=unsupported-assignment-operation
                axis_vector[axis] = 1
                # pylint: enable=unsupported-assignment-operation
                # pylint: disable=invalid-sequence-index
                next_points = (
                    current_point[newaxis, :]
                    + (coordinates[axis][:, newaxis] - self.min[axis])
                    * axis_vector[newaxis, :]
                )
                # pylint: enable=invalid-sequence-index
                points.append(next_points[1:-1])
                current_point = next_points[-1]
        points = concatenate(points, axis=0)
        return points

    @property
    def bounding_box(self):
        """Return the bounding box of the shape."""
        bounding_box = IsoHyperrectangle(min=self.min, max=self.max)
        return bounding_box
