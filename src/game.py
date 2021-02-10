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
from rendering import (
	Colors,
	GridRenderer,
	Renderer,
	Rendering,
	Size,
)
from tuple_util import formula


class Game:

	def __init__(
			self,
			grid: Grid,
			screen_size: Union[Size, Sequence[int], None],
			rendering: Rendering,
	):
		self.grid = grid
		self.renderer = Renderer(self.grid, screen_size, rendering)
		self.mouse_down = False
		self.mouse_edge = False

	def clear_cells(self):
		selected = self.renderer.get_selected()
		for cell in selected:
			cell.set_guess('')

	def select_cell(self):
		pos = pg.mouse.get_pos()
		ctrl_held = pg.key.get_mods() & pg.KMOD_CTRL
		shift_held = pg.key.get_mods() & pg.KMOD_SHIFT
		size = self.renderer.rendering.size()
		coord = formula(pos, size, 0, lambda p, s, w: p // (s + w))
		if not (ctrl_held or shift_held) and self.mouse_edge:
			self.renderer.plane.clear(GridRenderer.Clearable.SELECTIONS)
		try:
			cell = self.renderer.plane.cells[coord]
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
		selected = self.renderer.get_selected()
		for cell in selected:
			cell.set_guess(digit)

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
				elif event.key == pg.K_DELETE:
					self.clear_cells()
			for box in self.renderer.input_boxes:
				box.handle_event(event)
		if self.mouse_down:
			self.select_cell()
		if not self.mouse_down and self.mouse_edge:
			self.renderer.plane.clear(GridRenderer.Clearable.INTERACTIONS)
		self.renderer.tick()
		return True


def main():
	pg.init()
	regioning = Regioning(False, size=(2, 2))
	screen_size = (500, 500)
	font_size = 50
	font = pg.font.SysFont('monospaced', font_size)
	rendering = Rendering(font, [Colors.PENCIL, Colors.BLACK], 50, 3)
	grid = Grid(3, regioning)
	game = Game(grid, screen_size, rendering)
	while game.mainloop():
		pass


if __name__ == '__main__':
	main()
