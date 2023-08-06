import collections
import os
import re
from pathlib import Path
from typing import Union

import ruamel.yaml
from pydantic import BaseModel

yaml = ruamel.yaml.YAML()


class ConfigParsingError(Exception):
    pass


class BaseConfig(BaseModel):
    @classmethod
    def load(cls, path: Union[str, Path]):
        conf_path = Path(path)
        try:
            raw_yaml = cls._render_env_var_templates(conf_path.read_text())
            conf_data = yaml.load(raw_yaml) or {}
        except FileNotFoundError:
            raise ValueError(f"Config file is missing: {conf_path}")

        return cls(**conf_data)

    @staticmethod
    def _render_env_var_templates(content: str) -> str:
        pattern = r"(\${{\s*?(\w*?)\s*?}}\s*?)"  # add quotes
        missing_keys = []
        subs = {}
        for template, var_name in re.findall(pattern, content):
            try:
                value = os.environ[var_name]
            except KeyError:
                missing_keys.append(var_name)
            else:
                subs[template] = value
        if missing_keys:
            missing_list = ", ".join(missing_keys)
            raise ConfigParsingError(
                f"Failed to get following variables from environment: {missing_list}"
            )

        for tmpl, value in subs.items():
            content = content.replace(tmpl, value)

        return content

    @classmethod
    def export_as_yaml(cls, path: Union[str, Path]):
        path = Path(path) if isinstance(path, str) else path

        if path.exists():
            current_content = yaml.load(path)
            new_content = dict_merge(current_content, generate_yaml(cls))
        else:
            new_content = generate_yaml(cls)

        yaml.dump(new_content, path)


def generate_yaml(cls):
    conf_dict = {}
    for name, field in cls.__fields__.items():
        if hasattr(field.type_, "Config"):
            value = generate_yaml(field.type_)
        elif field.default is not None:
            value = field.default
        else:
            value = f"_{field.type_.__name__}_"
        conf_dict[name] = value

    return conf_dict


def dict_merge(origin: dict, updated: dict):
    # update if default value is set
    # remove key if it's obsolete? how?

    new_dict = origin.copy()
    for k in updated:
        if (
            k in new_dict
            and isinstance(new_dict[k], dict)
            and isinstance(updated[k], collections.Mapping)
        ):
            new_dict[k] = dict_merge(new_dict[k], updated[k])
        elif k not in new_dict:
            new_dict[k] = updated[k]
    return _remove_obsolete(new_dict, updated)


def _remove_obsolete(origin: dict, updated: dict):
    new_dict = origin.copy()
    obsolete = []
    for key in new_dict:
        if key not in updated:
            obsolete.append(key)
        elif isinstance(new_dict[key], collections.Mapping) and isinstance(
            updated[key], collections.Mapping
        ):
            _remove_obsolete(new_dict[key], updated[key])
    for key in obsolete:
        new_dict.pop(key, None)
    return new_dict
