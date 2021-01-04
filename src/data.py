from __future__ import annotations

from typing import Tuple, TYPE_CHECKING

import numpy as np

from src.tuple_util import formula

if TYPE_CHECKING:
	from grid import Cell


class Data(np.object):

	def __init__(self, cell: Cell):
		self.cell = cell
		self.given = False
		self.value = None
		self.candidates = PencilMarks(self)  # center
		self.contingencies = PencilMarks(self)  # corner

	def set_given(self, value: int):
		self.value = value
		self.given = value is not None

	def set_guess(self, value: int):
		if not self.given:
			self.value = value


class PencilMarks(list):

	def __init__(self, data: Data):
		self.data = data
		super().__init__([False] * (self.data.cell.grid.size + 1))

	def fill(self, value: bool):
		for digit in range(len(self)):
			self.set(digit, value)

	def set(self, digit: int, value: bool = True):
		self[digit] = value

	def toggle(self, digit: int):
		self[digit] = not self[digit]


class Regioning:

	def __init__(self, regular: bool = True, size: Tuple[int, int] = None):
		self.regular = regular
		self._size = size
		if self.regular:
			self._size = (3, 3)

	def load(self, file):
		# implement later to support irregular sudoku
		pass

	def size(self, scale: Tuple[int, int] = (1, 1), extra: Tuple[int, int] = (0, 0)):
		return formula(self._size, scale, extra, lambda ss, s, e: (ss * s) + e)
