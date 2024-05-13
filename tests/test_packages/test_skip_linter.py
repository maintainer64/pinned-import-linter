from __future__ import annotations

import pathlib
import typing as t
from unittest import mock

import pytest

from pinnedimportlinter import checker_files_content_uc
from pinnedimportlinter.domain.constant import EXIT_STATUS_SUCCESS


@pytest.fixture(scope="session")
def files_skip_linter(directory_test_file: pathlib.Path) -> list[pathlib.Path]:
    return sorted(
        filter(
            lambda x: x.is_file() and x.name.endswith("_skip.yp"),
            directory_test_file.iterdir(),
        )
    )


def test_skip_linter(
    directory_custom_tox_file: pathlib.Path,
    mock_std_error: t.Callable[..., list[str]],
    mock_sys_exit: mock.Mock,
    files_skip_linter: list[pathlib.Path],
) -> None:
    checker_files_content_uc(
        configure_path=str(directory_custom_tox_file),
        file_path_to_check=list(map(str, files_skip_linter)),
    )
    mock_sys_exit.assert_called_with(EXIT_STATUS_SUCCESS)
    assert mock_std_error() == [""]
