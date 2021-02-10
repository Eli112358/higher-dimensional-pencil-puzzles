from __future__ import annotations

from typing import (
	Callable,
	List,
	Sequence,
	TYPE_CHECKING,
	Tuple,
	Union,
)

import pygame as pg
from pygame import (
	Color,
	RESIZABLE,
	SRCALPHA,
	Surface,
)
from pygame.font import Font

from grid import CellBase, GridBase
from tuple_util import formula

if TYPE_CHECKING:
	from grid import (
		Cell,
		Grid,
	)

Size = Union[int, Tuple[int, int]]


class Colors:
	BLACK = (0, 0, 0)
	PENCIL = (29, 106, 229)
	SELECTED = (230, 217, 48, 128)
	WHITE = (255, 255, 255)


class Rendering:

	def __init__(
			self,
			font: Font,
			colors: List[Colors or Tuple[int, int, int]],
			cell_size: int,
			width: int,
	):
		self.cell_size = cell_size
		self.colors = colors
		self.font = font
		self.width = width
		self.empty = Color(0, 0, 0, 0)

	def size(self, scale: Size = (1, 1), margin: Size = (0, 0)) -> Tuple[int, int]:
		return formula(self.cell_size, scale, margin, lambda cs, s, m: (cs * s) + m)


class PencilMarks:

	def __init__(self, size: Size):
		self.center = Surface(size, flags=SRCALPHA)
		self.corner = Surface(size, flags=SRCALPHA)


class CellRenderer(CellBase):

	def __init__(self, grid: GridRenderer):
		super().__init__(grid)
		self.interacted = False
		self.selected = False
		self.background = Surface(self.size, flags=SRCALPHA)
		self.border = Surface(self.size, flags=SRCALPHA)
		self.selection = Surface(self.size, flags=SRCALPHA)
		self.value = Surface(self.size, flags=SRCALPHA)
		self.pencil_marks = PencilMarks(self.size)
		width = self.rendering.width
		size = self.rendering.cell_size
		pg.draw.rect(self.border, Colors.BLACK, (0, 0, size, size), width)
		self.selection.fill(Colors.SELECTED)

	@property
	def renderer(self) -> Renderer:
		return self.grid.renderer

	@property
	def rendering(self):
		return self.renderer.rendering

	@property
	def cell(self) -> Cell:
		return self.renderer.get_cell(self)

	@property
	def color(self) -> Colors:
		return self.rendering.colors[int(self.cell.given)]

	@property
	def font(self) -> Font:
		return self.rendering.font

	@property
	def size(self) -> Tuple[int, int]:
		return self.rendering.size()

	def render(self):
		text = self.font.render(str(self.cell.value), 1, self.color)
		self.value.fill(self.rendering.empty)
		self.value.blit(text, (0, 0))
		self.background.fill(Colors.WHITE)
		surfs = [
			self.border,
			self.value,
		]
		if self.selected:
			surfs.append(self.selection)
		for s in surfs:
			self.background.blit(s, (0, 0))


class GridRenderer(GridBase):
	class Clearable:
		INTERACTIONS = 'interactions'
		SELECTIONS = 'selections'

		@staticmethod
		def error(name):
			ValueError(f'{name} must be one of GridRenderer.Clearable literals')

	def __init__(
			self,
			size: int,
			renderer: Renderer,
	):
		self.renderer = renderer
		super().__init__(2, size, CellRenderer)
		margin = self.renderer.grid.regioning.size(extra=(1, 1))
		size_calc = self.renderer.rendering.size(self.size, margin=margin)
		self.surface = Surface(size_calc, flags=SRCALPHA)

	def clear(self, target: Clearable):
		for cell in self.iterator():
			if target is GridRenderer.Clearable.INTERACTIONS:
				cell[()].interacted = False
			elif target is GridRenderer.Clearable.SELECTIONS:
				cell[()].selected = False
			else:
				raise GridRenderer.Clearable.error('target')


class InputBox:
	# Derived from the object-oriented variant at https://stackoverflow.com/a/46390412/2640292

	def __init__(self, renderer: Renderer, rect: pg.Rect, callback: Callable, reset: bool = True, text: str = ''):
		self.active = False
		self.callback = callback
		self.rect = rect
		self.renderer = renderer
		self.reset = reset
		self.surface = pg.Surface((self.rect.w, self.rect.h))
		self.text = text
		self.txt_surface = self.font.render(self.text, True, Colors.BLACK)

	@property
	def color(self):
		return Colors.PENCIL if self.active else Colors.BLACK

	@property
	def font(self):
		return self.renderer.rendering.font

	def handle_event(self, event):
		if event.type == pg.MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				self.active = not self.active
			else:
				self.active = False
				self.callback(self.text)
		if event.type == pg.KEYDOWN:
			if self.active:
				if event.key == pg.K_RETURN:
					self.callback(self.text)
					if self.reset:
						self.text = ''
				elif event.key == pg.K_BACKSPACE:
					self.text = self.text[:-1]
				elif event.key == pg.K_ESCAPE:
					self.text = ''
				else:
					self.text += event.unicode

	def draw(self, screen: Surface, font: Font):
		self.txt_surface = font.render(self.text, True, Colors.BLACK)
		self.rect.w = max(200, self.txt_surface.get_width() + 10)
		screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
		pg.draw.rect(screen, self.color, self.rect, 5)


class Renderer:

	def __init__(
			self,
			grid: Grid,
			screen_size: Union[Size, Sequence[int], None],
			rendering: Rendering,
	):
		self.coordinates = None
		self.grid = grid
		self.input_boxes = []
		self.loaded = False
		self.rendering = rendering
		self.screen = None
		self.size = screen_size
		self.plane = GridRenderer(self.grid.size, self)
		self.view = GridBase(2, self.grid.size, None)
		rect = pg.Rect(50, self.plane.surface.get_height() + 20, 200, 50)
		self.input_boxes.append(InputBox(self, rect, self.set_view, False, ''))
		self.set_view()

	def get_cell(self, source: CellBase) -> CellBase:
		grids = [self.view, self.plane]
		if isinstance(source, CellRenderer):
			grids.reverse()
		return grids[1].cells[grids[0].get_coordinates(source)]

	def get_selected(self):
		return [self.get_cell(cell[()]) for cell in self.plane.iterator() if cell[()].selected]

	def set_view(self, s: str = ''):
		if s == '':
			c = [0] * (self.grid.dimensions - 2) + [-1, -1]
			s = ','.join([str(x) for x in c])
			self.input_boxes[0].text = s
		self.coordinates = tuple([int(x) for x in s.split(',')])
		axes = []
		mapped = []
		for i, c in enumerate(self.coordinates):
			(mapped if c < 0 else axes).append(i)
		coord = tuple([min(c, self.plane.size - 1) for c in self.coordinates if c > -1])
		if len(mapped) != 2:
			raise ValueError('coordinates must have exactly 2 "-1"s')
		self.view.cells = self.grid.cells.transpose(axes + mapped)[coord]

	def tick(self):
		size = self.rendering.size
		for cell in self.plane.iterator():
			cell[()].render()
		surfs = [(cell.background, size(coord)) for coord, cell in self.plane.enumerator]
		self.plane.surface.blits(surfs, doreturn=False)
		self.resize(self.size)

	def resize(self, new_size: Size):
		if not self.loaded:
			self.screen = pg.display.set_mode(size=new_size, flags=RESIZABLE)
			self.loaded = True
		self.screen.fill(Colors.WHITE)
		self.screen.blit(self.plane.surface, (0, 0))
		for box in self.input_boxes:
			box.draw(self.screen, self.rendering.font)
		pg.display.flip()
