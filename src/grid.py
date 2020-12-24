import numpy as np
from pygame import Surface, SRCALPHA

from src.tuple_util import formula


class RegionData:

	def __init__(self, regular=True, size=None):
		self.regular = regular
		self._size = size
		if self.regular:
			self._size = (3, 3)

	def load(self, file):
		# implement later to support irregular sudoku
		pass

	def size(self, scale=1, extra=0):
		return formula(self._size, scale, extra)


class Grid:

	def __init__(
			self,
			cells=None,
			dimensions=2,
			parent=None,
			region_data=RegionData(),
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


class Cell(np.object):

	def __init__(self, grid):
		self.grid = grid
		self.surface = Surface(self.grid.rendering.size(), flags=SRCALPHA)
		self.given = False
		self.value = None
		self.candidates = PencilMarks(self)  # center
		self.contingencies = PencilMarks(self)  # corner

	def set_given(self, value):
		self.value = value
		self.given = value is not None

	def set_guess(self, value):
		if not self.given:
			self.value = value

	@property
	def color(self):
		return self.grid.rendering.colors[int(self.given)]

	@property
	def font(self):
		return self.grid.rendering.font

	def clear(self):
		self.surface.fill(self.grid.rendering.empty)

	def render(self):
		text = self.font.render(str(self.value), 1, self.color)
		self.surface.blit(text, (0, 0))


class PencilMarks(list):

	def __init__(self, cell):
		self.cell = cell
		super().__init__([False] * (self.cell.grid.size + 1))

	def fill(self, value):
		for digit in range(len(self)):
			self.set(digit, value)

	def set(self, digit, value=True):
		self[digit] = value

	def toggle(self, digit):
		self[digit] = not self[digit]
