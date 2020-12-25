import numpy as np
from pygame import Surface, SRCALPHA

from data import Data, Regioning
from rendering import Surfaces


class Cell:

	def __init__(self, grid):
		self.grid = grid
		self.data = Data(self)
		self.surfaces = Surfaces(self)


class Grid:

	def __init__(
			self,
			cells=None,
			dimensions=2,
			parent=None,
			region_data=Regioning(),
			rendering=None,
	):
		self._dimensions = None
		self.cells = cells
		self.parent = parent
		self.dimensions = dimensions
		self.region_data = region_data
		self.rendering = rendering
		if self.parent is not None:
			# inherit certain properties
			self.dimensions = self.parent.dimensions - 1
			self.region_data = self.parent.region_data
			self.rendering = self.parent.rendering
			self.surface = self.parent.surface
		self.size = self.region_data.size()[0] * self.region_data.size()[1]
		if self.parent is None:
			margin = self.region_data.size(extra=1)
			self.surface = Surface(self.rendering.size(self.size, margin), flags=SRCALPHA)
		if self.cells is None:
			self.cells = np.empty([self.size] * self.dimensions, Cell)
			for cell in self.cells_iter(flags=['refs_ok'], op_flags=['writeonly']):
				cell[...] = Cell(self)

	def cells_iter(self, flags=None, op_flags=None):
		return np.nditer(self.cells, flags=flags, op_flags=op_flags)

	def sub_grid(self, index_pairs):
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
