import numpy as np
import pygame as pg
from pygame import Color, Surface, SRCALPHA

from tuple_util import formula


class Colors:
	BLACK = (0, 0, 0)
	PENCIL = (29, 106, 229)
	WHITE = (255, 255, 255)


class Rendering:

	def __init__(self, font, colors, cell_size, width):
		self.cell_size = cell_size
		self.colors = colors
		self.font = font
		self.width = width
		self.empty = Color(0, 0, 0, 0)

	def size(self, scale=1, margin=0):
		return formula(self.cell_size, scale, margin)


class Renderer:

	def __init__(self, grid, screen_size):
		self.grid = grid
		self.screen = pg.display.set_mode(screen_size)
		self.dirty = []
		self.loaded = False

	def load(self):
		self.screen.fill(Colors.WHITE)
		width = self.grid.rendering.width
		size = self.grid.rendering.cell_size
		for cell in self.grid.cells_iter(flags=['refs_ok'], op_flags=['readonly']):
			pg.draw.rect(cell[()].surfaces.background, Colors.BLACK, (0, 0, size, size), width)
		plane = self.grid.sub_grid([(0, 0)])
		cells_enum = np.ndenumerate(plane.cells)
		surfs = [(cell.surfaces.background, (i*size, j*size)) for (i, j), cell in cells_enum]
		self.dirty += self.screen.blits(surfs, doreturn=True)
		self.loaded = True

	def tick(self):
		if not self.loaded:
			self.load()
		if len(self.dirty):
			pg.display.update(self.dirty.pop(0))


class PencilMarks:

	def __init__(self, surfaces):
		self.surfaces = surfaces
		self.center = Surface(self.surfaces.size, flags=SRCALPHA)
		self.corner = Surface(self.surfaces.size, flags=SRCALPHA)


class Surfaces:
	
	def __init__(self, cell):
		self.cell = cell
		self.background = Surface(self.size, flags=SRCALPHA)
		self.selected = Surface(self.size, flags=SRCALPHA)
		self.value = Surface(self.size, flags=SRCALPHA)
		self.pencil_marks = PencilMarks(self)

	@property
	def color(self):
		return self.cell.grid.rendering.colors[int(self.cell.data.given)]

	@property
	def font(self):
		return self.cell.grid.rendering.font

	@property
	def size(self):
		return self.cell.grid.rendering.size()

	def clear(self):
		self.value.fill(self.cell.grid.rendering.empty)

	def render(self):
		text = self.font.render(str(self.cell.data.value), 1, self.color)
		self.value.blit(text, (0, 0))
