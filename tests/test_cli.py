from unittest import mock
import os

import pytest
from personalcli.main import main


@mock.patch.dict(os.environ, {'PERSONALCLI_GOOGLE_API_KEY': 'your_mocked_api_key'})
@mock.patch("getpass.getuser")
@mock.patch("personalcli.main.typer")
@mock.patch("personalcli.main.query_gemini")
def test_main_with_interactive(qg_mock, typer_mock, getuser_mock):
    # GIVEN
    question = "Any question?"
    response = "Hello, Gemini!"
    interactive_mode = True
    qg_mock.return_value = response
    getuser_mock.return_value = "user Z"
    typer_mock.prompt.side_effect = [KeyboardInterrupt]

    # WHEN
    with pytest.raises(KeyboardInterrupt):
        main(question, interactive=interactive_mode)

    # THEN
    typer_mock.style.assert_any_call(f" {response}\n", fg=typer_mock.colors.BRIGHT_GREEN)
    typer_mock.style.assert_any_call(f"\n{getuser_mock.return_value}:", bold=True, fg=typer_mock.colors.BRIGHT_CYAN)
    typer_mock.style.assert_any_call(f"\n Algo mais {getuser_mock.return_value}?  (CTRL + C para encerrar)\n", bold=True, fg=typer_mock.colors.BRIGHT_GREEN)


@mock.patch.dict(os.environ, {'PERSONALCLI_GOOGLE_API_KEY': 'your_mocked_api_key'})
@mock.patch("getpass.getuser")
@mock.patch("personalcli.main.typer")
@mock.patch("personalcli.main.query_gemini")
def test_main_wo_interactive(qg_mock, typer_mock, getuser_mock):
    # GIVEN
    question = "Any question?"
    response = "Hello, Gemini!"
    interactive_mode = False
    qg_mock.return_value = response
    getuser_mock.return_value = "user Z"

    # WHEN
    main(question, interactive=interactive_mode)

    # THEN
    typer_mock.style.assert_any_call(f" {response}\n", fg=typer_mock.colors.BRIGHT_GREEN)
    typer_mock.style.assert_any_call(f"\n{getuser_mock.return_value}:", bold=True, fg=typer_mock.colors.BRIGHT_CYAN)
    typer_mock.prompt.assert_not_called()