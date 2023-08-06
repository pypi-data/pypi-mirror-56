from pathlib import Path


def get_flubber_path() -> str:
    return str(Path(__file__).parent.parent.absolute())
