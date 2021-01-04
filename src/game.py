from __future__ import annotations

from typing import Sequence, Union

import pygame as pg
from pygame.locals import (
	KEYDOWN,
	MOUSEBUTTONDOWN,
	QUIT,
	VIDEORESIZE,
)

from data import Regioning, Size
from grid import Grid
from rendering import Renderer, Rendering, Colors
from tuple_util import formula


class Game:

	def __init__(self, grid: Grid, screen_size: Union[Size, Sequence[int], None]):
		self.grid = grid
		self.plane = self.grid.sub_grid([(0, 0)])
		self.renderer = Renderer(self.plane, screen_size)
		self.handlers = {}

	def click(self):
		pos = pg.mouse.get_pos()
		size = self.plane.rendering.size()
		width = self.plane.rendering.width
		coords = formula(pos, size, width, lambda p, s, w: p // (s + w))
		try:
			cell = self.plane.cells[coords]
			cell.selected = not cell.selected
		except IndexError:
			for cell in self.plane.cells_iter():
				cell[()].selected = False

	def mainloop(self) -> bool:
		for event in pg.event.get():
			if event.type == QUIT:
				return False
			if event.type == VIDEORESIZE:
				self.renderer.resize(event.size)
			if event.type == MOUSEBUTTONDOWN:
				self.click()
			if event.type == KEYDOWN:
				if event.key in self.handlers.keys():
					self.handlers[event.key](event)

		self.renderer.tick()
		return True


def main():
	pg.init()
	regioning = Regioning(False, size=(2, 2))
	screen_size = [500, 500]
	font_size = 50
	font = pg.font.SysFont('monospaced', font_size)
	rendering = Rendering(font, [Colors.PENCIL, Colors.BLACK], 50, 3)
	grid = Grid(dimensions=3, regioning=regioning, rendering=rendering)
	game = Game(grid, screen_size)
	while game.mainloop():
		pass


if __name__ == '__main__':
	main()
