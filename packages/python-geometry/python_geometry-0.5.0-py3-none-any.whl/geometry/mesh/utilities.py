"""Utilities for working with meshes."""

from itertools import product

from numpy import all as all_
from numpy import asanyarray, atleast_2d, bincount, int64, linspace, ndim, newaxis
from numpy import round as round_
from numpy import zeros


def histogram(points, mesh, weights=None, density=False):
    """Return the histogram of the data for the cells of the given `mesh`."""
    cell_ids = mesh.get_cell_id_around_point(point=points)
    mask = mesh.is_valid_cell_id(cell_ids)
    cell_ids = cell_ids[mask]
    if weights is not None:
        weights = asanyarray(weights)[mask]
        hist_dtype = float if density else weights.dtype
        hist = zeros([mesh.number_of_cells] + list(weights.shape[1:]), dtype=hist_dtype)
        for indices in product(*[range(i) for i in hist.shape[1:]]):
            indices = tuple([...] + list(indices))
            hist[indices] = bincount(
                cell_ids, weights=weights[indices], minlength=mesh.number_of_cells
            )
    else:
        hist_dtype = float if density else int
        # pylint: disable=no-member
        hist = bincount(cell_ids, minlength=mesh.number_of_cells).astype(
            hist_dtype, copy=False
        )
        # pylint: enable=no-member

    if density:
        hist /= mesh.cell_volumes[tuple([slice(None)] + (hist.ndim - 1) * [newaxis])]

    return hist


def get_equally_spaced_bins(bounding_box, bin_size):
    """Return a list of bins with equal spacing within given `bounding_box`."""
    bounding_box = asanyarray(bounding_box)
    bin_size = asanyarray(bin_size)

    if not all_(bin_size > 0):
        raise ValueError("Only positive bin sizes allowed.")

    original_number_of_dimensions = bounding_box.ndim
    bounding_box = atleast_2d(bounding_box)
    if ndim(bin_size) == 0:
        bin_size = [bin_size] * len(bounding_box)
    if not len(bin_size) == len(bounding_box):
        raise ValueError(
            (
                "Number of dimensions of the bounding box {} and bin sizes {} "
                "is incompatible."
            ).format(len(bounding_box), len(bin_size))
        )
    bins = []
    for (minimum, maximum), bin_size_ in zip(bounding_box, bin_size):
        bins.append(
            linspace(
                minimum,
                maximum,
                max(round_((maximum - minimum) / bin_size_).astype(int64) + 1, 2),
            )
        )
    if original_number_of_dimensions == 1:
        bins = bins[0]
    return bins
