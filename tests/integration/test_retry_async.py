import pytest
from app.utils.retry import retry_async

@pytest.mark.asyncio
async def test_retry_async_success_after_failure():
    """
    Թեստում ենք, որ եթե առաջին փորձը ձախողվի, բայց երկրորդը հաջող լինի՝
    ֆունկցիան վերականգնվում է:
    """
    calls = []

    async def unstable_function():
        calls.append("call")
        if len(calls) < 2:
            raise RuntimeError("Առաջին փորձը ձախողվեց")
        return "Երկրորդից հաջողվեց"

    result = await retry_async(unstable_function, retries=3, base_delay=0)
    assert result == "Երկրորդից հաջողվեց"
    assert len(calls) == 2  # առաջինը fail, երկրորդը OK

@pytest.mark.asyncio
async def test_retry_async_failure_all_attempts():
    """
    Թեստում ենք, որ եթե բոլոր փորձերը ձախողվում են, վերջինում կբարձրացվի սխալ:
    """
    async def always_fail():
        raise RuntimeError("Շարունակ ձախողում է")

    with pytest.raises(RuntimeError, match="Շարունակ ձախողում է"):
        await retry_async(always_fail, retries=3, base_delay=0)

