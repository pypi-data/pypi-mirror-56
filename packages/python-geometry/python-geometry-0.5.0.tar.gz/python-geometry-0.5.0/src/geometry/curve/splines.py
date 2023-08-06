"""Collection of splines of the geometry package."""

from attr import attrib, attrs
from numpy import asanyarray, ascontiguousarray, concatenate, linspace, newaxis, sqrt
from numpy import sum as sum_
from numpy import transpose, zeros
from numpy.linalg import norm
from scipy.integrate import quad
from scipy.interpolate import splev, splprep

from ..utilities import are_same_point


@attrs
class BSpline:
    """N-dimensional B-spline for polygonal chains."""

    vertices = attrib(converter=lambda v: asanyarray(v).copy())
    is_closed = attrib()
    degree = attrib(default=3)
    smoothing = attrib(default=None)

    def __attrs_post_init__(self):
        # pylint: disable=attribute-defined-outside-init
        self._tck = self._fit_spline(
            vertices=self.vertices,
            degree=self.degree,
            smoothing=self.smoothing,
            is_closed=self.is_closed,
        )

    @staticmethod
    def _fit_spline(vertices, degree, smoothing, is_closed):
        # pylint: disable=unsubscriptable-object
        if is_closed and not are_same_point(vertices[0], vertices[-1]):
            vertices = concatenate(
                (transpose(vertices), transpose([vertices[0]])), axis=-1
            )
        else:
            vertices = transpose(vertices)
        # as we have a copy of vertices we do not care whether things are reset
        quiet = 2
        # pylint: disable=attribute-defined-outside-init
        tck = splprep(vertices, k=degree, s=smoothing, per=is_closed, quiet=quiet)[0]
        return tck

    def __call__(self, evaluation_points, derivative=0):
        """Return the interpolated values at given evaluation points."""
        evaluation_points = asanyarray(evaluation_points)
        return ascontiguousarray(
            transpose(splev(evaluation_points, self._tck, der=derivative))
        )

    def length(self, quad_kwargs=None):
        """Return the length of the curve."""
        quad_kwargs = quad_kwargs or {}
        length = quad(
            func=lambda x: norm(self(x, derivative=1), axis=-1), a=0, b=1, **quad_kwargs
        )[0]
        return length

    def curvature(self, evaluation_points):
        """Return the curvature values at given evaluation points."""
        evaluation_points = asanyarray(evaluation_points)
        first_derivative = self(evaluation_points, derivative=1)
        second_derivative = self(evaluation_points, derivative=2)

        first_derivative_norm = norm(first_derivative, axis=-1)
        second_derivative_norm = norm(second_derivative, axis=-1)

        # sometimes there might be very small negative values that lead the square root
        # to complain
        tmp = (
            first_derivative_norm ** 2 * second_derivative_norm ** 2
            - sum_(first_derivative * second_derivative, axis=-1) ** 2
        )
        tmp[tmp < 0] = 0

        curvature = sqrt(tmp) / first_derivative_norm ** 3
        return curvature

    def get_equally_spaced_evaluation_points(self, desired_vertex_spacing):
        """Return equally spaced evaluation points for desired vertex spacing."""
        length = self.length()
        initial_guess = int(round(length / desired_vertex_spacing))
        if self.is_closed:
            if initial_guess < 2:
                initial_guess = 2
            evaluation_points = linspace(0, 1, initial_guess, endpoint=False)
        else:
            initial_guess += 1
            if initial_guess < 2:
                initial_guess = 2
            evaluation_points = linspace(0, 1, initial_guess, endpoint=True)
        return evaluation_points


@attrs
class CubicHermiteSpline:
    """N-dimensional cubic Hermite spline."""

    initial_vertex = attrib(converter=asanyarray)
    initial_tangent = attrib(converter=asanyarray)
    terminal_vertex = attrib(converter=asanyarray)
    terminal_tangent = attrib(converter=asanyarray)

    def __call__(self, evaluation_points, derivative=0):
        """Return the interpolated values at given evaluation points."""
        ev_points = asanyarray(evaluation_points)
        if derivative == 0:
            result = (
                (2 * ev_points ** 3 - 3 * ev_points ** 2 + 1)[..., newaxis]
                * self.initial_vertex
                + (ev_points ** 3 - 2 * ev_points ** 2 + ev_points)[..., newaxis]
                * self.initial_tangent
                + (-2 * ev_points ** 3 + 3 * ev_points ** 2)[..., newaxis]
                * self.terminal_vertex
                + (ev_points ** 3 - ev_points ** 2)[..., newaxis]
                * self.terminal_tangent
            )
        elif derivative == 1:
            result = (
                (6 * ev_points ** 2 - 6 * ev_points)[..., newaxis] * self.initial_vertex
                + (3 * ev_points ** 2 - 4 * ev_points + 1)[..., newaxis]
                * self.initial_tangent
                + (-6 * ev_points ** 2 + 6 * ev_points)[..., newaxis]
                * self.terminal_vertex
                + (3 * ev_points ** 2 - 2 * ev_points)[..., newaxis]
                * self.terminal_tangent
            )
        elif derivative == 2:
            result = (
                (12 * ev_points - 6)[..., newaxis] * self.initial_vertex
                + (6 * ev_points - 4)[..., newaxis] * self.initial_tangent
                + (-12 * ev_points + 6)[..., newaxis] * self.terminal_vertex
                + (6 * ev_points - 2)[..., newaxis] * self.terminal_tangent
            )
        elif derivative == 3:
            result = (
                12 * self.initial_vertex
                + 6 * self.initial_tangent
                - 12 * self.terminal_vertex
                + 6 * self.terminal_tangent
            )
        elif derivative > 3:
            # pylint: disable=no-member
            result = zeros([ev_points.shape[0], self.initial_vertex.shape[1]])
        else:
            raise NotImplementedError()
        return result

    def length(self, quad_kwargs=None):
        """Return the length of the curve."""
        quad_kwargs = quad_kwargs or {}
        length = quad(
            func=lambda x: norm(self(x, derivative=1), axis=-1), a=0, b=1, **quad_kwargs
        )[0]
        return length

    def curvature(self, evaluation_points):
        """Return the curvature values at given evaluation points."""
        evaluation_points = asanyarray(evaluation_points)
        first_derivative = self(evaluation_points, derivative=1)
        second_derivative = self(evaluation_points, derivative=2)

        first_derivative_norm = norm(first_derivative, axis=-1)
        second_derivative_norm = norm(second_derivative, axis=-1)

        # sometimes there might be very small negative values that lead the square root
        # to complain
        tmp = (
            first_derivative_norm ** 2 * second_derivative_norm ** 2
            - sum_(first_derivative * second_derivative, axis=-1) ** 2
        )
        tmp[tmp < 0] = 0

        curvature = sqrt(tmp) / first_derivative_norm ** 3
        return curvature
