from typing import (
	Callable,
	ForwardRef,
	Iterable,
	Optional,
	Tuple,
	Union,
)

from numpy import (
	empty,
	ndarray,
	ndenumerate,
	nditer,
)

from grid.constants import (
	INIT_EMPTY,
	POPULATE,
)
from rendering import Size
from util.tuple import formula

Coordinates = Tuple[int, ...]
Flags = Optional[Iterable[str]]


class Regioning:

	def __init__(
			self,
			regular: bool = True,
			shape: Tuple[int, int] = None,
	):
		self.grid = None
		self.regular = regular
		self.shape = shape

	def load(self, file):
		# implement later to support irregular sudoku
		pass

	def size(self, scale: Size = (1, 1), extra: Size = (0, 0)) -> Size:
		return formula(lambda ss, s, e: (ss * s) + e, self.shape, scale, extra)


class Cell:

	def __init__(self, grid: ForwardRef('Grid')):
		self.grid = grid


class Grid:

	def __init__(
			self,
			dimensions: int,
			regioning: Union[int, Regioning],
			cell_type: Optional[Callable] = None,
			cells: Optional[ndarray] = None,
			flags: Flags = None,
	):
		if flags is None:
			flags = []
		self.cells = cells
		if type(regioning) is not int:
			self.regioning = regioning
			self.regioning.grid = self
		if any([
			cell_type is not None,
			INIT_EMPTY in flags,
			POPULATE in flags,
		]):
			size = regioning if type(regioning) is int else (shape := regioning.shape)[0] * shape[1]
			self.cells = empty([size] * dimensions, cell_type)
			self.populate(cell_type)

	@property
	def dimensions(self) -> int:
		return self.cells.ndim

	@property
	def enumerator(self) -> ndenumerate:
		return ndenumerate(self.cells)

	@property
	def size(self) -> int:
		return self.cells.shape[0]

	def get_coordinates(self, target: Cell) -> Coordinates:
		for coordinates, cell in self.enumerator:
			if cell == target:
				return coordinates
		raise KeyError('target cell is not in grid')

	def iterator(self, flags: Flags = None, op_flags: Flags = None) -> nditer:
		if flags is None:
			flags = ['refs_ok']
		if op_flags is None:
			op_flags = ['readonly']
		return nditer(self.cells, flags=flags, op_flags=op_flags)

	def populate(self, cell_type: Callable):
		for cell in self.iterator(op_flags=['writeonly']):
			cell[...] = cell_type(self)
