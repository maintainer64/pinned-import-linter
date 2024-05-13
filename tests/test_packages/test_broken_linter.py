from __future__ import annotations

import pathlib
import typing as t
from unittest import mock

import pytest

from pinnedimportlinter import checker_files_content_uc
from pinnedimportlinter.domain.constant import ERROR_RED
from pinnedimportlinter.domain.constant import EXIT_STATUS_ERROR


@pytest.fixture(scope="session")
def files_broken_linter(directory_test_file: pathlib.Path) -> list[pathlib.Path]:
    return sorted(
        filter(
            lambda x: x.is_file() and x.name.endswith("_broken.yp"),
            directory_test_file.iterdir(),
        )
    )


@pytest.fixture(scope="session")
def output_broken_linter(directory_test_file: pathlib.Path) -> list[str]:
    output = [
        # alias_any
        "alias_any_broken.yp:1: {} Banned import 'import alias_any'",
        "alias_any_broken.yp:3: {} Banned import 'from alias_any import ...'",
        # alias_or_package_broken
        "alias_or_package_broken.yp:3: {} Banned import 'from alias_or_package import ...'",
        "banned_broken.yp:1: {} Banned import 'import banned'",
        "banned_broken.yp:2: {} Banned import 'import banned as ...'",
        "banned_broken.yp:3: {} Banned import 'from banned import ...'",
        # only_alias_only_names_broken
        "only_alias_only_names_broken.yp:1: {} Banned import 'import only_alias_only_names'",
        "only_alias_only_names_broken.yp:2: {} Banned import "
        "'import only_alias_only_names as real_any_type'",
        "only_alias_only_names_broken.yp:5: {} Banned import 'from only_alias_only_names import ...'",
        # only_from_broken
        "only_from_broken.yp:1: {} Banned import 'import only_from'",
        "only_from_broken.yp:2: {} Banned import 'import only_from as ...'",
        # only_package
        "only_package_broken.yp:2: {} Banned import 'import only_package as ...'",
        "only_package_broken.yp:4: {} Banned import 'from only_package import ...'",
    ]
    format_output = "\n".join(
        [str(directory_test_file) + "/" + line.format(ERROR_RED) for line in output]
    )
    return [format_output]


def test_broken_linter(
    directory_custom_tox_file: pathlib.Path,
    mock_std_error: t.Callable[..., list[str]],
    mock_sys_exit: mock.Mock,
    files_broken_linter: list[pathlib.Path],
    output_broken_linter: list[str],
) -> None:
    checker_files_content_uc(
        configure_path=str(directory_custom_tox_file),
        file_path_to_check=list(map(str, files_broken_linter)),
    )
    mock_sys_exit.assert_called_with(EXIT_STATUS_ERROR)
    assert mock_std_error() == output_broken_linter
