"""Async retry utility with exponential backoff and jitter.

- Uses `SystemRandom` to avoid Bandit B311 (non-crypto RNG in security contexts).
- Type-annotated for mypy; re-raises the last exception after exhausting retries.
- Suitable for wrapping transient network calls (LLM API, HTTP requests, etc.).
"""

import asyncio
from typing import Awaitable, Callable, Optional, TypeVar
from random import SystemRandom

T = TypeVar("T")
_RNG = SystemRandom()


async def retry_async(
    fn: Callable[[], Awaitable[T]],
    retries: int = 3,
    base_delay: float = 1.0,
    max_delay: Optional[float] = 8.0,
) -> T:
    """Retry an async callable with exponential backoff + jitter.

    Args:
        fn: Zero-arg async callable to execute.
        retries: Maximum number of attempts (>=1).
        base_delay: Initial delay (seconds) for the first retry.
        max_delay: Upper bound for the computed delay (None = unbounded).

    Returns:
        The awaited return value from `fn` once it succeeds.

    Raises:
        Exception: Re-raises the last exception from `fn` if all attempts fail.
    """
    for attempt in range(retries):
        try:
            return await fn()
        except Exception:
            if attempt == retries - 1:
                # Final attempt failed: re-raise original exception.
                raise
            backoff = base_delay * (2**attempt)
            jitter = _RNG.random()
            delay = min(backoff + jitter, max_delay) if max_delay else backoff + jitter
            await asyncio.sleep(delay)

    # Defensive: mypy-friendly guard (should never be reached).
    raise RuntimeError("retry_async exhausted without returning")
