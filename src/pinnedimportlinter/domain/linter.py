from __future__ import annotations

import dataclasses
from enum import Enum


class Rule(Enum):
    import_from = 0
    import_as = 1
    import_module = 2


@dataclasses.dataclass
class LinterModuleName:
    module_name: str | None = None
    alias_name: str | None = None


@dataclasses.dataclass
class LinterLine:
    filename: str
    lineno: int
    col_offset: int
    module: LinterModuleName
    rule: Rule
