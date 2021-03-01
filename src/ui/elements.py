from __future__ import annotations

from typing import (
	Callable,
	Optional,
	TYPE_CHECKING,
)

import pygame as pg
from pygame import Surface
from pygame.event import Event

from rendering import Colors
from rendering.graphics import render_text

if TYPE_CHECKING:
	from rendering.renderer import Renderer


class InputBox:
	# Derived from the object-oriented variant at https://stackoverflow.com/a/46390412/2640292

	def __init__(
			self,
			renderer: Renderer,
			rect: pg.Rect,
			callback: Optional[Callable] = None,
			reset: Optional[bool] = True,
			text: Optional[str] = '',
	):
		self.active = False
		self.callback = callback
		self.rect = rect
		self.renderer = renderer
		self.reset = reset
		self.surface = pg.Surface((self.rect.w, self.rect.h))
		self.text = text

	@property
	def color(self):
		return Colors.PENCIL if self.active else Colors.BLACK

	@property
	def font(self):
		return self.renderer.rendering.font

	def draw(self, screen: Surface, font: str):
		txt_surface = render_text(font, self.text, 50, Colors.BLACK)
		self.rect.w = max(200, txt_surface.get_width() + 10)
		background = Surface(self.rect.size)
		background.fill(self.color)
		background.blit(txt_surface, (5, 5))
		screen.blit(background, self.rect.topleft)
		pg.draw.rect(screen, Colors.BLACK, self.rect, 5)

	def handle_event(self, event: Event):
		if event.type == pg.MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				self.active = not self.active
			else:
				self.active = False
				if self.callback is not None:
					self.callback(self.text)
		if event.type == pg.KEYDOWN:
			if self.active:
				if event.key in [pg.K_RETURN, pg.K_KP_ENTER]:
					self.callback(self.text)
					if self.reset:
						self.text = ''
					self.active = False
				elif event.key == pg.K_BACKSPACE:
					self.text = self.text[:-1]
				elif event.key == pg.K_ESCAPE:
					self.text = ''
				else:
					self.text += event.unicode
