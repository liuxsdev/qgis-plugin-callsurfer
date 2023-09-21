from pathlib import Path

Plugin_DIR = Path(__file__).parent
Project_DIR = Plugin_DIR.joinpath("Projects")

if not Project_DIR.exists():
    Project_DIR.mkdir()
