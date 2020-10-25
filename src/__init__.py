import numpy as np


class Grid:

	def __init__(self, dimensions, region_size):
		self.dimensions = dimensions
		self.region_size = region_size
		self.size = self.region_size[0] * self.region_size[1]
		self.cells = np.empty([self.size for _ in range(self.dimensions)], Cell)
		for cell in np.nditer(self.cells, flags=['refs_ok'], op_flags=['readwrite']):
			cell[...] = Cell()


class Cell(np.object):

	def __init__(self):
		pass
