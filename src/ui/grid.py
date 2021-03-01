from __future__ import annotations

from enum import auto
from typing import (
	TYPE_CHECKING,
	Tuple,
)

from pygame import (
	Rect,
	SRCALPHA,
	Surface,
	draw as drawing,
)

from rendering import (
	Colors,
	Size,
)
from rendering.graphics import render_text
from src.grid import (
	Cell,
	CellBase,
	GridBase,
)
from util.enums import AutoName

if TYPE_CHECKING:
	from rendering.renderer import Renderer


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
		drawing.rect(self.border, Colors.BLACK, (0, 0, size, size), width)
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
	def font(self) -> str:
		return self.rendering.font

	@property
	def size(self) -> Tuple[int, int]:
		return self.rendering.size()

	def render(self):
		text = render_text(self.font, str(self.cell.value), 50, self.color)
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
	class Clearable(str, AutoName):
		INTERACTIONS = auto()
		SELECTIONS = auto()

		@staticmethod
		def error(name: str):
			ValueError(f'{name} must be one of GridRenderer.Clearable literals')

	def __init__(
			self,
			renderer: Renderer,
			top_left: Tuple[int, int],
			size: int,
	):
		self.renderer = renderer
		super().__init__(2, size, CellRenderer)
		margin = self.renderer.grid.regioning.size(extra=(1, 1))
		size_calc = self.renderer.rendering.size(self.size, margin=margin)
		self.surface = Surface(size_calc, flags=SRCALPHA)
		x, y, l, w = top_left + size_calc
		self.rect = Rect(x, y, w + x, l + y)

	def clear(self, target: Clearable):
		for cell in self.iterator():
			if target == GridRenderer.Clearable.INTERACTIONS:
				cell[()].interacted = False
			elif target == GridRenderer.Clearable.SELECTIONS:
				cell[()].selected = False
			else:
				raise GridRenderer.Clearable.error('target')
