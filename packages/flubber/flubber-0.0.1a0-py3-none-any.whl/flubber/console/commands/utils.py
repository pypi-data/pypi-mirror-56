from pathlib import Path


def get_flubber_path() -> str:
    return Path(__file__).parent.parent.parent.absolute()
