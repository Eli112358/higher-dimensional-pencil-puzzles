import numpy as np


class Grid:

	def __init__(self, dimensions, region_size, cells=None):
		self.dimensions = dimensions
		self.region_size = region_size
		self.size = self.region_size[0] * self.region_size[1]
		if cells is not None:
			self.cells = cells
		else:
			self.cells = np.empty([self.size]*self.dimensions, Cell)
			for cell in np.nditer(self.cells, flags=['refs_ok'], op_flags=['readwrite']):
				cell[...] = Cell(self.cells)

	def get_sub_grid(self, axis, index):
		axes = list(range(self.cells.ndim))
		axes.insert(0, axes.pop(axis))
		cells = self.cells.transpose(tuple(axes))[index]
		try:
			return Grid(self.dimensions - 1, self.region_size, cells)
		except TypeError:
			# You've tried to go too far
			# Warn in the logs later
			return self


class Cell(np.object):

	def __init__(self, grid):
		self.grid = grid
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


class PencilMarks(list):

	def __init__(self, cell):
		self.cell = cell
		super().__init__([False] * (self.cell.grid.size + 1))

	def clear(self):
		for i in range(len(self)):
			self[i] = False

	def toggle(self, i):
		self[i] = not self[i]
