from __future__ import annotations

from typing import (
	List,
	Sequence,
	TYPE_CHECKING,
	Tuple,
	Union,
)

import numpy as np
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


class Colors:
	BLACK = (0, 0, 0)
	PENCIL = (29, 106, 229)
	WHITE = (255, 255, 255)


class Rendering:

	def __init__(self, font: Font, colors: List[Colors or Tuple[int, int, int]], cell_size: int, width: int):
		self.cell_size = cell_size
		self.colors = colors
		self.font = font
		self.width = width
		self.empty = Color(0, 0, 0, 0)

	def size(self, scale: Tuple[int, int] = (1, 1), margin: Tuple[int, int] = (0, 0)) -> Tuple[int, int]:
		return formula(self.cell_size, scale, margin, lambda cs, s, m: (cs * s) + m)


class Renderer:

	def __init__(self, plane: Grid, screen_size: Union[Tuple[int, int], Sequence[int], None]):
		self.dirty = []
		self.loaded = False
		self.plane = plane
		self.screen = None
		self.size = screen_size

	def load(self):
		width = self.grid.rendering.width
		size = self.grid.rendering.cell_size
		for cell in self.grid.cells_iter(flags=['refs_ok'], op_flags=['readonly']):
			pg.draw.rect(cell[()].surfaces.background, Colors.BLACK, (0, 0, size, size), width)
		plane = self.grid.sub_grid([(0, 0)])
		cells_enum = np.ndenumerate(plane.cells)
		surfs = [(cell.surfaces.background, (i * size, j * size)) for (i, j), cell in cells_enum]
		self.grid.surface.blits(surfs, doreturn=True)
		self.resize(self.size)
		self.loaded = True

	def tick(self):
		if not self.loaded:
			self.load()
		if len(self.dirty):
			pg.display.update(self.dirty.pop(0))

	def resize(self, new_size):
		self.screen = pg.display.set_mode(size=new_size, flags=RESIZABLE)
		self.screen.fill(Colors.WHITE)
		self.screen.blit(self.plane.surface, (0, 0))
		pg.display.flip()


class PencilMarks:

	def __init__(self, size: Tuple[int, int]):
		self.center = Surface(size, flags=SRCALPHA)
		self.corner = Surface(size, flags=SRCALPHA)


class Surfaces:

	def __init__(self, cell: Cell):
		self.cell = cell
		self.background = Surface(self.size, flags=SRCALPHA)
		self.selected = Surface(self.size, flags=SRCALPHA)
		self.value = Surface(self.size, flags=SRCALPHA)
		self.pencil_marks = PencilMarks(self.size)

	@property
	def color(self) -> Colors:
		return self.cell.grid.rendering.colors[int(self.cell.data.given)]

	@property
	def font(self) -> Font:
		return self.cell.grid.rendering.font

	@property
	def size(self) -> Tuple[int, int]:
		return self.cell.grid.rendering.size()

	def clear(self):
		self.value.fill(self.cell.grid.rendering.empty)

	def render(self):
		text = self.font.render(str(self.cell.data.value), 1, self.color)
		self.value.blit(text, (0, 0))
