from unittest import mock
import os

from personalcli.main import query_gemini


@mock.patch.dict(os.environ, {'PERSONALCLI_GOOGLE_API_KEY': 'your_mocked_api_key'})
@mock.patch("personalcli.main.genai.GenerativeModel")
def test_query_gemini(gm_mock):
    # GIVEN
    gm_mock.return_value.generate_content.return_value.text = "Hello, Gemini!"
    observer = gm_mock.return_value.generate_content

    # WHEN
    response = query_gemini("instruction: {message}", "Initial Question")

    # THEN
    observer.assert_called_once_with("instruction: Initial Question")
    assert response == "Hello, Gemini!"