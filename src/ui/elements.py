from __future__ import annotations

from enum import auto
from typing import (
	Callable,
	Optional,
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

from event import (
	EventHandler,
	event_handler,
)
from rendering import Colors
from rendering.graphics import (
	blit_center,
	render_text,
)
from util.enums import AutoName

if TYPE_CHECKING:
	from rendering.renderer import Renderer


class UIElement(EventHandler):

	def __init__(
			self,
			renderer: Renderer,
			name: str,
			rect: Rect,
			callback: Optional[Callable] = None,
	):
		super().__init__()
		self.callback = callback
		self.name = name
		self.rect = rect
		self.renderer = renderer

	def draw(self, screen: Surface, font: str):
		pass


class Button(UIElement):
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
		super().__init__(renderer, name, rect, callback)
		self.enabled = False
		self.graphic = graphic
		self.group_name = group
		self.type = btn_type

	@property
	def color(self) -> Color:
		return Colors.SELECTED if self.enabled else Colors.WHITE

	@property
	def group(self) -> list[Button]:
		return [btn for btn in self.renderer.buttons if btn.group_name is self.group_name]

	@event_handler(MOUSEBUTTONDOWN)
	def click(self, event: Event):
		if not self.rect.collidepoint(event.pos):
			return
		if self.type == Button.Type.TOGGLE:
			self.enabled = not self.enabled
		elif self.type == Button.Type.RADIO:
			self.enable()
		if self.callback is not None:
			self.callback()

	def draw(self, screen: Surface, _):
		background = Surface(self.rect.size)
		background.fill(self.color)
		blit_center(self.graphic, background)
		screen.blit(background, self.rect.topleft)
		drawing.rect(screen, Colors.BLACK, self.rect, 3)

	def enable(self):
		for btn in self.group:
			btn.enabled = False
		self.enabled = True


class InputBox(UIElement):
	# Derived from the object-oriented variant at https://stackoverflow.com/a/46390412/2640292

	def __init__(
			self,
			renderer: Renderer,
			name: str,
			rect: Rect,
			callback: Optional[Callable] = None,
			reset: Optional[bool] = True,
			text: Optional[str] = '',
	):
		super().__init__(renderer, name, rect, callback)
		self.active = False
		self.reset = reset
		self.surface = Surface((self.rect.w, self.rect.h))
		self.text = text

	@property
	def color(self):
		return Colors.SELECTED if self.active else Colors.WHITE

	@event_handler(MOUSEBUTTONDOWN)
	def click(self, event: Event):
		if self.rect.collidepoint(event.pos):
			self.active = not self.active
		else:
			self.active = False
			if self.callback is not None:
				self.callback(self.text)

	@event_handler(KEYDOWN)
	def key_press(self, event: Event):
		if not self.active:
			return
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

	def draw(self, screen: Surface, font: str):
		txt_surface = render_text(font, self.text, 50, Colors.BLACK)
		self.rect.w = max(200, txt_surface.get_width() + 10)
		background = Surface(self.rect.size)
		background.fill(self.color)
		background.blit(txt_surface, (5, 5))
		screen.blit(background, self.rect.topleft)
		drawing.rect(screen, Colors.BLACK, self.rect, 5)
