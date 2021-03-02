from __future__ import annotations

import unittest

import pygame as pg

from grid import (
	Cell,
	Regioning,
)
from grid.sudoku import SudokuGrid
from rendering import Rendering


class TestGrid(unittest.TestCase):
	pg.init()
	region_data = Regioning()
	region_data._size = (2, 2)
	rendering = Rendering(50, 'monospaced', 3)
	grid = SudokuGrid(dimensions=3, regioning=region_data)

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
