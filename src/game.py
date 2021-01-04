from __future__ import annotations

from typing import Sequence, Union

import pygame as pg
from pygame.event import Event
from pygame.locals import (
	KEYDOWN,
	MOUSEBUTTONDOWN,
	QUIT,
	VIDEORESIZE,
	K_0,
	K_1,
	K_2,
	K_3,
	K_4,
	K_5,
	K_6,
	K_7,
	K_8,
	K_9,
	K_KP0,
	K_KP1,
	K_KP2,
	K_KP3,
	K_KP4,
	K_KP5,
	K_KP6,
	K_KP7,
	K_KP8,
	K_KP9,
)

from data import Regioning, Size
from grid import Grid
from rendering import Renderer, Rendering, Colors
from tuple_util import formula


class Game:
	number_keys = [
		K_0,
		K_1,
		K_2,
		K_3,
		K_4,
		K_5,
		K_6,
		K_7,
		K_8,
		K_9,
		K_KP0,
		K_KP1,
		K_KP2,
		K_KP3,
		K_KP4,
		K_KP5,
		K_KP6,
		K_KP7,
		K_KP8,
		K_KP9,
	]

	def __init__(self, grid: Grid, screen_size: Union[Size, Sequence[int], None]):
		self.grid = grid
		self.plane = self.grid.sub_grid([(0, 0)])
		self.renderer = Renderer(self.plane, screen_size)

	def clear_selection(self):
		for cell in self.plane.iterator():
			cell[()].selected = False

	def click(self):
		pos = pg.mouse.get_pos()
		ctrl_held = pg.key.get_mods() & pg.KMOD_CTRL
		size = self.plane.rendering.size()
		width = self.plane.rendering.width
		coords = formula(pos, size, width, lambda p, s, w: p // (s + w))
		if not ctrl_held:
			self.clear_selection()
		try:
			cell = self.plane.cells[coords]
			cell.selected = not cell.selected
		except IndexError:
			self.clear_selection()

	def enter_digit(self, event: Event):
		digit = self.number_keys.index(event.key) % 10
		selected = [cell[()] for cell in self.plane.iterator() if cell[()].selected]
		for cell in selected:
			cell.data.set_guess(digit)

	def mainloop(self) -> bool:
		for event in pg.event.get():
			if event.type == QUIT:
				return False
			if event.type == VIDEORESIZE:
				self.renderer.resize(event.size)
			if event.type == MOUSEBUTTONDOWN:
				self.click()
			if event.type == KEYDOWN:
				if event.key in self.number_keys:
					self.enter_digit(event)

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
