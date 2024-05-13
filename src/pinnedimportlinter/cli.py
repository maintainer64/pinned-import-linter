from __future__ import annotations

import argparse

from .application.use_cases.checker_files_content import checker_files_content_uc


def argument_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check for restricted imports in Python files.")
    parser.add_argument(
        "files", metavar="FILE", type=str, nargs="+", help="Files or directories to be checked"
    )
    parser.add_argument(
        "--config", type=str, default="tox.ini", help="Path to config file (default: tox.ini)"
    )
    return parser.parse_args()


def main() -> None:
    args = argument_parser()
    checker_files_content_uc(
        configure_path=args.config,
        paths_to_check=args.files,
    )


if __name__ == "__main__":
    main()
