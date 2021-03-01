from typing import Sequence, Union

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

from grid import Grid, Regioning
from keys import number_keys
from rendering import (
	Colors,
	Rendering,
	Size,
)
from rendering.renderer import Renderer
from ui.grid import GridRenderer
from util.tuple import formula


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
		pos = get_mouse_pos()
		ctrl_held = get_mod_keys() & KMOD_CTRL
		shift_held = get_mod_keys() & KMOD_SHIFT
		size = self.renderer.rendering.size()
		topleft = self.renderer.plane.rect.topleft
		coord = formula(pos, size, topleft, lambda p, s, f: (p - f) // s)
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
	rendering = Rendering('monospaced', [Colors.PENCIL, Colors.BLACK], 50, 3)
	grid = Grid(3, regioning)
	game = Game(grid, screen_size, rendering)
	while game.mainloop():
		pass


if __name__ == '__main__':
	main()
