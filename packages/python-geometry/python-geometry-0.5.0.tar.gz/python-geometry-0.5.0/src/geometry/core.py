"""Core functions of the geometry package."""

from attr import attrib, attrs
from numpy import abs as abs_
from numpy import all as all_
from numpy import (
    allclose,
    arccos,
    argmax,
    asanyarray,
    asarray,
    cos,
    cross,
    dot,
    empty,
    empty_like,
    errstate,
    identity,
    inf,
    isclose,
    linspace,
    newaxis,
    number,
    roll,
)
from numpy import round as round_
from numpy import sin, sqrt
from numpy import sum as sum_
from numpy import zeros
from numpy.linalg import norm

from .internal import _get_vertices_information
from .validators import SubDTypeValidator


def get_segments(vertices, is_closed):
    """Return segments described by given `vertices`."""
    vertices, number_of_vertices, number_of_dimensions = _get_vertices_information(
        vertices=vertices
    )
    if not number_of_vertices > 1:
        raise ValueError("It takes at least more than one vertex to form segments.")
    if is_closed:
        segments = empty((number_of_vertices, number_of_dimensions))
        segments[:-1] = vertices[1:] - vertices[:-1]
        segments[-1] = vertices[0] - vertices[-1]
    else:
        segments = vertices[1:] - vertices[:-1]
    return segments


def get_segment_lengths(vertices, is_closed):
    """Return lengths of segments given by `vertices`."""
    segments = get_segments(vertices=vertices, is_closed=is_closed)
    segment_lengths = norm(segments, axis=-1)
    return segment_lengths


def get_segment_lengths_at_vertices(vertices, is_closed):
    """Return lengths of segments given by `vertices` at vertices."""
    segment_lengths = get_segment_lengths(vertices=vertices, is_closed=is_closed)
    segment_lengths_at_vertices = empty(len(vertices))
    if is_closed:
        segment_lengths_at_vertices[0] = 0.5 * (
            segment_lengths[-1] + segment_lengths[0]
        )
        segment_lengths_at_vertices[1:] = 0.5 * (
            segment_lengths[:-1] + segment_lengths[1:]
        )
    else:
        segment_lengths_at_vertices[0] = 0.5 * segment_lengths[0]
        segment_lengths_at_vertices[1:-1] = 0.5 * (
            segment_lengths[:-1] + segment_lengths[1:]
        )
        segment_lengths_at_vertices[-1] = 0.5 * segment_lengths[-1]
    return segment_lengths_at_vertices


def get_normal_vectors(vertices, is_closed):
    """Return normalized normal vectors of segments given by `vertices`."""
    if not vertices.shape[-1] == 3:
        raise ValueError(
            "Computing normal vectors only makes sense for three-dimensional space."
        )
    segments = get_segments(vertices=vertices, is_closed=is_closed)
    if is_closed:
        normal_vectors = empty_like(vertices)
        normal_vectors[0] = normalize(cross(segments[-1], segments[0]))
        normal_vectors[1:] = normalize(cross(segments[:-1], segments[1:]))
    else:
        normal_vectors = normalize(cross(segments[:-1], segments[1:]))
    return normal_vectors


def get_normal_vector(vertices, is_closed):
    """Return normalized normal vector of polygon given by `vertices`."""
    if not vertices.shape[-1] == 3:
        raise ValueError(
            "Computing normal vectors only makes sense for three-dimensional space."
        )
    segments = get_segments(vertices=vertices, is_closed=is_closed)
    if is_closed:
        normal_vectors = empty_like(vertices)
        normal_vectors[0] = cross(segments[-1], segments[0])
        normal_vectors[1:] = cross(segments[:-1], segments[1:])
    else:
        normal_vectors = cross(segments[:-1], segments[1:])
    return normalize(sum_(normal_vectors, axis=0))


def normalize(vectors):
    """Return normalized `vectors`."""
    return asanyarray(vectors) / norm(vectors, axis=-1)[..., newaxis]


def are_parallel(vector, other_vector):
    """Return whether given `vector` is parallel to given `other_vector`."""
    if allclose(vector, 0) or allclose(other_vector, 0):
        return True
    normalized_vector = normalize(vectors=vector)
    normalized_other_vector = normalize(vectors=other_vector)

    return allclose(normalized_vector, normalized_other_vector) or allclose(
        normalized_vector, -normalized_other_vector
    )


def are_antiparallel(vector, other_vector):
    """Return whether given `vector` is parallel to given `other_vector`."""
    if allclose(vector, 0) or allclose(other_vector, 0):
        return True
    normalized_vector = normalize(vectors=vector)
    normalized_other_vector = normalize(vectors=other_vector)

    return allclose(normalized_vector, -normalized_other_vector)


def get_circle_radii(vertices, is_closed):
    """Return radii of circles described by vertices at each vertex."""
    vertices = asanyarray(vertices)
    vertices_prev = roll(vertices, -1, axis=0)
    vertices_next = roll(vertices, 1, axis=0)

    length_mid_next = norm(vertices_next - vertices, axis=1)
    length_prev_next = norm(vertices_next - vertices_prev, axis=1)
    length_prev_mid = norm(vertices - vertices_prev, axis=1)

    length_prev_next_average = (
        length_mid_next + length_prev_next + length_prev_mid
    ) / 2
    radii = zeros(len(vertices))
    with errstate(divide="ignore"):
        if is_closed:
            # Due to floating point arithmetic it may happen that the term
            # in the square root becomes "slightly" negative even though it
            # should be zero
            tmp = (
                length_prev_next_average
                * (length_prev_next_average - length_mid_next)
                * (length_prev_next_average - length_prev_next)
                * (length_prev_next_average - length_prev_mid)
            )
            tmp[tmp < 0] = 0
            radii = length_mid_next * length_prev_next * length_prev_mid / 4 / sqrt(tmp)
        else:
            # Due to floating point arithmetic it may happen that the term
            # in the square root becomes "slightly" negative even though it
            # should be zero
            tmp = (
                length_prev_next_average[1:-1]
                * (length_prev_next_average[1:-1] - length_mid_next[1:-1])
                * (length_prev_next_average[1:-1] - length_prev_next[1:-1])
                * (length_prev_next_average[1:-1] - length_prev_mid[1:-1])
            )
            tmp[tmp < 0] = 0
            radii[1:-1] = (
                length_mid_next[1:-1]
                * length_prev_next[1:-1]
                * length_prev_mid[1:-1]
                / 4
                / sqrt(tmp)
            )
            radii[0] = inf
            radii[-1] = inf
    return radii


def get_angle_between_vectors(vector_1, vector_2):
    """Return the angle between two vectors."""
    vector_1 = normalize(vector_1)
    vector_2 = normalize(vector_2)
    angle_between_vectors = arccos(sum_(vector_1 * vector_2, axis=-1))
    return angle_between_vectors


def get_cross_product_matrix(vector):
    """Return the cross product matrix of given vector."""
    vector = asanyarray(vector)
    cross_product_matrix = zeros(list(vector.shape) + [vector.shape[-1]])
    cross_product_matrix[..., 0, 1] = -vector[..., 2]
    cross_product_matrix[..., 0, 2] = vector[..., 1]
    cross_product_matrix[..., 1, 0] = vector[..., 2]
    cross_product_matrix[..., 1, 2] = -vector[..., 0]
    cross_product_matrix[..., 2, 0] = -vector[..., 1]
    cross_product_matrix[..., 2, 1] = vector[..., 0]
    return cross_product_matrix


def get_rotation_matrix(axis, angle):
    """Return rotation matrix for rotation by given angle about given axis."""
    axis_normalized = normalize(axis)
    rotation_matrix = (
        cos(angle) * identity(len(axis_normalized))
        + sin(angle) * get_cross_product_matrix(axis_normalized)
        + (1 - cos(angle)) * (axis_normalized[:, newaxis] * axis_normalized[newaxis, :])
    )
    return rotation_matrix


def get_reflection_matrix(direction):
    """Return matrix for reflection through the origin orthogonal to given direction."""
    direction_normalized = normalize(direction)
    reflection_matrix = identity(len(direction_normalized)) - 2 * (
        direction_normalized[:, newaxis] * direction_normalized[newaxis, :]
    )
    return reflection_matrix


def get_equally_spaced_points(
    minimum, maximum, average_distance, minimum_number_of_points=None, **linspace_kwargs
):
    """Return equally spaced points between `minimum` and `maximum`."""
    number_of_points = round_((maximum - minimum) / average_distance).astype(int) + 1
    if minimum_number_of_points is not None:
        number_of_points = max(number_of_points, minimum_number_of_points)
    return linspace(minimum, maximum, number_of_points, **linspace_kwargs)


@attrs(cmp=False)
class Direction:
    """A direction whose length is irrelevant."""

    _direction = attrib(converter=asarray, validator=SubDTypeValidator(number))

    def __array__(self):
        return self._direction

    def __neg__(self):
        return type(self)(direction=-self._direction)

    def __eq__(self, other):
        if isinstance(other, Direction):
            return all_(isclose(normalize(self), normalize(other)), axis=-1)
        return False


@attrs
class Line:
    """A line represented by a point and a vector."""

    _point = attrib(converter=asanyarray)
    _vector = attrib(converter=asanyarray)

    @property
    def direction(self):
        """Return the normalized direction of the line."""
        return normalize(self._vector)

    def point(self, parameter=0):
        """Return a point of the line."""
        return self._point + parameter * self._vector


@attrs
class Plane:
    """A plane."""

    _parameters = attrib(converter=asanyarray)

    @classmethod
    def from_point_and_direction(cls, point, direction):
        """Construct plane from a point and a normal direction."""
        parameters = empty(4)
        parameters[:3] = direction
        # pylint: disable=invalid-unary-operand-type
        parameters[3] = -dot(point, direction)
        # pylint: enable=invalid-unary-operand-type
        return cls(parameters=parameters)

    @classmethod
    def from_points(cls, point_0, point_1, point_2):
        """Construct plane from three points."""
        point_0 = asanyarray(point_0)
        point_1 = asanyarray(point_1)
        point_2 = asanyarray(point_2)
        vector_20 = point_0 - point_2
        vector_21 = point_1 - point_2
        direction = cross(vector_20, vector_21)
        return cls.from_point_and_direction(point=point_2, direction=direction)

    @property
    def orthogonal_direction(self):
        """Return the normalized normal vector of the plane."""
        return normalize(self._parameters[:3])

    @property
    def orthogonal_vector(self):
        """Return the normal vector of the plane."""
        return self._parameters[:3]

    @property
    def d(self):  # pylint: disable=invalid-name
        """Return the `d` parameter of the point-normal form of the plane."""
        return self._parameters[3]

    @property
    def point(self):
        """Return a point on the plane."""
        point = zeros(3)
        i_max = argmax(abs_(self._parameters[:3]))
        point[i_max] = -self._parameters[3] / self._parameters[i_max]
        return point

    def projection(self, point):
        """Return the projection of `point` onto the plane."""
        lambda_ = (dot(self.orthogonal_vector, point) + self.d) / dot(
            self.orthogonal_vector, self.orthogonal_vector
        )
        projected_point = point - lambda_ * self.orthogonal_vector
        return projected_point
