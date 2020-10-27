import unittest

from src.grid import Grid, Cell


class TestGrid(unittest.TestCase):
	d, l, w = 3, 2, 2
	grid = Grid(d, {0: l, 1: w})

	def test_dimensions(self):
		self.assertEqual(self.grid.dimensions, self.d)

	def test_region_size(self):
		self.assertEqual(self.grid.region_size[0], self.l)
		self.assertEqual(self.grid.region_size[1], self.w)

	def test_size(self):
		self.assertEqual(self.grid.size, self.l*self.w)

	def test_cell(self):
		self.assertIsInstance(self.grid.cells[0, 0, 0], Cell)

	def test_sub_grid(self):
		self.assertEqual(self.grid.get_sub_grid(2, 0).cells[0][1], self.grid.cells[0][1][0])


if __name__ == '__main__':
	unittest.main()
