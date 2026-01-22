from collections.abc import Iterable
from glob import glob


def get_paths(path: str | list[str]) -> list[str]:
    if isinstance(path, str):
        return glob(path)
    
    paths: list[str] = []

    if isinstance(path, Iterable):
        
        p: str

        for p in path:
            paths.extend(glob(p))

    return paths
