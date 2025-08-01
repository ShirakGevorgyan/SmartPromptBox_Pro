from unittest.mock import patch, MagicMock
from app.llm import img_generator
import os

@patch("app.llm.img_generator.requests.get")
@patch("app.llm.img_generator.client")
def test_generate_image(mock_client, mock_requests):
    
    mock_client.images.generate.return_value.data = [
        MagicMock(url="https://fakeimage.com/image1.png")
    ]

    mock_requests.return_value.content = b"FAKE_IMAGE_BYTES"

    file_path = img_generator.generate_image("A castle on a cliff at night")

    assert file_path.startswith("images/")
    assert file_path.endswith(".png")

    assert os.path.exists(file_path)

    os.remove(file_path)
