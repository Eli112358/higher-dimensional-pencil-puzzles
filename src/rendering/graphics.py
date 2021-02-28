from pygame import (
	Color,
	font as fonts,
	Surface,
)


def render_text(font: str, text: str, size: int, color: Color) -> Surface:
	return fonts.SysFont(font, size).render(text, True, color)
