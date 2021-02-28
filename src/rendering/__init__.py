from enum import Enum
from typing import (
	List,
	Tuple,
	Union,
)

from pygame import Color
from pygame.font import Font

from util.tuple import formula

Size = Union[int, Tuple[int, int]]


class Colors(Color, Enum):
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
