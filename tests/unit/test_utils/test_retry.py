import pytest
from unittest.mock import AsyncMock, patch
from app.utils.retry import retry_async

@pytest.mark.asyncio
async def test_retry_success_on_first_try():
    mock_fn = AsyncMock(return_value="✅ OK")
    result = await retry_async(mock_fn)
    assert result == "✅ OK"
    assert mock_fn.call_count == 1

@pytest.mark.asyncio
async def test_retry_success_after_retries():
    mock_fn = AsyncMock(side_effect=[Exception("Fail"), Exception("Fail again"), "🎉 Success"])
    result = await retry_async(mock_fn, retries=3, base_delay=0)
    assert result == "🎉 Success"
    assert mock_fn.call_count == 3

@pytest.mark.asyncio
async def test_retry_fails_after_all_attempts():
    mock_fn = AsyncMock(side_effect=Exception("💥 Always fails"))
    with pytest.raises(Exception, match="💥 Always fails"):
        await retry_async(mock_fn, retries=3, base_delay=0)
    assert mock_fn.call_count == 3

@pytest.mark.asyncio
@patch("asyncio.sleep", new_callable=AsyncMock)
async def test_retry_waits_between_attempts(mock_sleep):
    # Fail 2 times, succeed on 3rd
    mock_fn = AsyncMock(side_effect=[Exception(), Exception(), "Done"])
    result = await retry_async(mock_fn, retries=3, base_delay=0.1)
    assert result == "Done"
    assert mock_sleep.call_count == 2 
