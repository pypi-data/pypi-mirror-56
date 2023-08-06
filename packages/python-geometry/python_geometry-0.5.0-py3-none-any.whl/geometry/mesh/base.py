"""Basic components for meshes."""

from abc import ABC, abstractmethod

from attr import attrs


@attrs
class Mesh(ABC):
    """Base class defining the interface of a mesh."""

    @property
    @abstractmethod
    def number_of_dimensions(self):
        """Return the number of spatial dimensions of the mesh."""
        ...

    @property
    @abstractmethod
    def number_of_cells(self):
        """Return the number of cells that make up the mesh."""
        ...

    @abstractmethod
    def get_cell_id_around_point(self, point):
        """Return the ID of the cell containing the given `point`."""
        ...

    @abstractmethod
    def is_valid_cell_id(self, cell_id):
        """Return whether the given `cell_id` is valid for this mesh."""
        ...

    @property
    @abstractmethod
    def cell_volumes(self):
        """Return an array containing the cell volumes."""
        ...

    @property
    @abstractmethod
    def shape(self):
        """Return the shape of the mesh."""
        ...
