from __future__ import annotations

import unittest

import pygame as pg

from grid import Cell, Grid, Regioning
from rendering import Colors, Rendering


class TestGrid(unittest.TestCase):
	pg.init()
	region_data = Regioning()
	region_data._size = (2, 2)
	font = pg.font.SysFont('monospaced', 15)
	rendering = Rendering(font, [Colors.PENCIL, Colors.BLACK], 50, 3)
	grid = Grid(dimensions=3, regioning=region_data)

	def test_dimensions(self):
		self.assertEqual(self.grid.dimensions, 3)

	def test_region_size(self):
		self.assertEqual(self.grid.regioning.size()[0], 2)
		self.assertEqual(self.grid.regioning.size()[1], 2)

	def test_size(self):
		self.assertEqual(self.grid.size, 4)

	def test_cell(self):
		self.assertIsInstance(self.grid.cells[0, 0, 0], Cell)


if __name__ == '__main__':
	unittest.main()
