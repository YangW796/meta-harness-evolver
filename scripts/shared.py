#!/usr/bin/env python3

import os
import importlib.util
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


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def resolve_maybe_relative_path(raw_path: str | Path, *, cwd: Path | None = None) -> Path:
    p = Path(raw_path).expanduser()
    if p.is_absolute():
        return p.resolve()
    base = (cwd or Path.cwd()).expanduser().resolve()
    return (base / p).resolve()


def find_sidecar_next_to_script(script_path: str | Path, filename: str) -> Path | None:
    try:
        sp = resolve_maybe_relative_path(script_path)
    except Exception:
        return None
    p = sp.parent / filename
    return p if p.exists() else None


def load_callable_from_python_file(raw_path: str | Path, fn_name: str, module_name: str) -> object | None:
    try:
        p = resolve_maybe_relative_path(raw_path)
    except Exception:
        return None
    if not p.exists():
        return None
    try:
        spec = importlib.util.spec_from_file_location(module_name, str(p))
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        fn = getattr(module, fn_name, None)
        return fn if callable(fn) else None
    except Exception:
        return None
