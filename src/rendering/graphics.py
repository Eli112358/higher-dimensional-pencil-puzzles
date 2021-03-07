from enum import Enum
from typing import Optional

from pygame import (
	Color,
	Rect,
	SRCALPHA,
	Surface,
	draw,
	font as fonts,
)


class Center(str, Enum):
	HORIZONTAL = 'top'
	VERTICAL = 'left'


def center(source: Surface, dest: Surface, axes: Optional[Center] = None) -> Rect:
	rect = source.get_rect()
	rect.center = dest.get_rect().center
	if axes is not None:
		exec(f'rect.{axes} = source.get_rect().{axes}')
	return rect


def blit_center(source: Surface, dest: Surface, axes: Optional[Center] = None):
	dest.blit(source, center(source, dest, axes))


def new_surface(size: Optional[int] = 40) -> Surface:
	return Surface((size, size), SRCALPHA)


def render_text(font: str, text: str, size: int, color: Color) -> Surface:
	return fonts.SysFont(font, size).render(text, True, color)


class ModeButton:
	corner_formulae = [
		'(m, m)',
		'(r.w - tr[1].w - m, m)',
		'(m, r.h - tr[2].h - m)',
	]

	@staticmethod
	def __common(
			color: Color,
			texting: Optional[tuple[str, str, int]] = None
	) -> Surface:
		surf = new_surface()
		if texting is not None:
			blit_center(render_text(*texting, color), surf)
		draw.rect(surf, color, (2, 2, 36, 36), 3)
		return surf

	@staticmethod
	def center(font: str, color: Color) -> Surface:
		return ModeButton.__common(color, (font, '12', 25))

	@staticmethod
	def color(font: str, color: Color) -> Surface:
		return ModeButton.__common(color, (font, 'color', 15))

	@staticmethod
	def corner(font: str, color: Color) -> Surface:
		surf = ModeButton.__common(color)
		text = [render_text(font, str(i + 1), 21, color) for i in range(3)]
		tr = [t.get_rect() for t in text]
		m = 6  # m for margin
		r = surf.get_rect()
		coord = [eval(f, loc) for loc in (locals(),) for f in ModeButton.corner_formulae]
		surf.blits(zip(text, coord), False)
		return surf

	@staticmethod
	def digit(font: str, color: Color) -> Surface:
		return ModeButton.__common(color, (font, '9', 55))
