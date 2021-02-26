from __future__ import annotations

from typing import (
	Callable,
	TYPE_CHECKING,
)

import pygame as pg
from pygame import Surface
from pygame.font import Font

from rendering import Colors

if TYPE_CHECKING:
	from rendering.renderer import Renderer


class InputBox:
	# Derived from the object-oriented variant at https://stackoverflow.com/a/46390412/2640292

	def __init__(
			self,
			renderer: Renderer,
			rect: pg.Rect,
			callback: Callable,
			reset: bool = True,
			text: str = '',
	):
		self.active = False
		self.callback = callback
		self.rect = rect
		self.renderer = renderer
		self.reset = reset
		self.surface = pg.Surface((self.rect.w, self.rect.h))
		self.text = text
		self.txt_surface = self.font.render(self.text, True, Colors.BLACK)

	@property
	def color(self):
		return Colors.PENCIL if self.active else Colors.BLACK

	@property
	def font(self):
		return self.renderer.rendering.font

	def handle_event(self, event):
		if event.type == pg.MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				self.active = not self.active
			else:
				self.active = False
				self.callback(self.text)
		if event.type == pg.KEYDOWN:
			if self.active:
				if event.key == pg.K_RETURN:
					self.callback(self.text)
					if self.reset:
						self.text = ''
				elif event.key == pg.K_BACKSPACE:
					self.text = self.text[:-1]
				elif event.key == pg.K_ESCAPE:
					self.text = ''
				else:
					self.text += event.unicode

	def draw(self, screen: Surface, font: Font):
		self.txt_surface = font.render(self.text, True, Colors.BLACK)
		self.rect.w = max(200, self.txt_surface.get_width() + 10)
		screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
		pg.draw.rect(screen, self.color, self.rect, 5)
