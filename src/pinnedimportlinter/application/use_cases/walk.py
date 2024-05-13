from __future__ import annotations

import functools
import os
import pathlib
import typing as t

from ...application.config_parser import LinterConfig


def _check_exclude_directory(
    path: pathlib.Path,
    pattern_exclude: t.Pattern[t.AnyStr] | None = None,
) -> bool:
    if not pattern_exclude:
        return True
    relative_path = os.sep.join(path.parts)
    return pattern_exclude.match(relative_path) is None  # type: ignore[call-overload]


def _check_extensions(
    path: pathlib.Path,
    file_extensions: set[str] | None = None,
) -> bool:
    if not file_extensions:
        return True
    extension = path.suffix.lstrip(".")
    return extension in file_extensions


def _check_file(
    path: pathlib.Path,
    config: LinterConfig,
) -> bool:
    return _check_extensions(
        path=path, file_extensions=config.file_extensions
    ) and _check_exclude_directory(
        path=path,
        pattern_exclude=config.exclude,
    )


def _glob_walk_files(path: pathlib.Path) -> t.Iterator[pathlib.Path]:
    if path.is_file():
        yield path
    yield from path.glob("**/*")


def search_python_files(
    paths_to_check: list[str],
    config: LinterConfig,
) -> t.Iterator[pathlib.Path]:
    visited: set[pathlib.Path] = set()
    check_file = functools.partial(_check_file, config=config)
    for path_to_check in paths_to_check:
        path = pathlib.Path(path_to_check)
        for file in _glob_walk_files(path):
            if not file.is_file() or not check_file(file) or path in visited:
                continue
            visited.add(file)
            yield file
