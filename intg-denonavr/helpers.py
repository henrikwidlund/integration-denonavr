"""
Helper functions.

:copyright: (c) 2023 by Unfolded Circle ApS.
:license: Mozilla Public License Version 2.0, see LICENSE for more details.
"""

from typing import Any, Callable
import time
import asyncio
import functools


def key_update_helper(key: str, value: str | None, attributes: dict, original_attributes: dict[str, Any]):
    """Update the attributes dictionary with the given key and value."""
    if value is None:
        return attributes

    if key in original_attributes:
        if original_attributes[key] != value:
            attributes[key] = value
    else:
        attributes[key] = value

    return attributes


def timeit(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to measure execution time of both sync and async callables.

    If the wrapped function's module defines a `_LOG` logger variable it will be used to
    emit a debug message with the function qualified name and elapsed time. Otherwise
    the timing is a no-op (just returns the result).
    """

    is_coro = asyncio.iscoroutinefunction(func)

    @functools.wraps(func)
    async def _async_wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return await func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            logger = getattr(func, "__globals__", {}).get("_LOG")
            if logger is not None:
                # use qualname to include class when present (e.g. Class.method)
                logger.debug("%s took %.6fs", func.__qualname__, elapsed)

    @functools.wraps(func)
    def _sync_wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            logger = getattr(func, "__globals__", {}).get("_LOG")
            if logger is not None:
                logger.debug("%s took %.6fs", func.__qualname__, elapsed)

    return _async_wrapper if is_coro else _sync_wrapper
