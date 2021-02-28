from enum import Enum
from typing import Optional

from pygame import (
	Color,
	Rect,
	Surface,
	font as fonts,
)


class Center(str, Enum):
	HORIZONTAL = 'top'
	VERTICAL = 'left'


def center(source: Surface, dest: Surface, axes: Optional[Center]) -> Rect:
	rect = source.get_rect()
	rect.center = dest.get_rect().center
	if axes is not None:
		exec(f'rect.{axes} = source.get_rect().{axes}')
	return rect


def blit_center(source: Surface, dest: Surface, axes: Optional[Center]):
	dest.blit(source, center(source, dest, axes))


def render_text(font: str, text: str, size: int, color: Color) -> Surface:
	return fonts.SysFont(font, size).render(text, True, color)
