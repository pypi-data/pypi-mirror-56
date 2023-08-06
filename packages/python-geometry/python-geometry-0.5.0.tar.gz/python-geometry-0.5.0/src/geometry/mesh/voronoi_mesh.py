"""Mesh based on Voronoi tessellation."""

from attr import attrib, attrs
from numpy import any as any_
from numpy import (
    asanyarray,
    atleast_2d,
    concatenate,
    empty,
    iinfo,
    isfinite,
    isscalar,
    logical_and,
    transpose,
)
from scipy.spatial import ConvexHull, Delaunay, Voronoi
from scipy.spatial.ckdtree import cKDTree

from ..intersections import line_segment_triangle_intersection
from ..shape.convex_polytope import ConvexPolytope
from ..shape.iso_hyperrectangle import IsoHyperrectangle
from ..shape.utlities import get_points_in_or_on_shape
from ..triangulation import Triangulation
from .base import Mesh


def _seeds_converter(seeds):
    if isscalar(seeds[0]):
        converted_seeds = transpose(atleast_2d(seeds))
    else:
        converted_seeds = asanyarray(seeds)
    return converted_seeds


@attrs
class VoronoiMesh(Mesh):
    """Mesh based on a Voronoi tessellation."""

    _seeds = attrib(converter=_seeds_converter)
    _shape = attrib(default=None)
    _kdtree = attrib(init=False, repr=False, default=None)
    _voronoi = attrib(init=False, repr=False, default=None)
    _delaunay = attrib(init=False, repr=False, default=None)
    _cell_shapes = attrib(init=False, repr=False, default=None)
    _cell_volumes = attrib(init=False, repr=False, default=None)

    def __attrs_post_init__(self):
        if self._shape and any_(self._shape.has_on_unbounded_side(self.seeds)):
            raise ValueError("Seeds must be contained in the shape.")

    @property
    def seeds(self):
        """Return the seeds of the Voronoi mesh."""
        return self._seeds

    @property
    def shape(self):
        """Return the shape of the mesh."""
        return self._shape

    @property
    def kdtree(self):
        """Return the k-d tree of the seeds."""
        if self._kdtree is None:
            self._kdtree = cKDTree(self.seeds)
        return self._kdtree

    @property
    def voronoi(self):
        """Return the Voronoi diagram of the seeds."""
        if self._voronoi is None:
            self._voronoi = Voronoi(points=self.seeds)
        return self._voronoi

    @property
    def delaunay(self):
        """Return the Delaunay triangulation of the seeds."""
        if self._delaunay is None:
            self._delaunay = Delaunay(points=self.seeds)
        return self._delaunay

    @property
    def number_of_dimensions(self):
        """Return the number of spatial dimensions of the mesh."""
        return self.seeds.shape[1]

    @property
    def number_of_cells(self):
        """Return the number of cells that make up the mesh."""
        return len(self.seeds)

    def get_cell_id_around_point(self, point):
        """Return the ID of the cell containing the given `point`."""
        point = asanyarray(point)
        result_shape = (
            point.shape if self.number_of_dimensions == 1 else point.shape[:-1]
        )
        point = atleast_2d(point)
        if self.number_of_dimensions == 1:
            point = transpose(point)
        cell_id = self.kdtree.query(point)[1]

        if self._shape:
            cell_id[self.shape.has_on_unbounded_side(point)] = iinfo(cell_id.dtype).min

        cell_id = cell_id.reshape(result_shape)
        return cell_id

    def is_valid_cell_id(self, cell_id):
        """Return whether the given `cell_id` is valid for this mesh."""
        return logical_and(cell_id >= 0, cell_id < self.number_of_cells)

    def _get_surrounding_voronoi_diagram(self):
        bounding_box = self.shape.bounding_box
        bounding_box_diagonal = bounding_box.max - bounding_box.min
        outer_box = IsoHyperrectangle(
            min=bounding_box.min - bounding_box_diagonal,
            max=bounding_box.max + bounding_box_diagonal,
        )
        temporary_seeds = concatenate((self.seeds, outer_box.vertices), axis=0)
        return Voronoi(temporary_seeds)

    def _get_cell_shapes(self, volume_per_vertex):
        surrounding_voronoi = self._get_surrounding_voronoi_diagram()

        regions_triangulations = []
        for region_id in surrounding_voronoi.point_region[: self.number_of_cells]:
            region_vertices = surrounding_voronoi.vertices[
                surrounding_voronoi.regions[region_id]
            ]
            regions_triangulations.append(
                Triangulation.from_scipy_spatial_convex_hull(
                    ConvexHull(region_vertices)
                )
            )
        shape_surface_triangulation = self.shape.get_surface_triangulation(
            area_per_vertex=volume_per_vertex ** (2 / 3)
        )
        shape_surface_triangulation_vertices_cell_ids = self.get_cell_id_around_point(
            shape_surface_triangulation.vertices
        )

        cell_shapes = empty(self.number_of_cells, dtype=object)
        for i in range(self.number_of_cells):
            points_to_consider = []

            # vertices of the Voronoi cell that are in the surrounding shape
            region_triangulation_vertices = regions_triangulations[i].vertices
            relevant_region_triangulation_vertices = get_points_in_or_on_shape(
                self.shape, region_triangulation_vertices
            )
            points_to_consider.append(relevant_region_triangulation_vertices)

            if not len(relevant_region_triangulation_vertices) == len(
                region_triangulation_vertices
            ):
                # vertices of the triangulation of the surrounding shape
                points_to_consider.append(
                    shape_surface_triangulation.vertices[
                        shape_surface_triangulation_vertices_cell_ids == i
                    ]
                )

                # edges of the Voronoi region triangulation that intersect with the
                # triangles of the surface triangulation
                intersections = line_segment_triangle_intersection(
                    regions_triangulations[i].edges, shape_surface_triangulation.cells
                )
                points_to_consider.append(
                    intersections[any_(isfinite(intersections), axis=-1)]
                )

                # edges of the surface triangulation that intersect with the
                # triangles of the Voronoi region triangulation
                intersections = line_segment_triangle_intersection(
                    shape_surface_triangulation.edges, regions_triangulations[i].cells
                )
                points_to_consider.append(
                    intersections[any_(isfinite(intersections), axis=-1)]
                )

            cell_shapes[i] = ConvexPolytope.from_points(
                points=concatenate(points_to_consider, axis=0)
            )
        return cell_shapes

    @property
    def cell_shapes(self):
        """Return an array containing the cell shapes."""
        if self._cell_shapes is None:

            if self.shape is None:
                raise ValueError(
                    "A shape is required for the determination of cell shapes."
                )

            volume_per_vertex = self.shape.volume / len(self.seeds) / 100
            self._cell_shapes = self._get_cell_shapes(
                volume_per_vertex=volume_per_vertex
            )

        return self._cell_shapes

    @property
    def cell_volumes(self):
        """Return an array containing the cell volumes."""
        if self._cell_volumes is None:
            cell_volumes = empty(self.number_of_cells, dtype=float)
            for i, cell_shape in enumerate(self.cell_shapes):
                cell_volumes[i] = cell_shape.volume
            self._cell_volumes = cell_volumes
        return self._cell_volumes
