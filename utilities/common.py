import json
import os
import time


def get_config():
    root_dir = os.path.dirname(os.path.dirname(__file__))
    config_path = os.path.join(root_dir, "config.json")

    with open(config_path) as f:
        return json.load(f)


def generate_group_name(stream_name: str) -> str:
    current_time = int(time.time())
    return f"{stream_name}_{current_time}"
