#!/usr/bin/env python3
"""Deterministic safety and structure checks for the public harness workspace."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

MAX_FILE_SIZE = 1_000_000

REQUIRED_PATHS = {
    "README.md",
    "HARNESS.md",
    ".gitignore",
    ".github/pull_request_template.md",
    ".github/workflows/verify.yml",
    "experiments/README.md",
    "tools/verify_workspace.py",
    "tests/test_verify_workspace.py",
}

SENSITIVE_EXACT_NAMES = {
    ".env",
    "id_rsa",
    "id_ed25519",
    "credentials.json",
    "secrets.json",
}

SENSITIVE_SUFFIXES = {
    ".pem",
    ".p12",
    ".pfx",
}

SECRET_PATTERNS = (
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
)


def _tracked_files(root: Path) -> list[Path]:
    """Return tracked files when Git is available, otherwise all ordinary files."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return sorted(
            path
            for path in root.rglob("*")
            if path.is_file() and ".git" not in path.parts
        )

    entries = [entry for entry in proc.stdout.decode("utf-8").split("\0") if entry]
    return [root / entry for entry in entries]


def _relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _sensitive_filename(path: Path) -> bool:
    name = path.name.lower()
    if name in SENSITIVE_EXACT_NAMES:
        return True
    return path.suffix.lower() in SENSITIVE_SUFFIXES


def _scan_text(text: str) -> list[str]:
    findings: list[str] = []
    for label, pattern in SECRET_PATTERNS:
        if pattern.search(text):
            findings.append(label)
    return findings


def validate_file(root: Path, path: Path) -> list[str]:
    rel = _relative(root, path)
    errors: list[str] = []

    if path.is_symlink():
        return [f"{rel}: symlinks are not allowed"]

    if _sensitive_filename(path):
        errors.append(f"{rel}: sensitive filename is not allowed")

    try:
        data = path.read_bytes()
    except OSError as exc:
        return [f"{rel}: cannot read file: {exc}"]

    if len(data) > MAX_FILE_SIZE:
        errors.append(
            f"{rel}: file size {len(data)} exceeds {MAX_FILE_SIZE} bytes"
        )

    if b"\x00" in data[:8192]:
        errors.append(f"{rel}: binary/NUL content is not allowed")
        return errors

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        errors.append(f"{rel}: file is not valid UTF-8")
        return errors

    for label in _scan_text(text):
        errors.append(f"{rel}: possible {label} detected")

    return errors


def validate_workspace(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []

    for rel in sorted(REQUIRED_PATHS):
        if not (root / rel).is_file():
            errors.append(f"{rel}: required workspace file is missing")

    for path in _tracked_files(root):
        errors.extend(validate_file(root, path))

    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = validate_workspace(root)

    if errors:
        print("Harness workspace verification: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Harness workspace verification: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
