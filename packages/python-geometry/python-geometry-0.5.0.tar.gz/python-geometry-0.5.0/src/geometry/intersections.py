"""Module for intersections and helpers."""

from functools import singledispatch
from warnings import warn

from numpy import NaN
from numpy import abs as abs_
from numpy import all as all_
from numpy import (
    argmax,
    argmin,
    asanyarray,
    cross,
    dot,
    empty_like,
    errstate,
    inf,
    isclose,
    isinf,
    isnan,
    logical_or,
    newaxis,
    pi,
    sqrt,
)
from numpy import sum as sum_
from numpy import unravel_index
from numpy.linalg import norm

from .config import ISCLOSE_KWARGS
from .core import get_angle_between_vectors
from .shape.hypersphere import Hypersphere


@singledispatch
def intersect_with_rays_from_inside(shape, origins, directions):
    """Return intersections of a shape with rays whose origin are inside."""
    raise NotImplementedError(
        "Intersecting shape with rays from inside is not implemented for type "
        "{}".format(type(shape))
    )


@intersect_with_rays_from_inside.register(Hypersphere)
def _(shape, origins, directions):
    """Return intersections of a hypersphere with rays whose origin are inside."""
    first_term = -2 * (sum_(directions * (origins - shape.center[newaxis, :]), axis=-1))

    sqrt_term = first_term ** 2 - 4 * norm(directions, axis=-1) ** 2 * (
        norm(origins - shape.center[newaxis, :], axis=-1) ** 2 - shape.radius ** 2
    )
    denominator = 2 * norm(directions, axis=-1) ** 2
    assert all_(sqrt_term >= 0)
    intersections = (
        origins
        + ((first_term + sqrt(sqrt_term)) / denominator)[:, newaxis] * directions
    )
    return intersections


def line_triangle_intersection_line_parameter(line, triangle):
    """Return the line parameter for the intersection of given `line` and `triangle`.

    Uses the Möller–Trumbore intersection algorithm.
    """
    line = asanyarray(line)
    triangle = asanyarray(triangle)
    assert line.shape[-2:] == (2, 3)
    assert triangle.shape[-2:] == (3, 3)

    line_index = tuple(
        [slice(None)] * len(line.shape[:-2])
        + [newaxis] * len(triangle.shape[:-2])
        + [slice(None)]
    )
    triangle_index = tuple(
        [newaxis] * len(line.shape[:-2])
        + [slice(None)] * len(triangle.shape[:-2])
        + [slice(None)]
    )

    parameter = _moeller_trumbore_intersection_algorithm(
        origin=line[..., 0, :][line_index],
        direction=line[..., 1, :][line_index],
        vertex_0=triangle[..., 0, :][triangle_index],
        vertex_1=triangle[..., 1, :][triangle_index],
        vertex_2=triangle[..., 2, :][triangle_index],
    )

    return parameter


def _check_parallel_consistency(a, direction, edge_0, edge_1, is_parallel_mask):
    # pylint: disable=too-many-locals, invalid-name
    a_abs = abs_(a)
    index_min = unravel_index(argmin(a_abs), a.shape)
    edge_index_min = tuple(
        min(index, other_index - 1)
        for index, other_index in zip(index_min, edge_0.shape)
    )
    direction_index_min = tuple(
        min(index, other_index - 1)
        for index, other_index in zip(index_min, direction.shape)
    )
    angle_min = abs(
        get_angle_between_vectors(
            cross(edge_0[edge_index_min], edge_1[edge_index_min]),
            direction[direction_index_min],
        )
        - 0.5 * pi
    )
    is_parallel_min = is_parallel_mask[index_min]

    index_max = unravel_index(argmax(a_abs), a.shape)
    edge_index_max = tuple(
        min(index, other_index - 1)
        for index, other_index in zip(index_max, edge_0.shape)
    )
    direction_index_max = tuple(
        min(index, other_index - 1)
        for index, other_index in zip(index_max, direction.shape)
    )
    angle_max = abs(
        get_angle_between_vectors(
            cross(edge_0[edge_index_max], edge_1[edge_index_max]),
            direction[direction_index_max],
        )
        - 0.5 * pi
    )
    is_parallel_max = is_parallel_mask[index_max]

    threshold = 0.01 / 180 * pi
    if angle_min < threshold and not is_parallel_min:
        warn(
            (
                "Potential parallels might incorrectly not be flagged as being "
                "parallel due to the absolute tolerance configuration being chosen "
                "too large. The smallest angle observed is {angle_min:.4e} radians "
                "which is beneath the parallel threshold {threshold:.4e} "
                "({threshold_degree} degrees). The value responsible for this is "
                "{a_min} which is compared to zero. The largest angle observed is "
                "{angle_max} radians which resulted in a value of {a_max} being "
                "compared to zero."
            ).format(
                angle_min=angle_min,
                threshold=threshold,
                threshold_degree=threshold / pi * 180,
                a_min=a[index_min],
                angle_max=angle_max,
                a_max=a[index_max],
            )
        )

    if angle_max > threshold and is_parallel_max:
        warn(
            (
                "Potential intersections might incorrectly be flagged as being "
                "parallel incorrectly due to the absolute tolerance configuration "
                "being chosen too small. The largest angle observed is {angle_max} "
                "radians which is above the parallel threshold {threshold} "
                "({threshold_degree} degrees). The value responsible for this is "
                "{a_max} which is compared to zero. The smallest angle observed is "
                "{angle_min} radians which resulted in a value of {a_min} being "
                "compared to zero."
            ).format(
                angle_min=angle_min,
                threshold=threshold,
                threshold_degree=threshold / pi * 180,
                a_max=a[index_max],
                angle_max=angle_max,
                a_min=a[index_min],
            )
        )


def _moeller_trumbore_intersection_algorithm(
    origin, direction, vertex_0, vertex_1, vertex_2
):
    # pylint: disable=too-many-locals, invalid-name
    origin = asanyarray(origin)
    direction = asanyarray(direction)
    vertex_0 = asanyarray(vertex_0)
    vertex_1 = asanyarray(vertex_1)
    vertex_2 = asanyarray(vertex_2)
    edge_0 = vertex_1 - vertex_0
    edge_1 = vertex_2 - vertex_0

    h = cross(direction, edge_1)
    a = sum_(edge_0 * h, axis=-1)
    is_parallel_mask = isclose(a, 0, **ISCLOSE_KWARGS)
    if __debug__:
        _check_parallel_consistency(a, direction, edge_0, edge_1, is_parallel_mask)

    with errstate(divide="ignore", invalid="ignore"):
        f = 1 / a
        s = origin - vertex_0
        u = f * sum_(s * h, axis=-1)
        q = cross(s, edge_0)
        v = f * sum_(direction * q, axis=-1)
        has_no_intersection_mask = logical_or(
            logical_or(u < 0, u > 1), logical_or(v < 0, u + v > 1)
        )
        line_parameter = asanyarray(f * sum_(edge_1 * q, axis=-1))

    line_parameter[is_parallel_mask] = inf
    line_parameter[has_no_intersection_mask] = NaN
    return line_parameter


def line_triangle_intersection(line, triangle):
    """Return the intersection of given `line` and `triangle`."""
    line = asanyarray(line)
    triangle = asanyarray(triangle)
    assert line.shape[-2:] == (2, 3)
    assert triangle.shape[-2:] == (3, 3)

    line_index = tuple(
        [slice(None)] * len(line.shape[:-2])
        + [newaxis] * len(triangle.shape[:-2])
        + [slice(None)]
    )

    origin = line[..., 0, :][line_index]
    direction = line[..., 1, :][line_index]
    line_parameter = line_triangle_intersection_line_parameter(
        line=line, triangle=triangle
    )
    with errstate(invalid="ignore"):
        intersection = origin + line_parameter[..., newaxis] * direction
    is_parallel_mask = isinf(line_parameter)
    has_no_intersection_mask = isnan(line_parameter)
    intersection[has_no_intersection_mask] = NaN
    intersection[is_parallel_mask] = inf
    return intersection


def ray_triangle_intersection(ray, triangle):
    """Return the intersection of given `ray` and `triangle`."""
    ray = asanyarray(ray)
    triangle = asanyarray(triangle)
    assert ray.shape[-2:] == (2, 3)
    assert triangle.shape[-2:] == (3, 3)

    line_index = tuple(
        [slice(None)] * len(ray.shape[:-2])
        + [newaxis] * len(triangle.shape[:-2])
        + [slice(None)]
    )

    origin = ray[..., 0, :][line_index]
    direction = ray[..., 1, :][line_index]
    line_parameter = line_triangle_intersection_line_parameter(
        line=ray, triangle=triangle
    )
    with errstate(invalid="ignore"):
        intersection = origin + line_parameter[..., newaxis] * direction
    is_parallel_mask = isinf(line_parameter)
    has_no_intersection_mask = logical_or(isnan(line_parameter), line_parameter < 0)
    intersection[has_no_intersection_mask] = NaN
    intersection[is_parallel_mask] = inf
    return intersection


def line_segment_triangle_intersection(line_segment, triangle):
    """Return the intersection of given `line_segment` and `triangle`."""
    line_segment = asanyarray(line_segment)
    triangle = asanyarray(triangle)
    assert line_segment.shape[-2:] == (2, 3)
    assert triangle.shape[-2:] == (3, 3)

    line_index = tuple(
        [slice(None)] * len(line_segment.shape[:-2])
        + [newaxis] * len(triangle.shape[:-2])
        + [slice(None)]
    )

    initial_vertex = line_segment[..., 0, :]
    terminal_vertex = line_segment[..., 1, :]
    line = empty_like(line_segment)
    line[..., 0, :] = initial_vertex
    line[..., 1, :] = terminal_vertex - initial_vertex

    origin = line[..., 0, :][line_index]
    direction = line[..., 1, :][line_index]

    line_parameter = line_triangle_intersection_line_parameter(
        line=line, triangle=triangle
    )
    with errstate(invalid="ignore"):
        intersection = origin + line_parameter[..., newaxis] * direction
    is_parallel_mask = isinf(line_parameter)
    with errstate(invalid="ignore"):
        has_no_intersection_mask = logical_or(
            isnan(line_parameter), logical_or(line_parameter < 0, line_parameter > 1)
        )
    intersection[has_no_intersection_mask] = NaN
    intersection[is_parallel_mask] = inf
    return intersection


def line_plane_intersection(line, plane):
    """Return intersection between a line and a plane."""
    line = asanyarray(line)
    plane = asanyarray(plane)

    line_point = line[..., 0, :]
    line_direction = line[..., 1, :]

    plane_point = plane[..., 0, :]
    plane_normal = plane[..., 1, :]

    parameter = dot(plane_point - line_point, plane_normal) / dot(
        line_direction, plane_normal
    )

    intersection = line_point + parameter[..., newaxis] * line_direction

    return intersection
