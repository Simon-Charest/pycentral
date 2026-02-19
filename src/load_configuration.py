from json import load
from pathlib import Path
from typing import Any


def load_configuration(file: Path, encoding: str, verbose: bool = False) -> dict[str, Any]:
    configuration: dict[str, Any] = load(open(file, encoding=encoding))

    if verbose:
        print("Configuration loaded.")

    return configuration
