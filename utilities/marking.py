"""Utils specifically for testing"""

from functools import partial, wraps
from typing import Callable


class CustomMarker:
    """Function Marker"""

    marked_functions = {}

    @classmethod
    def __getattr__(cls, marker_name):
        return partial(cls._add_marker, marker_name)

    @classmethod
    def _add_marker(cls, marker_name: str, func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cls.marked_functions[marker_name].append(func)
            return func(*args, **kwargs)

        cls.marked_functions[marker_name] = func
        return wrapper
