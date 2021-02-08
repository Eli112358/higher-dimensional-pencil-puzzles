from __future__ import annotations

from typing import Sequence, Union

import pygame as pg
from pygame.event import Event
from pygame.locals import (
	KEYDOWN,
	MOUSEBUTTONDOWN,
	MOUSEBUTTONUP,
	QUIT,
	VIDEORESIZE,
)

from grid import Grid, Regioning
from keys import number_keys
from rendering import Colors, Renderer, Rendering, Size
from tuple_util import formula


class Game:

	def __init__(
			self,
			grid: Grid,
			screen_size: Union[Size, Sequence[int], None],
	):
		self.grid = grid
		self.plane = self.grid.sub_grid([(0, 0)])
		self.renderer = Renderer(self.plane, screen_size)
		self.mouse_down = False
		self.mouse_edge = False

	def clear_selection(self):
		for cell in self.plane.iterator():
			cell[()].selected = False

	def clear_interactions(self):
		for cell in self.plane.iterator():
			cell[()].interacted = False

	def select_cell(self):
		pos = pg.mouse.get_pos()
		ctrl_held = pg.key.get_mods() & pg.KMOD_CTRL
		shift_held = pg.key.get_mods() & pg.KMOD_SHIFT
		size = self.plane.rendering.size()
		width = self.plane.rendering.width
		coord = formula(pos, size, width, lambda p, s, w: p // (s + w))
		if not (ctrl_held or shift_held) and self.mouse_edge:
			self.clear_selection()
		try:
			cell = self.plane.cells[coord]
			if not cell.interacted:
				if ctrl_held:
					cell.selected = not cell.selected
				else:
					cell.selected = True
				cell.interacted = True
			self.mouse_edge = False
		except IndexError:
			pass

	def enter_digit(self, event: Event):
		digit = number_keys.index(event.key) % 10
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
				# rising edge
				self.mouse_down = True
				self.mouse_edge = True
			if event.type == MOUSEBUTTONUP:
				# falling edge
				self.mouse_down = False
				self.mouse_edge = True
			if event.type == KEYDOWN:
				if event.key in number_keys:
					self.enter_digit(event)
		if self.mouse_down:
			self.select_cell()
		if not self.mouse_down and self.mouse_edge:
			self.clear_interactions()
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
