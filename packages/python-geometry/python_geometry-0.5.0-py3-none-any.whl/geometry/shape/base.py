"""Basic components for shapes."""

from abc import ABC, abstractmethod

from attr import attrs
from numpy import logical_not, where
from scipy.spatial import ConvexHull

from ..triangulation import Triangulation


@attrs
class Shape(ABC):
    """Base class defining the interface of a shape."""

    @property
    @abstractmethod
    def number_of_dimensions(self):
        """Return the number of dimensions."""
        ...

    @abstractmethod
    def has_on_boundary(self, point, isclose_kwargs=None):
        """Return whether given point is on the boundary."""
        ...

    @abstractmethod
    def _has_on_bounded_side(self, point, isclose_kwargs=None):
        """Return whether given point is on the bounded side."""
        ...

    def has_on_bounded_side(self, point, isclose_kwargs=None):
        """Return whether given point is on the bounded side."""
        return where(
            self.has_on_boundary(point=point, isclose_kwargs=isclose_kwargs),
            False,
            self._has_on_bounded_side(point=point, isclose_kwargs=isclose_kwargs),
        )

    def has_on_unbounded_side(self, point, isclose_kwargs=None):
        """Return whether given point is on the unbounded side."""
        return where(
            self.has_on_boundary(point=point, isclose_kwargs=isclose_kwargs),
            False,
            logical_not(
                self.has_on_bounded_side(point=point, isclose_kwargs=isclose_kwargs)
            ),
        )


@attrs
class IsConvexMixin(ABC):
    """Base class defining the interface of a shape."""

    @abstractmethod
    def points_on_surface(self, area_per_point):
        """Return equally spaced points on the surface."""
        ...

    def get_surface_triangulation(self, area_per_vertex):
        """Return a triangulation of the surface."""
        points_on_surface = self.points_on_surface(area_per_point=area_per_vertex)
        surface_triangulation = Triangulation.from_scipy_spatial_convex_hull(
            ConvexHull(points_on_surface)
        )
        return surface_triangulation
