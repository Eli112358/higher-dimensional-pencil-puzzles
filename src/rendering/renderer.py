from __future__ import annotations

from typing import (
	Optional,
	Sequence,
	TYPE_CHECKING,
	Union,
)

from pygame import (
	RESIZABLE,
	Rect,
	display,
)

from grid import Grid
from grid.render import (
	CellRenderer,
	GridRenderer,
)
from grid.sudoku import (
	SudokuCell,
	SudokuGrid,
)
from keys import mode_keys
from rendering import (
	Colors,
	Rendering,
)
from rendering.graphics import ModeButton
from ui.elements import (
	Button,
	InputBox,
	UIElement,
)
from util.tuple import formula

if TYPE_CHECKING:
	from game import Game

CellType = Union[SudokuCell, CellRenderer]


class Renderer:

	def __init__(
			self,
			game: Game,
			grid: SudokuGrid,
			rendering: Rendering,
	):
		self.buttons = []
		self.coordinates = None
		self.game = game
		self.grid = grid
		self.input_boxes = []
		self.loaded = False
		self.rendering = rendering
		self.screen = None
		self.plane = GridRenderer(self, (20, 20), self.grid.size)
		self.size = formula(lambda a, b, c: sum([a, b, c]), self.plane.rect.size, self.plane.rect.topleft, 100)
		self.view = Grid(2, self.grid.size)
		rect = Rect(50, self.plane.rect.bottom + 20, 200, 50)
		self.input_boxes.append(InputBox(self, 'coordinates', rect, self.set_view, False))
		self.set_view()
		self.__init_mode_buttons()

	@property
	def elements(self) -> Sequence[UIElement]:
		return self.buttons + self.input_boxes

	@property
	def mode(self) -> str:
		return self.__modes('btn.name', 'btn.enabled')[0]

	@property
	def modes(self) -> Sequence[str]:
		return self.__modes('btn.name')

	@property
	def selected(self) -> Sequence[SudokuCell]:
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
			SudokuCell.Field.GUESS,
			SudokuCell.Field.CONTINGENCY,
			SudokuCell.Field.CANDIDATE,
			SudokuCell.Field.COLOR,
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

	def __modes(self, value: str = 'btn', condition: str = 'True') -> Sequence:
		return [eval(value) for btn in self.get_buttons('mode') if eval(condition)]

	def get_button(self, name: str) -> Button:
		return self.__buttons(f'btn.name == "{name}"')[0]

	def get_buttons(self, group: str) -> Sequence[Button]:
		return self.__buttons(f'btn.group_name == "{group}"')

	def get_cell(self, source: CellType) -> CellType:
		grids = [self.view, self.plane]
		if isinstance(source, CellRenderer):
			grids.reverse()
		return grids[1].cells[grids[0].get_coordinates(source)]

	def set_mode(
			self,
			name: Optional[str] = None,
			index: Optional[int] = None,
			key: Optional[int] = None,
	):
		button = None
		if name is not None:
			button = self.get_button(name)
		elif key is not None:
			index = mode_keys.index(key)
		if index is not None:
			button = self.get_buttons('mode')[index]
		if button is not None:
			button.enable()

	def set_view(self, s: str = ''):
		if s == '':
			s = '0,' * (self.grid.dimensions - 2) + '*,*'
			self.input_boxes[0].text = s
		self.coordinates = tuple([int(x) for x in s.replace('*', '-1').split(',')])
		axes, mapped = [], []
		for i, c in enumerate(self.coordinates):
			(mapped if c < 0 else axes).append(i)
		coord = tuple([min(c, self.plane.size - 1) for c in self.coordinates if c > -1])
		if len(mapped) != 2:
			raise ValueError('coordinates must have exactly 2 "*"s')
		self.view.cells = self.grid.cells.transpose(axes + mapped)[coord]

	def tick(self):
		if not self.loaded:
			self.screen = display.set_mode(size=self.size, flags=RESIZABLE)
			self.loaded = True
		self.plane.render()
		self.screen.fill(Colors.WHITE)
		self.screen.blit(self.plane.surface, self.plane.rect)
		for element in self.elements:
			element.draw(self.screen, self.rendering.font)
		display.flip()
