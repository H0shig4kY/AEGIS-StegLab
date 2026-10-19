from pathlib import Path
from unittest.mock import patch

from utils.helpers import creatfile, readfile


def test_readfile_preserves_utf8_and_line_endings(tmp_path):
    source = tmp_path / "input.txt"
    source.write_bytes("Olá\r\nStegLab\n".encode("utf-8"))
    assert readfile(str(source)) == "Olá\r\nStegLab\n"


def test_readfile_rejects_oversized_data_before_decoding(tmp_path, capsys):
    source = tmp_path / "large.txt"
    source.write_bytes(b"A" * 9)
    assert readfile(str(source), max_bytes=8) is None
    assert "exceeds the 8-byte limit" in capsys.readouterr().out


def test_creatfile_atomically_replaces_output(tmp_path):
    output = tmp_path / "result.txt"
    output.write_text("old", encoding="utf-8")
    assert creatfile("new\x00payload", output) is True
    assert output.read_bytes() == b"new\x00payload"


def test_creatfile_failure_preserves_output_and_cleans_temporary_file(tmp_path):
    output = tmp_path / "result.txt"
    output.write_text("old", encoding="utf-8")
    with patch("utils.helpers.os.replace", side_effect=OSError("simulated failure")):
        assert creatfile("new", output) is False
    assert output.read_text(encoding="utf-8") == "old"
    assert list(tmp_path.glob(".result.txt.*.tmp")) == []
