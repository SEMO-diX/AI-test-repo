from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.verify_workspace import _scan_text, _sensitive_filename, validate_file


class VerifyWorkspaceTests(unittest.TestCase):
    def test_private_key_marker_is_detected(self) -> None:
        marker = "-----BEGIN " + "PRIVATE KEY-----"
        self.assertIn("private key", _scan_text(marker))

    def test_github_token_shape_is_detected(self) -> None:
        token = "gh" + "p_" + ("A" * 24)
        self.assertIn("GitHub token", _scan_text(token))

    def test_sensitive_filename_is_rejected(self) -> None:
        self.assertTrue(_sensitive_filename(Path(".env")))
        self.assertTrue(_sensitive_filename(Path("client.pem")))
        self.assertFalse(_sensitive_filename(Path(".env.example")))

    def test_binary_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "payload.bin"
            path.write_bytes(b"hello\x00world")
            errors = validate_file(root, path)
        self.assertTrue(any("binary/NUL" in error for error in errors))

    def test_plain_utf8_file_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "note.txt"
            path.write_text("public engineering note\n", encoding="utf-8")
            self.assertEqual([], validate_file(root, path))


if __name__ == "__main__":
    unittest.main()
