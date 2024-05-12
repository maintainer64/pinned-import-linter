from __future__ import annotations

import ast
import dataclasses
import typing as t

from ..domain.linter import LinterLine
from ..domain.linter import LinterModuleName
from ..domain.linter import Rule
from .config_parser import LinterConfig
from .printer import Printer


@dataclasses.dataclass
class RuleCheckerService:
    filename: str
    config: LinterConfig
    printer: Printer

    def rule_import_from(self, node: ast.AST) -> int:
        if not isinstance(node, ast.ImportFrom):
            return 0
        package_name = node.module
        if self.config.get(package_name).allow_from:
            return 0
        self.printer.append(
            LinterLine(
                filename=self.filename,
                lineno=node.lineno,
                col_offset=node.col_offset,
                module=LinterModuleName(
                    module_name=node.module,
                ),
                rule=Rule.import_from,
            )
        )
        return 1

    def rule_import_item_alias(self, node: ast.Import, alias: ast.alias) -> int:
        if alias.asname is None:
            return 0
        config = self.config.get(alias.name)
        if config.allow_alias is False:
            self.printer.append(
                LinterLine(
                    filename=self.filename,
                    lineno=node.lineno,
                    col_offset=node.col_offset,
                    module=LinterModuleName(
                        module_name=alias.name,
                    ),
                    rule=Rule.import_as,
                )
            )
            return 1
        if not config.alias_names:
            return 0
        if config.allow_alias and alias.asname not in config.alias_names:
            self.printer.append(
                LinterLine(
                    filename=self.filename,
                    lineno=node.lineno,
                    col_offset=node.col_offset,
                    module=LinterModuleName(module_name=alias.name, alias_name=alias.asname),
                    rule=Rule.import_as,
                )
            )
            return 1
        return 0

    def rule_import_alias(self, node: ast.AST) -> int:
        if not isinstance(node, ast.Import):
            return 0
        errors = 0
        for alias in node.names:
            errors += self.rule_import_item_alias(node=node, alias=alias)
        return errors

    def rule_import_item_package_name(self, node: ast.Import, alias: ast.alias) -> int:
        if alias.asname is not None:
            return 0
        if self.config.get(alias.name).allow_package:
            return 0
        self.printer.append(
            LinterLine(
                filename=self.filename,
                lineno=node.lineno,
                col_offset=node.col_offset,
                module=LinterModuleName(
                    module_name=alias.name,
                ),
                rule=Rule.import_module,
            )
        )
        return 1

    def rule_import_package_name(self, node: ast.AST) -> int:
        if not isinstance(node, ast.Import):
            return 0
        errors = 0
        for alias in node.names:
            errors += self.rule_import_item_package_name(node=node, alias=alias)
        return errors

    def check_content(self, file_content: t.AnyStr) -> int:
        errors = 0
        tree = ast.parse(file_content, filename=self.filename)
        for node in ast.walk(tree):
            errors += self.rule_import_from(node=node)
            errors += self.rule_import_alias(node=node)
            errors += self.rule_import_package_name(node=node)
        return errors
