from unittest.mock import AsyncMock, patch

import pytest
from scores_reader import APIClient


@pytest.mark.asyncio
@patch("httpx.AsyncClient.post", new_callable=AsyncMock)
async def test_post_success(mock_post):
    # Setup mock response:
    """
    @patch("httpx.AsyncClient.post", new_callable=AsyncMock)
    This decorator replaces the post method of httpx.AsyncClient with an AsyncMock.
    This means when APIClient.post calls httpx.AsyncClient.post,
    it actually calls this mock, letting the test control the response
    :param mock_post:
    :return:
    """
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.text = "Success"
    mock_response.raise_for_status = AsyncMock()
    mock_post.return_value = mock_response

    client = APIClient(base_url="https://example.com/")
    result = await client.post({"key": "value"})

    assert result == "Success"


@pytest.mark.asyncio
@patch("httpx.AsyncClient.post", new_callable=AsyncMock)
async def test_post_failure(mock_post):
    # Setup mock response
    mock_response = AsyncMock()
    mock_response.status_code = 404
    mock_response.reason_phrase = "Not Found"
    mock_response.raise_for_status.side_effect = Exception("404 Not Found")
    mock_post.return_value = mock_response

    client = APIClient(base_url="https://example.com/")

    with pytest.raises(Exception) as exc_info:
        await client.post({"key": "value"})

    assert "Failed to fetch data" in str(exc_info.value)
