import asyncio
import random

async def retry_async(fn, retries=3, base_delay=1):
    for attempt in range(retries):
        try:
            return await fn()
        except Exception as e:
            if attempt == retries - 1:
                raise e
            delay = base_delay * 2 ** attempt + random.random()
            await asyncio.sleep(delay)
