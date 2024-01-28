import json
import os


def get_config():
    root_dir = os.path.dirname(os.path.dirname(__file__))
    config_path = os.path.join(root_dir, "config.json")

    with open(config_path) as f:
        return json.load(f)
