from typing import (
	Sequence,
	Union,
)

from pygame import (
	Rect,
	display,
)
from pygame.constants import RESIZABLE

from grid import (
	Grid,
	GridBase,
	CellBase,
)
from rendering import (
	Size,
	Rendering,
	Colors,
)
from ui.elements import InputBox
from ui.grid import CellRenderer, GridRenderer


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
		rect = Rect(50, self.plane.surface.get_height() + 20, 200, 50)
		self.input_boxes.append(InputBox(self, rect, self.set_view, False))
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
			self.screen = display.set_mode(size=new_size, flags=RESIZABLE)
			self.loaded = True
		self.screen.fill(Colors.WHITE)
		self.screen.blit(self.plane.surface, (0, 0))
		for box in self.input_boxes:
			box.draw(self.screen, self.rendering.font)
		display.flip()
