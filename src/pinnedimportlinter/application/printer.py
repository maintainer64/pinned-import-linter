from __future__ import annotations

import dataclasses
import sys
import typing as t

from ..domain.constant import ERROR_RED
from ..domain.linter import LinterLine
from ..domain.linter import Rule

TEMPLATE_MESSAGE = "{}:{}: {} Banned import '{}'"


@dataclasses.dataclass
class Printer:
    file: t.TextIO | None = dataclasses.field(default=sys.stderr)
    lines: list[LinterLine] = dataclasses.field(default_factory=list)

    def __len__(self) -> int:
        return len(self.lines)

    def __bool__(self) -> bool:
        return bool(self.lines)

    def append(self, line: LinterLine) -> None:
        self.lines.append(line)

    @staticmethod
    def format_line(line: LinterLine) -> str:
        module_name = line.module.module_name or "..."
        alias_name = line.module.alias_name or "..."
        template_payload: dict[Rule, str] = {
            Rule.import_from: f"from {module_name} import ...",
            Rule.import_as: f"import {module_name} as {alias_name}",
            Rule.import_module: f"import {module_name}",
        }
        return TEMPLATE_MESSAGE.format(
            line.filename, line.lineno, ERROR_RED, template_payload[line.rule]
        )

    def __str__(self) -> str:
        return "\n".join(map(self.format_line, self.lines))

    def print(self) -> None:
        print(str(self), file=self.file)
