import numpy as np
import pygame as pg
from pygame import Color
from pygame.locals import (
	KEYDOWN,
	QUIT
)

from src.grid import RegionData, Grid
from src.tuple_util import formula


class Colors:
	BLACK = (0, 0, 0)
	PENCIL = (29, 106, 229)
	WHITE = (255, 255, 255)


class Rendering:

	def __init__(self, font, colors, cell_size, width):
		self.cell_size = cell_size
		self.colors = colors
		self.font = font
		self.width = width
		self.empty = Color(0, 0, 0, 0)

	def size(self, scale=1, margin=0):
		return formula(self.cell_size, scale, margin)


class Game:

	def __init__(self, grid, screen_size):
		self.grid = grid
		self.screen = pg.display.set_mode(screen_size)
		self.handlers = {}
		self.dirty = []
		self.loaded = False

	def load(self):
		self.screen.fill(Colors.WHITE)
		width = self.grid.rendering.width
		size = self.grid.rendering.cell_size
		for cell in self.grid.cells_iter(flags=['refs_ok'], op_flags=['readonly']):
			pg.draw.rect(cell[()].surface, Colors.BLACK, (0, 0, size, size), width)
		plane = self.grid.sub_grid([(0, 0)])
		cells_enum = np.ndenumerate(plane.cells)
		surfs = [(cell.surface, (i*size, j*size)) for (i, j), cell in cells_enum]
		self.dirty += self.screen.blits(surfs, doreturn=True)
		self.loaded = True

	def mainloop(self):
		for event in pg.event.get():
			if event.type == QUIT:
				return False
			if event.type == KEYDOWN:
				if event.key in self.handlers:
					self.handlers[event.key]()

		if not self.loaded:
			self.load()
			# pg.display.flip()
		if len(self.dirty):
			pg.display.update(self.dirty.pop(0))
		return True


def main():
	pg.init()
	regions = RegionData()
	regions._size = (2, 2)
	screen_size = [500, 500]
	font = pg.font.SysFont('monospaced', 15)
	rendering = Rendering(font, [Colors.PENCIL, Colors.BLACK], 50, 3)
	grid = Grid(dimensions=3, region_data=regions, rendering=rendering)
	game = Game(grid, screen_size)
	while game.mainloop():
		pass


if __name__ == '__main__':
	main()
