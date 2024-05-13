from __future__ import annotations

import sys

from ...domain.constant import EXIT_STATUS_ERROR
from ...domain.constant import EXIT_STATUS_SUCCESS
from ..config_parser import LinterConfig
from ..printer import Printer
from ..rule_checker import RuleCheckerService
from .walk import search_python_files


def read_file(filename: str) -> str:
    with open(filename, encoding="utf-8") as file:
        return file.read()


def checker_files_content_uc(
    configure_path: str,
    paths_to_check: list[str],
) -> None:
    """
    Load configure and check files
    :param configure_path: Path on ini file
    :param paths_to_check: List of files or directories to check
    :return: system exit code
    """
    config = LinterConfig.read_config(config_path=configure_path)
    printer = Printer()
    errors = 0
    for file_path in search_python_files(
        paths_to_check=paths_to_check,
        config=config,
    ):
        filename = str(file_path)
        file_content = read_file(filename=filename)
        errors += RuleCheckerService(
            filename=filename, config=config, printer=printer
        ).check_content(file_content=file_content)
    printer.print()
    exit_code = EXIT_STATUS_ERROR if errors else EXIT_STATUS_SUCCESS
    sys.exit(exit_code)
