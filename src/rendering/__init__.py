from enum import Enum
from typing import (
	Tuple,
	Union,
)

from pygame import Color

from util.tuple import formula

Size = Union[int, Tuple[int, int]]


class Colors(Color, Enum):
	BLACK = (0, 0, 0)
	EMPTY = (0, 0, 0, 0)
	PENCIL = (29, 106, 229)
	SELECTED = (230, 217, 48, 128)
	WHITE = (255, 255, 255)


class Rendering:

	def __init__(
			self,
			cell_size: int,
			font: str,
			width: int,
	):
		self.cell_size = cell_size
		self.font = font
		self.width = width

	def size(self, scale: Size = (1, 1), margin: Size = (0, 0)) -> Tuple[int, int]:
		return formula(lambda cs, s, m: (cs * s) + m, self.cell_size, scale, margin)
