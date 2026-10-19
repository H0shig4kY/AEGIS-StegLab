from unittest.mock import patch
import pytest

from aegis.cli import get_password


def test_interactive_password_uses_getpass_and_returns_password():
    with patch("aegis.cli.getpass.getpass", return_value="not-echoed") as prompt:
        assert get_password() == "not-echoed"
    prompt.assert_called_once_with("Password      : ")


def test_interactive_password_rejects_empty_value():
    with patch("aegis.cli.getpass.getpass", return_value=""):
        assert get_password() is None


def test_wrong_aes_password_does_not_create_output_file(tmp_path, monkeypatch):
    from aegis import cli
    from crypto.aes import encrypt

    encrypted_file = tmp_path / "encrypted.txt"
    output_file = tmp_path / "must-not-exist.txt"
    encrypted_file.write_text(encrypt("secret", "right password"), encoding="utf-8")
    inputs = iter(["2", str(encrypted_file), "4", str(output_file), "5"])
    output_writes = []
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(inputs))
    monkeypatch.setattr(cli.getpass, "getpass", lambda _prompt="": "wrong password")
    real_writer = cli.creatfile

    def tracked_writer(content, destination):
        output_writes.append(destination)
        return real_writer(content, destination)

    monkeypatch.setattr(cli, "creatfile", tracked_writer)

    with pytest.raises(SystemExit):
        cli.Main()

    assert not output_file.exists()
    assert output_writes == []
