import pygame as pg
from pygame.locals import (
	KEYDOWN,
	QUIT
)

from data import Regioning
from grid import Grid
from rendering import Renderer, Rendering, Colors


class Game:

	def __init__(self, grid, screen_size):
		self.grid = grid
		self.renderer = Renderer(self.grid, screen_size)
		self.handlers = {}

	def mainloop(self):
		for event in pg.event.get():
			if event.type == QUIT:
				return False
			if event.type == KEYDOWN:
				if event.key in self.handlers:
					self.handlers[event.key]()

		self.renderer.tick()
		return True


def main():
	pg.init()
	regions = Regioning(False, size=(2, 2))
	screen_size = [500, 500]
	font = pg.font.SysFont('monospaced', 15)
	rendering = Rendering(font, [Colors.PENCIL, Colors.BLACK], 50, 3)
	grid = Grid(dimensions=3, region_data=regions, rendering=rendering)
	game = Game(grid, screen_size)
	while game.mainloop():
		pass


if __name__ == '__main__':
	main()
