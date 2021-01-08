import json
from pathlib import Path
cwd = Path(__file__).parents[1]
cwd = str(cwd)
def get_path():
    """
    A function to get the current path to bot.py
    Returns:
     - cwd (string) : Path to bot.py directory
    """
    cwd = Path(__file__).parents[1]
    cwd = str(cwd)
    print(cwd)
    return cwd
def read_json(filename):
    with open(f"{cwd}/bot_config/{filename}.json", "r") as file:
        data = json.load(file)
        return data
def write_json(data, filename):
    with open(f"{cwd}/bot_config/{filename}.json", "w") as file:
        json.dump(data, file, indent=4)