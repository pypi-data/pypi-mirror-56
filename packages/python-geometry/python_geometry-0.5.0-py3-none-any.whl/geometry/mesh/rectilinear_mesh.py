"""Mesh based on rectilinear discretization."""

from functools import reduce

from attr import attrib, attrs
from numpy import all as all_
from numpy import (
    asanyarray,
    atleast_2d,
    diff,
    empty,
    iinfo,
    linspace,
    logical_and,
    logical_not,
    multiply,
    ndim,
    prod,
    ravel_multi_index,
    reshape,
    searchsorted,
    squeeze,
    stack,
    transpose,
    unravel_index,
    zeros,
)

from ..shape.iso_hyperrectangle import IsoHyperrectangle
from .base import Mesh
from .utilities import get_equally_spaced_bins


def _bins_converter(bins):
    try:
        len(bins[0])
    except TypeError:
        converted_bins = [asanyarray(bins)]
    else:
        converted_bins = [asanyarray(bin_) for bin_ in bins]
    return converted_bins


def _get_bin_volumes(bins):
    return reduce(multiply.outer, [diff(bin_) for bin_ in bins])


@attrs
class RectilinearMesh(Mesh):
    """Mesh based on rectilinear discretization."""

    bins = attrib(converter=_bins_converter)

    @classmethod
    def from_shape_and_number_of_voxels(cls, shape, number_of_voxels, *args, **kwargs):
        """Initialize rectilinear mesh from shape and number of voxels."""
        if not isinstance(shape, IsoHyperrectangle):
            raise ValueError(
                "Unable to make rectilinear mesh from shape of type {}".format(
                    type(shape)
                )
            )
        if ndim(number_of_voxels) == 0:
            number_of_voxels = [number_of_voxels] * shape.number_of_dimensions
        elif not len(number_of_voxels) == shape.number_of_dimensions:
            raise ValueError(
                "Mismatch in dimensions of shape (= {}) and voxels (= {}).".format(
                    shape.number_of_dimensions, len(number_of_voxels)
                )
            )

        bins = []
        for min_, max_, n_voxels in zip(shape.min, shape.max, number_of_voxels):
            bins.append(linspace(min_, max_, n_voxels + 1))
        return cls(*args, bins=bins, **kwargs)

    @classmethod
    def from_shape_and_voxel_size(cls, shape, voxel_size, *args, **kwargs):
        """Initialize rectilinear mesh from shape and voxel edge length."""
        if not isinstance(shape, IsoHyperrectangle):
            raise ValueError(
                "Unable to make rectilinear mesh from shape of type {}".format(
                    type(shape)
                )
            )
        bins = get_equally_spaced_bins(
            bounding_box=stack(
                [shape.bounding_box.min, shape.bounding_box.max], axis=-1
            ),
            bin_size=voxel_size,
        )
        return cls(*args, bins=bins, **kwargs)

    @property
    def number_of_dimensions(self):
        """Return the number of spatial dimensions of the mesh."""
        return len(self.bins)

    @property
    def number_of_cells(self):
        """Return the number of cells that make up the mesh."""
        return prod([len(bin_) - 1 for bin_ in self.bins])

    @property
    def _shape(self):
        """Return the shape of the rectilinear mesh."""
        return tuple(len(bin_) - 1 for bin_ in self.bins)

    def is_valid_cell_id(self, cell_id):
        """Return whether the given `cell_id` is valid for this mesh."""
        return logical_and(cell_id >= 0, cell_id < self.number_of_cells)

    def is_valid_cell_index_array(self, cell_index_array):
        """Return whether the given `cell_index_array` is valid for this mesh."""
        cell_index_array = atleast_2d(cell_index_array)
        if self.number_of_dimensions == 1 and cell_index_array.shape[0] == 1:
            cell_index_array = transpose(cell_index_array)
        return logical_and(
            all_(zeros(self.number_of_dimensions) <= cell_index_array, axis=-1),
            all_(cell_index_array < self._shape, axis=-1),
        )

    def cell_index_array_to_cell_id(
        self, cell_index_array, ravel_multi_index_mode="raise"
    ):
        """Return the cell ID for given `cell_index_array`."""
        if self.number_of_dimensions == 1:
            cell_index_array = atleast_2d(cell_index_array)
        else:
            cell_index_array = transpose(cell_index_array)
        cell_id = ravel_multi_index(
            cell_index_array, self._shape, mode=ravel_multi_index_mode
        )
        return cell_id

    def cell_id_to_cell_index_array(self, cell_id):
        """Return the cell index array for given `cell_id`."""
        cell_index_array = transpose(unravel_index(cell_id, self._shape))
        if self.number_of_dimensions == 1:
            cell_index_array = squeeze(cell_index_array)
        return cell_index_array

    def get_cell_id_around_point(self, point):
        """Return the ID of the cell containing the given `point`."""
        cell_index_array = self.get_cell_index_array_around_point(point=point)
        cell_id = self.cell_index_array_to_cell_id(
            cell_index_array=cell_index_array, ravel_multi_index_mode="wrap"
        )
        valid_cell_index_array = self.is_valid_cell_index_array(
            cell_index_array=cell_index_array
        )
        if ndim(cell_id) == 0:
            if not valid_cell_index_array:
                cell_id = iinfo(int).min
        else:
            cell_id[logical_not(valid_cell_index_array)] = iinfo(cell_id.dtype).min
        return cell_id

    def get_cell_index_array_around_point(self, point):
        """Return the cell index array of the cell containing the given `point`."""
        point = asanyarray(point)
        original_shape = point.shape
        point = atleast_2d(point)
        if self.number_of_dimensions == 1 and len(original_shape) == 1:
            point = transpose(point)
        if not point.shape[-1] == self.number_of_dimensions:
            raise ValueError(
                (
                    "Dimensions of given point(s) {point_dimensions} is not compatible "
                    "with dimensions of mesh {mesh_dimensions}."
                ).format(
                    point_dimensions=point.shape[-1],
                    mesh_dimensions=self.number_of_dimensions,
                )
            )
        cell_ids = empty(point.shape, dtype=int)
        for i in range(self.number_of_dimensions):
            cell_ids[:, i] = searchsorted(self.bins[i], point[:, i], side="right") - 1
            cell_ids[point[:, i] == self.bins[i][-1], i] -= 1

        cell_ids[logical_not(self.is_valid_cell_index_array(cell_ids))] = iinfo(
            cell_ids.dtype
        ).min
        return reshape(cell_ids, original_shape)

    @property
    def cell_volumes(self):
        """Return an array containing the cell volumes."""
        return _get_bin_volumes(self.bins).ravel()

    @property
    def shape(self):
        """Return the shape of the mesh."""
        return IsoHyperrectangle(
            min=[bin_[0] for bin_ in self.bins], max=[bin_[-1] for bin_ in self.bins]
        )

    def get_cell_center(self, cell_id):
        """Return the center of the cell with given `cell_id`."""
        cell_index_array = self.cell_id_to_cell_index_array(cell_id=cell_id)
        cell_center = empty(self.number_of_dimensions)
        for i, (cell_index, bin_) in enumerate(zip(cell_index_array, self.bins)):
            cell_center[i] = 0.5 * (bin_[cell_index] + bin_[cell_index + 1])
        return cell_center
