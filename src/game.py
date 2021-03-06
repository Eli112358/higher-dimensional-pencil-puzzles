from asyncio import run
from typing import Tuple

from pygame import (
	KEYDOWN,
	KMOD_CTRL,
	KMOD_SHIFT,
	K_DELETE,
	MOUSEBUTTONDOWN,
	MOUSEBUTTONUP,
	MOUSEMOTION,
	QUIT,
	event as events,
	init as init_game,
	quit as quit_game,
)
from pygame.event import Event
from pygame.key import get_mods as get_mod_keys
from pygame.time import Clock

from event import (
	EventHandler,
	event_handler,
)
from grid import Regioning
from grid.render import GridRenderer
from grid.sudoku import SudokuGrid
from keys import (
	mode_keys,
	number_keys,
)
from rendering import Rendering
from rendering.renderer import Renderer
from util.tuple import formula


class Mouse(EventHandler):

	def __init__(
			self,
			down: bool = False,
			edge: bool = False,
			pos: Tuple[int, int] = None,
	):
		super().__init__()
		self.down = down
		self.edge = edge
		self.pos = pos

	@property
	def falling(self) -> bool:
		return (not self.down) and self.edge

	@property
	def rising(self) -> bool:
		return self.down and self.edge

	@property
	def up(self):
		return not self.down

	@event_handler(MOUSEBUTTONUP)
	def fall(self, _=None):
		self.down = False
		self.edge = True

	@event_handler(MOUSEMOTION)
	def move(self, event: Event):
		self.pos = event.pos

	@event_handler(MOUSEBUTTONDOWN)
	def rise(self, _=None):
		self.down = True
		self.edge = True

	def reset(self):
		self.edge = False


class Game(EventHandler):

	def __init__(
			self,
			grid: SudokuGrid,
			rendering: Rendering,
	):
		super().__init__()
		self.clock = Clock()
		self.fps = 30
		self.grid = grid
		self.mouse = Mouse()
		self.renderer = Renderer(self, self.grid, rendering)
		self.running = True

	@event_handler(KEYDOWN)
	def key_press(self, event: Event):
		if event.key in number_keys:
			self.enter_digit(event)
		elif event.key == K_DELETE:
			self.clear_cells()
		elif event.key in mode_keys:
			self.renderer.set_mode(key=event.key)

	def clear_cells(self):
		for cell in self.renderer.selected:
			cell.clear()

	def select_cell(self):
		pos = self.mouse.pos
		ctrl_held = get_mod_keys() & KMOD_CTRL
		shift_held = get_mod_keys() & KMOD_SHIFT
		size = self.renderer.rendering.size()
		topleft = self.renderer.plane.rect.topleft
		coord = formula(lambda p, s, f: (p - f) // s, pos, size, topleft)
		if not (ctrl_held or shift_held) and self.mouse.edge:
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
		self.mouse.reset()

	def enter_digit(self, event: Event):
		digit = number_keys.index(event.key) % 10
		mode = self.renderer.mode
		for cell in self.renderer.selected:
			cell.toggle(digit, mode)

	def mainloop(self):
		event = events.poll()
		if event.type == QUIT:
			self.running = False
			return
		self.handle(event)
		self.mouse.handle(event)
		for element in self.renderer.elements:
			element.handle(event)
		if self.mouse.down:
			self.select_cell()
		if self.mouse.falling:
			self.renderer.plane.clear(GridRenderer.Clearable.INTERACTIONS)
		self.clock.tick()
		if self.clock.get_fps() >= self.fps:
			self.renderer.tick()


async def main():
	init_game()
	regioning = Regioning(False, (3, 3))
	rendering = Rendering(50, 'monospaced', 3)
	grid = SudokuGrid(3, regioning)
	game = Game(grid, rendering)
	while game.running:
		game.mainloop()
	quit_game()


if __name__ == '__main__':
	run(main())
