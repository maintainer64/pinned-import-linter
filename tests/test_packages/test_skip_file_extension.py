from __future__ import annotations

import pathlib
import typing as t
from unittest import mock

import pytest

from pinnedimportlinter import checker_files_content_uc
from pinnedimportlinter.domain.constant import EXIT_STATUS_SUCCESS


@pytest.fixture(scope="session")
def files_broken_linter(directory_test_file: pathlib.Path) -> list[pathlib.Path]:
    return [directory_test_file / "banned_broken.yp"]


@pytest.fixture(scope="session")
def directory_file_extension_file(assets_path: pathlib.Path) -> pathlib.Path:
    return assets_path / "testpackage" / "file_extension.ini"


def test_skip_file_extension(
    directory_file_extension_file: pathlib.Path,
    mock_std_error: t.Callable[..., list[str]],
    mock_sys_exit: mock.Mock,
    files_broken_linter: list[pathlib.Path],
) -> None:
    checker_files_content_uc(
        configure_path=str(directory_file_extension_file),
        paths_to_check=list(map(str, files_broken_linter)),
    )
    mock_sys_exit.assert_called_with(EXIT_STATUS_SUCCESS)
    assert mock_std_error() == [""]
