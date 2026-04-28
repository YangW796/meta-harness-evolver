#!/usr/bin/env python3

import os
from pathlib import Path
from typing import Iterable


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if key:
            os.environ.setdefault(key, value)


def get_workspace() -> Path:
    raw = os.environ.get("EVOLVER_WORKSPACE", "~/hoss-evolution")
    return Path(raw).expanduser().resolve()


_IGNORED_DIR_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".ipynb_checkpoints",
    "node_modules",
    "dist",
    "build",
}
_IGNORED_FILE_NAMES = {
    ".DS_Store",
    ".env",
    ".env.local",
}
_IGNORED_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".pt"
}


def should_ignore_path(path: Path) -> bool:
    if "__pycache__" in path.parts:
        return True
    name = path.name
    if name in _IGNORED_FILE_NAMES:
        return True
    if name.endswith(".egg-info"):
        return True
    if name.startswith(".") and name not in {".gitkeep"}:
        return True
    if path.is_dir() and name in _IGNORED_DIR_NAMES:
        return True
    if path.is_file() and path.suffix in _IGNORED_SUFFIXES:
        return True
    return False


def iter_effective_files(directory: Path) -> Iterable[Path]:
    for p in directory.iterdir():
        if should_ignore_path(p):
            continue
        if p.is_file():
            yield p


def iter_effective_files_recursive(directory: Path) -> Iterable[Path]:
    stack = [directory]
    while stack:
        cur = stack.pop()
        for p in cur.iterdir():
            if should_ignore_path(p):
                continue
            if p.is_dir():
                stack.append(p)
            elif p.is_file():
                yield p
