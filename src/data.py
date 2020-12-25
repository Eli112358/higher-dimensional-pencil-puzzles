import numpy as np

from src.tuple_util import formula


class Data(np.object):

	def __init__(self, cell):
		self.cell = cell
		self.given = False
		self.value = None
		self.candidates = PencilMarks(self)  # center
		self.contingencies = PencilMarks(self)  # corner

	def set_given(self, value):
		self.value = value
		self.given = value is not None

	def set_guess(self, value):
		if not self.given:
			self.value = value


class PencilMarks(list):

	def __init__(self, data):
		self.data = data
		super().__init__([False] * (self.data.cell.grid.size + 1))

	def fill(self, value):
		for digit in range(len(self)):
			self.set(digit, value)

	def set(self, digit, value=True):
		self[digit] = value

	def toggle(self, digit):
		self[digit] = not self[digit]


class Regioning:

	def __init__(self, regular=True, size=None):
		self.regular = regular
		self._size = size
		if self.regular:
			self._size = (3, 3)

	def load(self, file):
		# implement later to support irregular sudoku
		pass

	def size(self, scale=1, extra=0):
		return formula(self._size, scale, extra)
