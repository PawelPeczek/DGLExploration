import json
import os
from typing import Union


def dump_json_to_file(target_path: str, content: Union[list, dict]) -> None:
    create_parent_dir(path=target_path)
    with open(target_path, "w") as f:
        json.dump(content, f, indent=4)


def parse_json(json_path: str) -> Union[dict, list]:
    with open(json_path, "r") as f:
        return json.load(f)


def create_parent_dir(path: str) -> None:
    parent_dir = os.path.dirname(path)
    parent_dir = os.path.abspath(parent_dir)
    os.makedirs(parent_dir, exist_ok=True)
