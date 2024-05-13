from __future__ import annotations

import sys

from ...domain.constant import EXIT_STATUS_ERROR
from ...domain.constant import EXIT_STATUS_SUCCESS
from ..config_parser import LinterConfig
from ..printer import Printer
from ..rule_checker import RuleCheckerService


def read_file(filename: str) -> str:
    with open(filename, encoding="utf-8") as file:
        return file.read()


def checker_files_content_uc(
    configure_path: str,
    file_path_to_check: list[str],
) -> None:
    """
    Load configure and check files
    :param configure_path: Path on ini file
    :param file_path_to_check: List of files to check
    :return: system exit code
    """
    config = LinterConfig.read_config(config_path=configure_path)
    printer = Printer()
    errors = 0
    for filename in file_path_to_check:
        file_content = read_file(filename=filename)
        errors = RuleCheckerService(
            filename=filename, config=config, printer=printer
        ).check_content(file_content=file_content)
    printer.print()
    exit_code = EXIT_STATUS_ERROR if errors else EXIT_STATUS_SUCCESS
    sys.exit(exit_code)
