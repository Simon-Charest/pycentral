from pandas import DataFrame
from pathlib import Path
from zipfile import ZipFile

from src.get_events import get_events
from src.get_paths import get_paths


def get_alarm_data(path: str | list[str], verbose: bool = False) -> DataFrame:
    paths: list[str] = get_paths(path)
    events: list[dict[str, str]] = []

    # For each archive file...
    for path in paths:
        zip_file: ZipFile = ZipFile(path, metadata_encoding="utf-8")
        member: str

        # For each text file within the archive...
        for member in zip_file.namelist():
            if member.lower().endswith(".txt") and not member.endswith("/"):
                if verbose:
                    print(f'Unzipping "{Path(path).name}"...')

                bytes_: bytes = zip_file.read(member)
                string: str = bytes_.decode("cp1252")
                events += get_events(string)

        zip_file.close()

    return DataFrame(events)
