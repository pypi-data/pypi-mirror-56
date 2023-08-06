"""Convex polytope class."""

from attr import attrib, attrs
from numpy import copy
from scipy.spatial import ConvexHull


@attrs
class ConvexPolytope:
    """Class representing a convex polytope."""

    initial_vertices = attrib(converter=copy)
    _hull = attrib(init=False, repr=False, default=None)

    def __attrs_post_init__(self):
        self._hull = ConvexHull(points=self.initial_vertices)
        if not len(self._hull.vertices) == len(self.initial_vertices):
            raise ValueError(
                "Given unnecessary points for the construction of a convex polytope."
            )

    @classmethod
    def from_points(cls, points):
        """Generate a convex polytope from given points."""
        hull = ConvexHull(points=points)
        # pylint: disable=unsubscriptable-object
        return cls(initial_vertices=hull.points[hull.vertices])

    @property
    def points(self):
        """Return the points."""
        # pylint: disable=unsubscriptable-object
        return self._hull.points

    @property
    def vertices_ids(self):
        """Return ids of the vertices."""
        # pylint: disable=unsubscriptable-object
        return self._hull.vertices

    @property
    def vertices(self):
        """Return the vertices."""
        # pylint: disable=unsubscriptable-object
        return self._hull.points[self.vertices_ids]

    @property
    def facets_vertices_ids(self):
        """Return ids of the vertices of the facets."""
        # pylint: disable=no-member
        return self._hull.simplices

    @property
    def facets(self):
        """Return the facets."""
        # pylint: disable=unsubscriptable-object
        return self._hull.points[self.facets_vertices_ids]

    @property
    def neighbors_facets_ids(self):
        """Return the ids of the facets of the neighbors."""
        # pylint: disable=no-member
        return self._hull.neighbors

    @property
    def neighbors(self):
        """Return the neighbor facets."""
        return self.facets[self.neighbors_facets_ids]

    @property
    def area(self):
        """Return the area of the polytope."""
        # pylint: disable=no-member
        return self._hull.area

    @property
    def volume(self):
        """Return the volume of the polytope."""
        # pylint: disable=no-member
        return self._hull.volume
