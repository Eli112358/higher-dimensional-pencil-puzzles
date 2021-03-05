from functools import wraps
from typing import Callable

from pygame.event import Event

from util.decorator import decorator_with_args


@decorator_with_args
def event_handler(callback: Callable, event_type: int):
	@wraps(callback)
	def decorated(*args):
		callback(*args)
	decorated.type = event_type
	return decorated


class EventHandler:

	def __init__(self):
		self.handlers = self.get_handlers(self.__class__)

	@staticmethod
	def get_handlers(cls):
		return {h.type: h for h in cls.__dict__.values() if hasattr(h, 'decorators') and event_handler in h.decorators}

	def handle(self, event: Event):
		handlers = self.handlers
		if event.type in handlers:
			handler = handlers[event.type]
			handler(self, event)
