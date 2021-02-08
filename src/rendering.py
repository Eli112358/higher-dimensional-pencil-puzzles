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

from tuple_util import formula

if TYPE_CHECKING:
	from grid import Grid, Cell

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


class Renderer:

	def __init__(
			self,
			grid: Grid,
			screen_size: Union[Size, Sequence[int], None],
			rendering: Rendering,
	):
		self.grid = grid
		self.loaded = False
		self.rendering = rendering
		self.screen = None
		self.size = screen_size
		self.plane = None

	def tick(self):
		size = self.rendering.size
		for cell in self.plane.iterator():
			cell[()].surfaces.render()
		surfs = [(cell.surfaces.background, size(coord)) for coord, cell in self.plane.enumerator]
		self.plane.surface.blits(surfs, doreturn=False)
		self.resize(self.size)

	def resize(self, new_size: Size):
		if not self.loaded:
			self.screen = pg.display.set_mode(size=new_size, flags=RESIZABLE)
			self.loaded = True
		self.screen.fill(Colors.WHITE)
		self.screen.blit(self.plane.surface, (0, 0))
		pg.display.flip()


class PencilMarks:

	def __init__(self, size: Size):
		self.center = Surface(size, flags=SRCALPHA)
		self.corner = Surface(size, flags=SRCALPHA)


class Surfaces:

	def __init__(self, cell: Cell):
		self.cell = cell
		self.background = Surface(self.size, flags=SRCALPHA)
		self.border = Surface(self.size, flags=SRCALPHA)
		self.selected = Surface(self.size, flags=SRCALPHA)
		self.value = Surface(self.size, flags=SRCALPHA)
		self.pencil_marks = PencilMarks(self.size)
		width = self.cell.grid.rendering.width
		size = self.cell.grid.rendering.cell_size
		pg.draw.rect(self.border, Colors.BLACK, (0, 0, size, size), width)
		self.selected.fill(Colors.SELECTED)

	@property
	def color(self) -> Colors:
		return self.cell.grid.rendering.colors[int(self.cell.given)]

	@property
	def font(self) -> Font:
		return self.cell.grid.rendering.font

	@property
	def size(self) -> Tuple[int, int]:
		return self.cell.grid.rendering.size()

	def render(self):
		text = self.font.render(str(self.cell.value), 1, self.color)
		self.value.fill(self.cell.grid.rendering.empty)
		self.value.blit(text, (0, 0))
		self.background.fill(Colors.WHITE)
		surfs = [
			self.border,
			self.value,
		]
		if self.cell.selected:
			surfs.append(self.selected)
		for s in surfs:
			self.background.blit(s, (0, 0))
