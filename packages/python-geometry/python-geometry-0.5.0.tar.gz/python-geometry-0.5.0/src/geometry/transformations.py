"""Transformations for coordinate systems and geometric objects."""
# pylint: skip-file
import warnings
from abc import ABC, abstractmethod

from attr import attrib, attrs, validators
from numpy import (
    allclose,
    asanyarray,
    asarray,
    cross,
    dot,
    einsum,
    isclose,
    ndim,
    newaxis,
    number,
    stack,
)
from numpy import sum as sum_
from numpy.linalg import inv, norm

from .core import Line, Plane, get_reflection_matrix, get_rotation_matrix
from .validators import SubDTypeValidator


def _build_row_vector_matrix(*vectors):
    # Copy makes sure that the data is contiguous in memory
    return asanyarray(vectors)


def _are_orthogonal(vector_0, vector_1):
    return bool(isclose(dot(vector_0, vector_1), 0))


class AffineTransformation:
    """Affine transformation implementing the basic transformation interface.

    Parameters
    ----------
    x, y, z
        The new basis vectors expressed in the terms of the reference basis.

    """

    def __init__(self, x, y, z):
        warnings.warn("Interface of Transformations will change", DeprecationWarning)
        self._x = x
        self._y = y
        self._z = z
        self.transformation_matrix = self._build_transformation_matrix(x, y, z)
        self.inverse_transformation_matrix = self._build_inverse_transformation_matrix(
            self.transformation_matrix
        )

    @staticmethod
    def _build_transformation_matrix(x, y, z):
        return _build_row_vector_matrix(x, y, z)

    @staticmethod
    def _build_inverse_transformation_matrix(transformation_matrix):
        return inv(transformation_matrix)

    def pushforward(self, vectors):
        """Transform vectors from reference to target coordinate system.

        Parameters
        ----------
        vectors
            Vectors in the reference coordinate system.

        Returns
        -------
        np.ndarray
            Vectors in the target coordinate system.

        """
        v = asanyarray(vectors)
        return einsum("...i,ij->...j", v, self.transformation_matrix)

    def pullback(self, vectors):
        """Transform vectors from target to reference coordinate system.

        Parameters
        ----------
        vectors
            Vectors in the target coordinate system.

        Returns
        -------
        np.ndarray
            Vectors in the reference coordinate system.

        """
        v = asanyarray(vectors)
        return einsum("...i,ij->...j", v, self.inverse_transformation_matrix)

    def __repr__(self):
        return (
            "{self.__class__.__name__}("
            "x={self._x!r}, "
            "y={self._y!r}, "
            "z={self._z!r}"
            ")"
        ).format(self=self)


class OrthogonalTransformation(AffineTransformation):
    """Transform coordinates using an orthogonal transformation.

    Parameters
    ----------
    x, y, z
        The new basis vectors expressed in the terms of the reference basis. At
        least two have to be given. If all three are given a check is performed
        to make sure that the new basis is orthogonal and right-handed.

    """

    def __init__(self, x=None, y=None, z=None):
        if x is not None:
            x = asanyarray(x)
        if y is not None:
            y = asanyarray(y)
        if z is not None:
            z = asanyarray(z)

        all_new_basis_vectors_given = False
        if x is not None and y is not None and z is not None:
            all_new_basis_vectors_given = True
        elif x is not None and y is not None and z is None:
            if not _are_orthogonal(x, y):
                raise RuntimeError("Non orthogonal target basis vectors given.")
            z = cross(x, y)
        elif x is not None and y is None and z is not None:
            if not _are_orthogonal(x, z):
                raise RuntimeError("Non orthogonal target basis vectors given.")
            y = cross(z, x)
        elif x is None and y is not None and z is not None:
            if not _are_orthogonal(y, z):
                raise RuntimeError("Non orthogonal target basis vectors given.")
            x = cross(y, z)
        else:
            raise RuntimeError("Not enough target basis vectors given.")
        x = x / norm(x)
        y = y / norm(y)
        z = z / norm(z)
        if all_new_basis_vectors_given and not allclose(cross(x, y), z):
            raise RuntimeError(
                "Unable to build transformation with given target basis, as "
                "they are non-orthogonal."
            )

        super(OrthogonalTransformation, self).__init__(x, y, z)

    @staticmethod
    def _build_inverse_transformation_matrix(transformation_matrix):
        # The inverse of an orthonormal matrix
        # Copy makes sure that the data is contiguous in memory
        return transformation_matrix.T.copy()


class Transformation(ABC):
    """Interface of a transformation."""

    @abstractmethod
    def transform(self, object_to_transform):
        """Transform `object_to_transform` according to the transformation."""
        ...


class HasInverseTransformationMixin(ABC):
    """Mixin for interfaces that have an inverse transformation."""

    @abstractmethod
    def get_inverse(self):
        """Return the inverse transformation."""
        ...


class LinearTransformation(Transformation):
    """Interface of a linear transformation."""

    @property
    @abstractmethod
    def transformation_matrix(self):
        """Return the transformation matrix."""
        ...

    def transform(self, object_to_transform):
        """Transform `object_to_transform` according to the transformation."""
        original_type = type(object_to_transform)
        object_to_transform = asanyarray(object_to_transform)

        rank_transformation_matrix = 2
        ndim_transformation_matrix = (
            ndim(self.transformation_matrix) - rank_transformation_matrix
        )

        rank_object_to_transform = 1
        ndim_object_to_transform = ndim(object_to_transform) - rank_object_to_transform

        transformation_matrix_slice = (
            ndim_transformation_matrix * (slice(None),)
            + ndim_object_to_transform * (newaxis,)
            + rank_transformation_matrix * (slice(None),)
            + (rank_object_to_transform - 1) * (newaxis,)
        )
        object_to_transform_slice = (
            ndim_transformation_matrix * (newaxis,)
            + ndim_object_to_transform * (slice(None),)
            + (rank_transformation_matrix - 1) * (newaxis,)
            + rank_object_to_transform * (slice(None),)
        )

        ret = sum_(
            self.transformation_matrix[transformation_matrix_slice]
            * object_to_transform[object_to_transform_slice],
            axis=-1,
        )

        return original_type(ret)


@attrs
class NullTransformation:
    """Transformation for returning the point as given."""

    def pushforward(self, point):
        """Return the point as is."""
        return point

    def pullback(self, point):
        """Return the point as is."""
        return point


@attrs
class Rotation(LinearTransformation):
    """Transformation for rotation around the origin."""

    rotation_matrix = attrib(converter=asarray, validator=SubDTypeValidator(number))

    @classmethod
    def from_rotated_basis(cls, *rotated_basis_vectors):
        """Construct rotation transformation from rotated basis vectors."""
        return cls(rotation_matrix=stack(rotated_basis_vectors, axis=-1))

    @classmethod
    def from_axis_and_angle(cls, axis, angle):
        """Construct rotation transformation from axis and angle."""
        return cls(rotation_matrix=get_rotation_matrix(axis=axis, angle=angle))

    @property
    def transformation_matrix(self):
        """Return the transformation matrix."""
        return self.rotation_matrix


@attrs
class ReflectionThroughPlane:
    """Transformation for reflection through an arbitrary plane."""

    plane = attrib(validator=validators.instance_of(Plane))

    @property
    def mirror_matrix(self):
        """Return the mirror matrix corresponding to mirroring through the plane."""
        return get_reflection_matrix(direction=self.plane.orthogonal_direction)

    def pushforward(self, point):
        """Pushforward the given point."""
        translation_point = self.plane.point
        translated_point = point - translation_point
        transformed_translated_point = einsum(
            "ij,...j->...i", self.mirror_matrix, translated_point
        )
        transformed_point = transformed_translated_point + translation_point
        return transformed_point

    def pullback(self, point):
        """Pullback the given point."""
        translation_point = self.plane.point
        translated_point = point - translation_point
        transformed_translated_point = einsum(
            "ij,...j->...i", self.mirror_matrix.T, translated_point
        )
        transformed_point = transformed_translated_point + translation_point
        return transformed_point


@attrs
class RotationAboutAxis:
    """Transformation for rotation about an arbitrary axis."""

    axis = attrib(validator=validators.instance_of(Line))
    angle = attrib()

    @property
    def rotation_matrix(self):
        """Return the rotation matrix corresponding to the rotation about the axis."""
        return get_rotation_matrix(axis=self.axis.direction, angle=self.angle)

    def pushforward(self, point):
        """Pushforward the given point."""
        translation_point = self.axis.point()
        translated_point = point - translation_point
        transformed_translated_point = einsum(
            "ij,...j->...i", self.rotation_matrix, translated_point
        )
        transformed_point = transformed_translated_point + translation_point
        return transformed_point

    def pullback(self, point):
        """Pullback the given point."""
        translation_point = self.axis.point()
        translated_point = point - translation_point
        transformed_translated_point = einsum(
            "ij,...j->...i", self.rotation_matrix.T, translated_point
        )
        transformed_point = transformed_translated_point + translation_point
        return transformed_point
