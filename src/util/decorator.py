from functools import wraps
from typing import Callable


def decorator_with_args(old_decorator: Callable):
	def decorator(*args, **kwargs):
		@wraps(old_decorator)
		def decorated(callback: Callable):
			new_callback = old_decorator(callback, *args, **kwargs)
			if not hasattr(old_decorator, 'decorators'):
				old_decorator.decorators = []
			new_callback.decorators = old_decorator.decorators
			if decorator not in new_callback.decorators:
				new_callback.decorators.append(decorator)
			return new_callback
		return decorated
	return decorator
