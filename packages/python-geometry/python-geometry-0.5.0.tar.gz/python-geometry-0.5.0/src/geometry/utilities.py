"""Utility functions of the geometry package."""
from itertools import chain

from numpy import abs as abs_
from numpy import allclose, asanyarray, finfo, floor, inf, issubsctype, log10
from numpy import max as max_
from numpy import nanmedian


def are_same_point(point, other_point, magnitude_shift=6):
    """Return whether two points are the same point."""
    point = asanyarray(point)
    other_point = asanyarray(other_point)

    if allclose(point, other_point, atol=0, rtol=0):
        atol = 0
    else:
        if issubsctype(point, int):
            point_atol = -inf
        else:
            point_atol = finfo(point.dtype).eps

        if issubsctype(other_point, int):
            other_point_atol = -inf
        else:
            other_point_atol = finfo(other_point.dtype).eps

        coordinates_to_consider = [c for c in chain(point, other_point) if not c == 0]

        atol = max_(
            [
                10
                ** int(
                    floor(nanmedian(log10(abs_(coordinates_to_consider))))
                    - magnitude_shift
                ),
                point_atol,
                other_point_atol,
            ]
        )
    return allclose(point, other_point, atol=atol, rtol=0)
