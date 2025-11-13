import json, os

SAVE_FILE = "savefile.json"

def load_save():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)
