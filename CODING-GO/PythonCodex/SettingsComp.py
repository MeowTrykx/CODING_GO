import json, os, pygame

# --- Paths ---
SAVE_FILE = "save_data.json"
FONT_PATH = os.path.join("Fonts", "Pixeled.ttf")

# --- Initialize Font ---
pygame.font.init()
try:
    font = pygame.font.Font(FONT_PATH, 32)
except:
    # Fallback font if file not found
    font = pygame.font.SysFont("consolas", 32)

# --- Default Settings Data ---
default_data = {
    "player_name": "????",
    "player_level": 1
}


# --- Load / Save Functions ---
def load_settings():
    """Load player data from JSON file or create a default one."""
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                return data
        except json.JSONDecodeError:
            print("Corrupted save file detected. Resetting...")
    save_settings(default_data)
    return default_data.copy()


def save_settings(data):
    """Save current player data to JSON file."""
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)


def reset_settings():
    """Reset player data to default (new game)."""
    save_settings(default_data.copy())


# --- Helper Functions ---
def get_player_name():
    data = load_settings()
    return data.get("player_name", "????")


def set_player_name(name):
    data = load_settings()
    data["player_name"] = name
    save_settings(data)


def get_player_level():
    data = load_settings()
    return data.get("player_level", 1)


def set_player_level(level):
    data = load_settings()
    data["player_level"] = level
    save_settings(data)


# --- Load data when imported ---
settings_data = load_settings()
