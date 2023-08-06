"""Internal functions of the geometry package."""

from collections import namedtuple

from numpy import asanyarray

VerticesInformation = namedtuple(
    "VerticesInformation", ("vertices", "number_of_vertices", "number_of_dimensions")
)


def _get_vertices_information(vertices):
    vertices = asanyarray(vertices)
    if not vertices.ndim == 2:
        raise ValueError(
            "Invalid number of array dimensions: {}. (Expected 2)".format(vertices.ndim)
        )
    number_of_vertices, number_of_dimensions = vertices.shape
    vertices_information = VerticesInformation(
        vertices=vertices,
        number_of_vertices=number_of_vertices,
        number_of_dimensions=number_of_dimensions,
    )
    return vertices_information
