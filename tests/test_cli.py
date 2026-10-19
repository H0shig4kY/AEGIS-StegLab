from unittest.mock import patch

from aegis.cli import get_password


def test_interactive_password_uses_getpass_and_returns_password():
    with patch("aegis.cli.getpass.getpass", return_value="not-echoed") as prompt:
        assert get_password() == "not-echoed"
    prompt.assert_called_once_with("Password      : ")


def test_interactive_password_rejects_empty_value():
    with patch("aegis.cli.getpass.getpass", return_value=""):
        assert get_password() is None
