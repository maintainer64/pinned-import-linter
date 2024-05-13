from __future__ import annotations

import configparser
import dataclasses
import re
import typing as t

from ..domain.constant import CONFIG_BLOCK_NAME


def _string_spit(string: str | list[str]) -> list[str]:
    if isinstance(string, list):
        return string
    return [name.strip() for name in string.split(",") if name.strip()]


@dataclasses.dataclass
class PackageNameSettingsBlock:
    allow_alias: bool
    alias_names: set[str]
    allow_from: bool
    allow_package: bool

    @classmethod
    def from_dict(cls, value: configparser.SectionProxy) -> t.Self:
        return cls(
            allow_alias=value.getboolean("allow_alias", fallback=True),
            alias_names=set(_string_spit(value.get("alias_names") or "") or []),
            allow_from=value.getboolean("allow_from", fallback=True),
            allow_package=value.getboolean("allow_package", fallback=True),
        )


@dataclasses.dataclass
class LinterSettingsBlock:
    package_names: t.Set[str]

    @classmethod
    def from_dict(cls, value: configparser.SectionProxy) -> t.Self:
        return cls(
            package_names=set(_string_spit(value.get("package_names") or "") or []),
        )


class LinterConfig:
    __default__ = PackageNameSettingsBlock(
        allow_alias=True,
        alias_names=set(),
        allow_from=True,
        allow_package=True,
    )

    def __init__(
        self,
        config_path: str,
        file_extensions: set[str] | None = None,
        exclude: str | None = None,
        packages: dict[str, PackageNameSettingsBlock] | None = None,
    ):
        self.config_path = config_path
        self.file_extensions: set[str] = file_extensions or {"py"}
        self.exclude: t.Pattern[str] | None = re.compile(exclude) if exclude else None
        self._packages = packages or {}

    def get(self, package_name: str | None) -> PackageNameSettingsBlock:
        if not package_name:
            return self.__default__
        return self._packages.get(package_name) or self.__default__

    @classmethod
    def read_config(cls, config_path: str) -> t.Self:
        config = configparser.ConfigParser()
        config.read(config_path)
        if CONFIG_BLOCK_NAME not in config:
            return cls(config_path=config_path)
        main_block = config[CONFIG_BLOCK_NAME]
        package_names = _string_spit(main_block.get("package_names") or "")
        file_extensions = _string_spit(main_block.get("file_extensions") or "")
        exclude = main_block.get("exclude", None)
        return cls(
            config_path=config_path,
            file_extensions=set(file_extensions),
            exclude=exclude,
            packages={
                package_name: PackageNameSettingsBlock.from_dict(config[block_name])
                for package_name in package_names
                if (block_name := f"{CONFIG_BLOCK_NAME}.{package_name}") in config
            },
        )
