import unittest

import pygame as pg

from src.game import Rendering, Colors
from src.grid import Grid, Cell, RegionData


class TestGrid(unittest.TestCase):
	pg.init()
	region_data = RegionData()
	region_data._size = (2, 2)
	font = pg.font.SysFont('monospaced', 15)
	rendering = Rendering(font, [Colors.PENCIL, Colors.BLACK], 50, 3)
	grid = Grid(dimensions=3, region_data=region_data, rendering=rendering)

	def test_dimensions(self):
		self.assertEqual(self.grid.dimensions, 3)

	def test_region_size(self):
		self.assertEqual(self.grid.region_data.size()[0], 2)
		self.assertEqual(self.grid.region_data.size()[1], 2)

	def test_size(self):
		self.assertEqual(self.grid.size, 4)

	def test_cell(self):
		self.assertIsInstance(self.grid.cells[0, 0, 0], Cell)

	def test_sub_grid(self):
		self.assertEqual(self.grid.sub_grid([(2, 0), (0, 0)]).cells[1], self.grid.cells[0][1][0])

	def test_sub_grid_too_far(self):
		self.assertIsInstance(self.grid.sub_grid([(2, 0), (0, 0), (0, 0), (0, 0)]), Grid)


if __name__ == '__main__':
	unittest.main()
