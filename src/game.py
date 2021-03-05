from typing import (
	Sequence,
	Union,
)

from pygame import (
	KEYDOWN,
	KMOD_CTRL,
	KMOD_SHIFT,
	K_DELETE,
	MOUSEBUTTONDOWN,
	MOUSEBUTTONUP,
	QUIT,
	VIDEORESIZE,
	event as events,
	init as init_game,
)
from pygame.event import Event
from pygame.key import get_mods as get_mod_keys
from pygame.mouse import get_pos as get_mouse_pos

from grid import Regioning
from grid.render import GridRenderer
from grid.sudoku import SudokuGrid
from keys import (
	mode_keys,
	number_keys,
)
from rendering import (
	Rendering,
	Size,
)
from rendering.renderer import Renderer
from util.tuple import formula


class Game:

	def __init__(
			self,
			grid: SudokuGrid,
			screen_size: Union[Size, Sequence[int], None],
			rendering: Rendering,
	):
		self.grid = grid
		self.renderer = Renderer(self.grid, screen_size, rendering)
		self.mouse_down = False
		self.mouse_edge = False

	def clear_cells(self):
		for cell in self.renderer.selected:
			cell.clear()

	def select_cell(self):
		pos = get_mouse_pos()
		ctrl_held = get_mod_keys() & KMOD_CTRL
		shift_held = get_mod_keys() & KMOD_SHIFT
		size = self.renderer.rendering.size()
		topleft = self.renderer.plane.rect.topleft
		coord = formula(lambda p, s, f: (p - f) // s, pos, size, topleft)
		if not (ctrl_held or shift_held) and self.mouse_edge:
			self.renderer.plane.clear(GridRenderer.Clearable.SELECTIONS)
		max_index = self.renderer.plane.size
		if not all([0 <= coord[0] < max_index, 0 <= coord[1] < max_index]):
			return
		cell = self.renderer.plane.cells[coord]
		if not cell.interacted:
			if ctrl_held:
				cell.selected = not cell.selected
			else:
				cell.selected = True
			cell.interacted = True
		self.mouse_edge = False

	def enter_digit(self, event: Event):
		digit = number_keys.index(event.key) % 10
		mode = self.renderer.mode
		for cell in self.renderer.selected:
			cell.toggle(digit, mode)

	def mainloop(self) -> bool:
		for event in events.get():
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
				elif event.key == K_DELETE:
					self.clear_cells()
				elif event.key in mode_keys:
					self.renderer.set_mode(key=event.key)
			for btn in self.renderer.buttons:
				btn.handle_event(event)
			for box in self.renderer.input_boxes:
				box.handle_event(event)
		if self.mouse_down:
			self.select_cell()
		if not self.mouse_down and self.mouse_edge:
			self.renderer.plane.clear(GridRenderer.Clearable.INTERACTIONS)
		self.renderer.tick()
		return True


def main():
	init_game()
	regioning = Regioning(False, size=(2, 2))
	screen_size = (500, 500)
	rendering = Rendering(50, 'monospaced', 3)
	grid = SudokuGrid(3, regioning)
	game = Game(grid, screen_size, rendering)
	while game.mainloop():
		pass


if __name__ == '__main__':
	main()
