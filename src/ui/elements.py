from __future__ import annotations

from enum import auto
from typing import (
	Callable,
	Optional,
	Sequence,
	TYPE_CHECKING,
)

from pygame import (
	Color,
	KEYDOWN,
	K_BACKSPACE,
	K_ESCAPE,
	K_KP_ENTER,
	K_RETURN,
	MOUSEBUTTONDOWN,
	Rect,
	Surface,
	draw as drawing,
)
from pygame.event import Event

from rendering import Colors
from rendering.graphics import (
	blit_center,
	render_text,
)
from util.enums import AutoName

if TYPE_CHECKING:
	from rendering.renderer import Renderer


class Button:
	class Type(str, AutoName):
		RADIO = auto()
		SIMPLE = auto()
		TOGGLE = auto()

	def __init__(
			self,
			renderer: Renderer,
			name: str,
			rect: Rect,
			graphic: Surface,
			callback: Optional[Callable] = None,
			btn_type: Optional[Type] = Type.SIMPLE,
			group: Optional[str] = '',
	):
		self.callback = callback
		self.enabled = False
		self.graphic = graphic
		self.group = group
		self.name = name
		self.rect = rect
		self.renderer = renderer
		self.type = btn_type

	@property
	def color(self) -> Color:
		return Colors.SELECTED if self.enabled else Colors.WHITE

	def draw(self, screen: Surface):
		background = Surface(self.rect.size)
		background.fill(self.color)
		blit_center(self.graphic, background)
		screen.blit(background, self.rect.topleft)
		drawing.rect(screen, Colors.BLACK, self.rect, 3)

	def enable(self):
		for btn in self.get_group():
			btn.enabled = False
		self.enabled = True

	def get_group(self) -> Sequence[Button]:
		return [btn for btn in self.renderer.buttons if btn.group is self.group]

	def handle_event(self, event: Event):
		if event.type == MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				if self.type == Button.Type.TOGGLE:
					self.enabled = not self.enabled
				elif self.type == Button.Type.RADIO:
					self.enable()
				if self.callback is not None:
					self.callback()


class InputBox:
	# Derived from the object-oriented variant at https://stackoverflow.com/a/46390412/2640292

	def __init__(
			self,
			renderer: Renderer,
			rect: Rect,
			callback: Optional[Callable] = None,
			reset: Optional[bool] = True,
			text: Optional[str] = '',
	):
		self.active = False
		self.callback = callback
		self.rect = rect
		self.renderer = renderer
		self.reset = reset
		self.surface = Surface((self.rect.w, self.rect.h))
		self.text = text

	@property
	def color(self):
		return Colors.SELECTED if self.active else Colors.WHITE

	def draw(self, screen: Surface, font: str):
		txt_surface = render_text(font, self.text, 50, Colors.BLACK)
		self.rect.w = max(200, txt_surface.get_width() + 10)
		background = Surface(self.rect.size)
		background.fill(self.color)
		background.blit(txt_surface, (5, 5))
		screen.blit(background, self.rect.topleft)
		drawing.rect(screen, Colors.BLACK, self.rect, 5)

	def handle_event(self, event: Event):
		if event.type == MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				self.active = not self.active
			else:
				self.active = False
				if self.callback is not None:
					self.callback(self.text)
		if event.type == KEYDOWN:
			if self.active:
				if event.key in [K_RETURN, K_KP_ENTER]:
					self.callback(self.text)
					if self.reset:
						self.text = ''
					self.active = False
				elif event.key == K_BACKSPACE:
					self.text = self.text[:-1]
				elif event.key == K_ESCAPE:
					self.text = ''
				else:
					self.text += event.unicode
