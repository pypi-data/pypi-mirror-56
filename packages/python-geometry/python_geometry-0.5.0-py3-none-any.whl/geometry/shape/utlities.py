"""Utilities for meshes."""

from numpy import logical_not


def get_points_in_or_on_shape(shape, points):
    """Return points that are in the shape or on its boundary."""
    vertices_in_shape_mask = logical_not(shape.has_on_unbounded_side(points))
    filtered_points = points[vertices_in_shape_mask]
    return filtered_points
