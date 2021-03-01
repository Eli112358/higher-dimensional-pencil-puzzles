from typing import (
	Optional,
	Sequence,
	Union,
)

from pygame import (
	RESIZABLE,
	Rect,
	display,
)

from grid import (
	Cell,
	Grid,
	GridBase,
)
from rendering import (
	Colors,
	Rendering,
	Size,
)
from rendering.graphics import ModeButton
from ui.elements import Button, InputBox
from ui.grid import CellRenderer, GridRenderer

CellType = Union[Cell, CellRenderer]


class Renderer:

	def __init__(
			self,
			grid: Grid,
			screen_size: Union[Size, Sequence[int], None],
			rendering: Rendering,
	):
		self.buttons = []
		self.coordinates = None
		self.grid = grid
		self.input_boxes = []
		self.loaded = False
		self.rendering = rendering
		self.screen = None
		self.size = screen_size
		self.plane = GridRenderer(self, (20, 20), self.grid.size)
		self.view = GridBase(2, self.grid.size)
		rect = Rect(50, self.plane.rect.bottom + 20, 200, 50)
		self.input_boxes.append(InputBox(self, rect, self.set_view, False))
		self.set_view()
		self.__init_mode_buttons()

	@property
	def mode(self) -> str:
		return [btn.name for btn in self.get_buttons('mode') if btn.enabled][0]

	@property
	def modes(self) -> Sequence[str]:
		return [btn.name for btn in self.get_buttons('mode')]

	@property
	def selected(self) -> Sequence[Cell]:
		return [self.get_cell(cell[()]) for cell in self.plane.iterator() if cell[()].selected]

	def __buttons(self, condition: Optional[str] = 'True') -> Sequence[Button]:
		return [btn for btn in self.buttons if eval(condition)]

	def __init_mode_buttons(self):
		rect = [Rect(self.plane.rect.right + 20, 30, 60, 60)]
		for _ in range(3):
			r = rect[-1].copy()
			r.y += r.h + 5
			rect.append(r)
		names = [
			Cell.Field.GUESS,
			Cell.Field.CONTINGENCY,
			Cell.Field.CANDIDATE,
			Cell.Field.COLOR,
		]
		icons = [
			ModeButton.digit,
			ModeButton.corner,
			ModeButton.center,
			ModeButton.color,
		]
		font = self.rendering.font
		radio = Button.Type.RADIO
		for i in range(4):
			btn = Button(self, names[i].name, rect[i], icons[i](font, Colors.BLACK), btn_type=radio, group='mode')
			self.buttons.append(btn)
		self.get_buttons('mode')[0].enabled = True

	def get_button(self, name: str) -> Button:
		return self.__buttons(f'btn.name == "{name}"')[0]

	def get_buttons(self, group: str) -> Sequence[Button]:
		return self.__buttons(f'btn.group == "{group}"')

	def get_cell(self, source: CellType) -> CellType:
		grids = [self.view, self.plane]
		if isinstance(source, CellRenderer):
			grids.reverse()
		return grids[1].cells[grids[0].get_coordinates(source)]

	def set_mode(self, name: str):
		self.get_button(name).enable()

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
		self.plane.render()
		self.resize(self.size)

	def resize(self, new_size: Size):
		self.size = new_size
		if not self.loaded:
			self.screen = display.set_mode(size=self.size, flags=RESIZABLE)
			self.loaded = True
		self.screen.fill(Colors.WHITE)
		self.screen.blit(self.plane.surface, self.plane.rect)
		for btn in self.buttons:
			btn.draw(self.screen)
		for box in self.input_boxes:
			box.draw(self.screen, self.rendering.font)
		display.flip()
