from unittest.mock import patch, MagicMock
from app.llm import img_generator
import os

# ✅ Test generate_image function
@patch("app.llm.img_generator.requests.get")
@patch("app.llm.img_generator.client")
def test_generate_image(mock_client, mock_requests):
    # Mock image URL return
    mock_client.images.generate.return_value.data = [
        MagicMock(url="https://fakeimage.com/image1.png")
    ]

    # Mock requests.get().content
    mock_requests.return_value.content = b"FAKE_IMAGE_BYTES"

    # Actual test
    file_path = img_generator.generate_image("A castle on a cliff at night")

    # ✅ Check path validity
    assert file_path.startswith("images/")
    assert file_path.endswith(".png")

    # ✅ Check that file was saved
    assert os.path.exists(file_path)

    # ✅ Clean up after test
    os.remove(file_path)
