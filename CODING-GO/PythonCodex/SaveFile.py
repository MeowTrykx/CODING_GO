import json
import os

SAVE_PATH = "PythonCodex/save_data.json"

# Default data if no save exists
DEFAULT_SAVE = {
    "player_name": "Poko",
    "current_hp": 100,
    "max_hp": 100,
    "current_stamina": 100,
    "max_stamina": 100,
    "progress_stage": "tutorial_start"
}

# --- Create or load save file ---
def load_save():
    """Loads player save data. If none exists, creates a default save."""
    if not os.path.exists(SAVE_PATH):
        save_data(DEFAULT_SAVE)
        return DEFAULT_SAVE
    try:
        with open(SAVE_PATH, "r") as f:
            data = json.load(f)
        # Add missing keys if code is updated
        for key, value in DEFAULT_SAVE.items():
            if key not in data:
                data[key] = value
        return data
    except (json.JSONDecodeError, FileNotFoundError):
        save_data(DEFAULT_SAVE)
        return DEFAULT_SAVE


# --- Save data to file ---
def save_data(data):
    """Saves player progress to file."""
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    with open(SAVE_PATH, "w") as f:
        json.dump(data, f, indent=4)


# --- Update individual data points ---
def update_save(player_name=None, hp=None, stamina=None, stage=None):
    """Updates specific parts of the save file."""
    data = load_save()
    if player_name is not None:
        data["player_name"] = player_name
    if hp is not None:
        data["current_hp"] = hp
    if stamina is not None:
        data["current_stamina"] = stamina
    if stage is not None:
        data["progress_stage"] = stage
    save_data(data)


# --- Quick reset for debugging or new game ---
def reset_save():
    """Resets save file to default state."""
    save_data(DEFAULT_SAVE)
    print("Save file reset to defaults.")


# --- Example usage ---
if __name__ == "__main__":
    # Try loading an existing save
    save = load_save()
    print("Loaded Save:", save)

    # Example of updating save
    update_save(player_name="Poko", hp=80, stamina=60, stage="tutorial_end")

    # Print updated save
    print("Updated Save:", load_save())

