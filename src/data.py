from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
	from grid import Cell


class Data(np.object):

	def __init__(self, cell: Cell):
		self.cell = cell
		self.given = False
		self.value = ''
		self.candidates = PencilMarks(self)  # center
		self.contingencies = PencilMarks(self)  # corner

	def set_given(self, value: int):
		self.value = value
		self.given = value != ''

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
