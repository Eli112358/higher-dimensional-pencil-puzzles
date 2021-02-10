from __future__ import annotations

from typing import (
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
		Coordinates,
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
			coordinates: Coordinates,
			renderer: Renderer,
	):
		self.coordinates = coordinates
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


class Renderer:

	def __init__(
			self,
			grid: Grid,
			coordinates: Coordinates,
			screen_size: Union[Size, Sequence[int], None],
			rendering: Rendering,
	):
		self.coordinates = coordinates
		self.grid = grid
		self.loaded = False
		self.rendering = rendering
		self.screen = None
		self.size = screen_size
		self.plane = GridRenderer(self.grid.size, coordinates, self)
		self.view = GridBase(2, self.grid.size, None)
		self.set_view()

	def get_cell(self, source: CellBase) -> CellBase:
		grids = [self.view, self.plane]
		if isinstance(source, CellRenderer):
			grids.reverse()
		return grids[1].cells[grids[0].get_coordinates(source)]

	def set_view(self):
		axes = []
		mapped = []
		for i, c in self.coordinates:
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
		pg.display.flip()
