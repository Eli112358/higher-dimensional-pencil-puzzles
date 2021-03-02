from enum import auto
from typing import Sequence, ForwardRef

from grid import (
	Cell,
	Grid,
	Regioning,
)
from keys import number_keys
from util.enums import AutoName


class SudokuCell(Cell):
	class Field(str, AutoName):
		CANDIDATE = auto()
		COLOR = auto()
		CONTINGENCY = auto()
		GUESS = auto()

		@staticmethod
		def error(name):
			return ValueError(f'{name} should be one of Cell.Field literals')

	def __init__(self, grid: ForwardRef('SudokuGrid')):
		super().__init__(grid)
		self.candidates = 0
		self.color = 0
		self.contingencies = 0
		self.given = False
		self.region = None
		self.value = ''

	def set_given(self, value: int):
		self.value = value
		self.given = value != ''

	def is_set(self, digit: int, field: Field) -> bool:
		_field = self.candidates if field == SudokuCell.Field.CANDIDATE else self.contingencies
		return _field & (1 << digit) > 0

	def convert(self, field: Field) -> Sequence[int]:
		return [n for n in range(len(number_keys) // 2) if self.is_set(n, field)]

	def clear(self):
		if self.given:
			return
		if self.value != '':
			self.value = ''
		elif self.color > 0:
			self.color = 0
		elif self.contingencies > 0:
			self.contingencies = 0
		elif self.candidates > 0:
			self.candidates = 0

	def set(self, digit: int, field: Field):
		bit = 1 << digit
		if field == SudokuCell.Field.GUESS:
			if not self.given:
				self.value = digit
		elif field == SudokuCell.Field.CANDIDATE:
			self.candidates |= bit
		elif field == SudokuCell.Field.CONTINGENCY:
			self.contingencies |= bit
		elif field == SudokuCell.Field.COLOR:
			pass
		else:
			raise SudokuCell.Field.error('field')

	def toggle(self, digit: int, field: Field):
		bit = 1 << digit
		if field == SudokuCell.Field.GUESS:
			if not self.given:
				self.value = '' if self.value == digit else digit
		elif field == SudokuCell.Field.CANDIDATE:
			self.candidates ^= bit
		elif field == SudokuCell.Field.CONTINGENCY:
			self.contingencies ^= bit
		elif field == SudokuCell.Field.COLOR:
			pass
		else:
			raise SudokuCell.Field.error('field')


class SudokuGrid(Grid):

	def __init__(
			self,
			dimensions: int = 2,
			regioning: Regioning = Regioning(),
	):
		self.regioning = regioning
		size = self.regioning.size()[0] * self.regioning.size()[1]
		super().__init__(dimensions, size, SudokuCell)
