from pandas import DataFrame, concat, read_csv
from pathlib import Path

from src.get_paths import get_paths


def get_token_data(path: str | list[str], verbose: bool = False) -> DataFrame:
    paths: list[str] = get_paths(path)
    frames: list[DataFrame] = []

    # For each archive file...
    for path in paths:
        if verbose:
            print(f'Reading "{Path(path).name}"...')

        frames.append(read_csv(path, keep_default_na=False, encoding="utf-16"))

    return concat(frames, ignore_index=True)
