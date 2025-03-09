from datetime import datetime
import json
import os
from utils.resource_utils import resource_path

class Runner:
    def __init__(self, name):
        self.name = name
        self.data_file = resource_path(f"database/users/{name}.json")
        self._init_database()

    def _init_database(self):
        if not os.path.exists(self.data_file):
            base_structure = {
                "runner_info": {"name": self.name},
                "training_records": {},
                "training_modes": {}
            }
            self._save_data(base_structure)

    def _load_data(self):
        with open(self.data_file, 'r') as f:
            return json.load(f)

    def _save_data(self, data):
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)