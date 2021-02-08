from __future__ import annotations

from typing import (
	Iterable,
	List,
	Optional,
	TYPE_CHECKING,
	Tuple,
)

import numpy as np
from pygame import Surface, SRCALPHA

from rendering import Rendering, Surfaces
from tuple_util import formula

if TYPE_CHECKING:
	from rendering import Size

Coordinates = Tuple[int, ...]
Flags = Optional[Iterable[str]]


class Regioning:

	def __init__(self, regular: bool = True, size: Size = None):
		self.regular = regular
		self._size = size
		if self.regular:
			self._size = (3, 3)

	def load(self, file):
		# implement later to support irregular sudoku
		pass

	def size(self, scale: Size = (1, 1), extra: Size = (0, 0)):
		return formula(self._size, scale, extra, lambda ss, s, e: (ss * s) + e)


class CellBase:

	def __init__(self, grid: GridBase):
		self.grid = grid


class GridBase:

	def __init__(
			self,
			dimensions: int = 2,
			size: int = 9,
			cell_type: type = CellBase,
	):
		self.dimensions = dimensions
		self.size = size
		self.cells = np.empty([self.size] * self.dimensions, cell_type)
		for cell in self.iterator(op_flags=['writeonly']):
			cell[...] = cell_type(self)

	@property
	def enumerator(self):
		return np.ndenumerate(self.cells)

	def get_coordinates(self, target: CellBase) -> Coordinates:
		for coordinates, cell in self.enumerator:
			if cell == target:
				return coordinates
		raise KeyError('target cell is not in grid')

	def iterator(self, flags: Flags = None, op_flags: Flags = None) -> np.nditer:
		if flags is None:
			flags = ['refs_ok']
		if op_flags is None:
			op_flags = ['readonly']
		return np.nditer(self.cells, flags=flags, op_flags=op_flags)


class Cell:

	def __init__(self, grid: Grid):
		self.grid = grid
		self.candidates = 0
		self.contingencies = 0
		self.given = False
		self.region = None
		self.value = ''
		self.surfaces = Surfaces(self)
		self.selected = False
		self.interacted = False

	def set_given(self, value: int):
		self.value = value
		self.given = value != ''

	def set_guess(self, value: int):
		if not self.given:
			self.value = value


class Grid:

	def __init__(
			self,
			cells: np.ndarray = None,
			dimensions: int = 2,
			parent: Grid = None,
			regioning: Regioning = Regioning(),
			rendering: Rendering = None,
	):
		self.cells = cells
		self.parent = parent
		self.dimensions = dimensions
		self.regioning = regioning
		self.rendering = rendering
		if self.parent is not None:
			# inherit certain properties
			self.dimensions = self.parent.dimensions - 1
			self.regioning = self.parent.regioning
			self.rendering = self.parent.rendering
			self.surface = self.parent.surface
		self.size = self.regioning.size()[0] * self.regioning.size()[1]
		if self.parent is None:
			margin = self.regioning.size(extra=(1, 1))
			self.surface = Surface(self.rendering.size(self.size, margin), flags=SRCALPHA)
		if self.cells is None:
			self.cells = np.empty([self.size] * self.dimensions, Cell)
			for cell in self.iterator(op_flags=['writeonly']):
				cell[...] = Cell(self)
			for coords, cell in self.enumerator:
				cell.coords = coords

	def iterator(self, flags: Flags = None, op_flags: Flags = None) -> np.nditer:
		if flags is None:
			flags = ['refs_ok']
		if op_flags is None:
			op_flags = ['readonly']
		return np.nditer(self.cells, flags=flags, op_flags=op_flags)

	@property
	def enumerator(self):
		return np.ndenumerate(self.cells)

	def sub_grid(self, index_pairs: List[Tuple[int, int]]) -> Grid:
		if len(index_pairs) == 0 or isinstance(self.cells, Cell):
			return self
		axis, index = index_pairs[0]
		axes = list(range(self.cells.ndim))
		axes.insert(0, axes.pop(axis))
		cells = self.cells.transpose(tuple(axes))[index]
		grid = Grid(cells=cells, parent=self)
		try:
			return grid.sub_grid(index_pairs[1:])
		except TypeError:
			# You've tried to go too far
			# Warn in the logs later
			return grid
