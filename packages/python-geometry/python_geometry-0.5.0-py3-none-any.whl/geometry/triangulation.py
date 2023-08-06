"""Module for triangulations and helpers."""

from itertools import combinations

from attr import attrib, attrs
from numpy import asanyarray, empty, mean
from triangle import triangulate

from .core import get_normal_vector
from .transformations import OrthogonalTransformation


@attrs
class Triangulation:
    """Class representing a triangulation."""

    vertices = attrib(converter=asanyarray)
    cells_vertices_ids = attrib(converter=asanyarray)
    edges_vertices_ids = attrib(converter=asanyarray)

    @classmethod
    def from_scipy_spatial_convex_hull(cls, convex_hull):
        """Compute a triangulation based on given `convex_hull`."""
        vertex_id_to_new_id_map = {
            vertex_id: new_id for new_id, vertex_id in enumerate(convex_hull.vertices)
        }

        cells_vertices_ids = empty((len(convex_hull.simplices), 3), dtype=int)
        edges_vertices_ids = set()
        for i_simplex, simplex in enumerate(convex_hull.simplices):
            new_simplex_ids = [vertex_id_to_new_id_map[i] for i in simplex]
            cells_vertices_ids[i_simplex] = new_simplex_ids

            for edge_vertex_id_combination in combinations(new_simplex_ids, 2):
                new_id_combination = tuple(sorted(edge_vertex_id_combination))
                edges_vertices_ids.add(new_id_combination)
        edges_vertices_ids = asanyarray(sorted(edges_vertices_ids))

        triangulation = cls(
            vertices=convex_hull.points[convex_hull.vertices],
            cells_vertices_ids=cells_vertices_ids,
            edges_vertices_ids=edges_vertices_ids,
        )
        return triangulation

    @property
    def number_of_cells(self):
        """Return the number of cells."""
        return len(self.cells_vertices_ids)

    @property
    def cells(self):
        """Return the cell vertices."""
        return self.vertices[self.cells_vertices_ids]

    @property
    def number_of_edges(self):
        """Return the number of edges."""
        return len(self.edges_vertices_ids)

    @property
    def edges(self):
        """Return the edge vertices."""
        return self.vertices[self.edges_vertices_ids]


def triangulate_polygon(polygon, maximum_area=None, minimum_angle=None):
    """Return a triangulation of the given `polygon`."""
    polygon = asanyarray(polygon)
    if not polygon.ndim == 2:
        raise ValueError("Given polygon should be a sequence of vertices.")
    number_of_spatial_dimensions = polygon.shape[1]
    if number_of_spatial_dimensions == 2:
        triangulation = _triangulate_polygon_2d(
            polygon=polygon, maximum_area=maximum_area, minimum_angle=minimum_angle
        )
    elif number_of_spatial_dimensions == 3:
        triangulation = _triangulate_polygon_3d(
            polygon=polygon, maximum_area=maximum_area, minimum_angle=minimum_angle
        )
    else:
        raise NotImplementedError(
            (
                "Triangulation of polygons in {}-dimensional space is not implemented."
            ).format(number_of_spatial_dimensions)
        )
    return triangulation


def _triangulate_polygon_2d(polygon, maximum_area=None, minimum_angle=None):
    """Return a triangulation of the given two-dimensional `polygon`."""
    polygon = asanyarray(polygon)
    if not polygon.ndim == 2:
        raise ValueError("Given polygon should be a sequence of vertices.")
    if not polygon.shape[1] == 2:
        raise ValueError("Given polygon should be two-dimensional.")
    triangle_options = ""
    if minimum_angle is not None:
        triangle_options += (
            "q" if minimum_angle is True else "q{}".format(minimum_angle)
        )
    if maximum_area is not None:
        triangle_options += "a{}".format(maximum_area)
    triangulation = triangulate({"vertices": polygon}, opts=triangle_options)
    triangulation = Triangulation(
        vertices=triangulation["vertices"],
        cells_vertices_ids=triangulation["triangles"],
        edges_vertices_ids=triangulation["segments"],
    )
    return triangulation


def _triangulate_polygon_3d(polygon, maximum_area=None, minimum_angle=None):
    """Return a triangulation of the given three-dimensional `polygon`."""
    polygon = asanyarray(polygon)
    if not polygon.ndim == 2:
        raise ValueError("Given polygon should be a sequence of vertices.")
    if not polygon.shape[1] == 3:
        raise ValueError("Given polygon should be three-dimensional.")
    polygon_normal_vector = get_normal_vector(polygon, is_closed=True)
    transformation = OrthogonalTransformation(
        x=polygon[1] - polygon[0], z=polygon_normal_vector
    )
    polygon_in_plane = transformation.pullback(polygon)
    z_in_plane = mean(polygon_in_plane[:, 2])

    triangulation = _triangulate_polygon_2d(
        polygon_in_plane, maximum_area=maximum_area, minimum_angle=minimum_angle
    )

    triangulation_vertices = empty((len(triangulation.vertices), 3))
    triangulation_vertices[:, :2] = triangulation.vertices
    triangulation_vertices[:, 2] = z_in_plane
    triangulation.vertices = transformation.pushforward(triangulation_vertices)

    return triangulation
