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
    """
    Retry an async callable with exponential backoff + jitter.
    Uses SystemRandom to avoid Bandit B311; mypy-friendly with final raise.
    """
    for attempt in range(retries):
        try:
            return await fn()
        except Exception:
            if attempt == retries - 1:
                raise
            backoff = base_delay * (2**attempt)
            jitter = _RNG.random()
            delay = min(backoff + jitter, max_delay) if max_delay else backoff + jitter
            await asyncio.sleep(delay)

    raise RuntimeError("retry_async exhausted without returning")
