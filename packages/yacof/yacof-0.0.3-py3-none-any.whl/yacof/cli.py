import argparse
import importlib
import os
import sys
from pathlib import Path
from typing import List, NamedTuple, Optional

import configparser


class ConfigDumpSettings(NamedTuple):
    yaml_path: str
    conf_module: str
    conf_name: str


class CliArgs(NamedTuple):
    verbose: bool
    dump_settings: Optional[ConfigDumpSettings]


def read_cli_args() -> CliArgs:
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--out", help="Resulted .YAML config")
    parser.add_argument(
        "-m", "--module", help="Module with custom config derived from yacof.BaseConfig"
    )
    parser.add_argument(
        "-n", "--name", help="Name of custom config derived from yacof.BaseConfig"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", default=False, help="Verbose mode"
    )
    args = parser.parse_args()

    if not all((args.out, args.module, args.name)):
        settings = None
    else:
        settings = ConfigDumpSettings(args.out, args.module, args.name)
    return CliArgs(args.verbose, settings)


def load_setup_cfg(setup_cfg_path: str) -> List[ConfigDumpSettings]:
    parser = configparser.ConfigParser()
    parser.read(setup_cfg_path)
    settings = []
    for yaml_path in parser["yacof"]:
        module, name = parser["yacof"][yaml_path].split(":")
        settings.append(ConfigDumpSettings(yaml_path, module, name))
    return settings


def dump_configs(dump_settings: List[ConfigDumpSettings]):
    sys.path.append(os.getcwd())
    for settings in dump_settings:
        module = importlib.import_module(settings.conf_module)
        for attr in dir(module):
            if attr == settings.conf_name:
                conf_class = getattr(module, attr)
                conf_class.export_as_yaml(settings.yaml_path)
                print(f"Saving {attr} -> {settings.yaml_path}")


def main():
    args = read_cli_args()
    if args.dump_settings is not None:
        if args.verbose:
            print(f"Dumping: {args.dump_settings}")
        dump_configs([args.dump_settings])

    setup_cfg = "setup.cfg"
    if Path(setup_cfg).exists():
        if args.verbose:
            print("Found setup.cfg")
        dump_settings = load_setup_cfg(setup_cfg)
        if args.verbose:
            print(f"Dumping: {dump_settings}")
        dump_configs(dump_settings)
    elif args.verbose:
        print("No setup.cfg found")
