from __future__ import annotations

import os
import pathlib
import sys
import typing as t
from unittest import mock

import pytest


@pytest.fixture(autouse=True, scope="session")
def chdir() -> None:
    os.chdir(pathlib.Path(__file__).parent)


@pytest.fixture(scope="session")
def assets_path() -> pathlib.Path:
    return pathlib.Path(__file__).parent / "assets"


@pytest.fixture(scope="session")
def directory_custom_tox_file(assets_path: pathlib.Path) -> pathlib.Path:
    return assets_path / "testpackage" / "custom_tox_file.ini"


@pytest.fixture(scope="session")
def directory_empty_tox_file(assets_path: pathlib.Path) -> pathlib.Path:
    return assets_path / "testpackage" / "empty_file.txt"


@pytest.fixture(scope="session")
def directory_test_file(assets_path: pathlib.Path) -> pathlib.Path:
    return assets_path / "testpackage" / "testpackage"


@pytest.fixture()
def mock_std_error() -> t.Iterator[t.Callable[..., list[str]]]:
    with mock.patch("builtins.print") as output:

        def wrap() -> list[str]:
            return [
                call.args[0] for call in output.call_args_list if call.kwargs["file"] == sys.stderr
            ]

        yield wrap


@pytest.fixture()
def mock_sys_exit() -> t.Iterator[mock.Mock]:
    with mock.patch("sys.exit") as output:
        yield output
