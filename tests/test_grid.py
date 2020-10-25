import unittest

from src import Grid


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
        self.assertEqual(self.grid.cells[0, 0, 0], None)


if __name__ == '__main__':
    unittest.main()
