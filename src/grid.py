from __future__ import annotations

from typing import (
	Iterable,
	List,
	Optional,
	Tuple,
)

import numpy as np
from pygame import Surface, SRCALPHA

from data import Data, Regioning
from rendering import Surfaces, Rendering

Flags = Optional[Iterable[str]]


class Cell:

	def __init__(self, grid: Grid):
		self.grid = grid
		self.data = Data(self)
		self.surfaces = Surfaces(self)
		self.selected = False


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
