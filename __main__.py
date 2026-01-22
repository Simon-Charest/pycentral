from argparse import ArgumentParser, Namespace
from turtle import pd
from pandas import DataFrame, option_context
from pathlib import Path
from sqlite3 import Connection
from typing import Any
from zipfile import ZipFile

from src.get_events import get_events
from src.get_paths import get_paths
from src.load_configuration import load_configuration
from src.sqlite import disconnect, get_connection, query, write


def main() -> None:
    arguments: Namespace = parse_arguments()
    configuration: dict[str, Any] = load_configuration(Path(__file__).parent.joinpath("config.json"), arguments.verbose)
    connection: Connection = get_connection(configuration["database"], arguments.verbose)
    data_frame: DataFrame
    sql: str

    if arguments.get_data is not None:
        if len(arguments.get_data):
            path = arguments.get_data

        else:
            path = configuration["data"]
        
        data: DataFrame = get_data(path, arguments.verbose)
        write(data, connection, configuration["table"], "replace", False, arguments.verbose)
        write(DataFrame(configuration["users"]), connection, "users", "replace", False, arguments.verbose)

    if arguments.query:
        sql = f"""SELECT e.datetime
, CASE strftime('%w', datetime)
    WHEN '0' THEN 'Dimanche'
    WHEN '1' THEN 'Lundi'
    WHEN '2' THEN 'Mardi'
    WHEN '3' THEN 'Mercredi'
    WHEN '4' THEN 'Jeudi'
    WHEN '5' THEN 'Vendredi'
    WHEN '6' THEN 'Samedi'
END AS weekday
, CASE 
    WHEN INSTR(e.event, 'PR:') > 0 THEN
        SUBSTR(
            e.event,
            INSTR(e.event, 'PR:') + 3,
            INSTR(SUBSTR(e.event, INSTR(e.event, 'PR:') + 3), ' ') - 1
        )
    ELSE NULL
END AS PR
, u.name
, e.event
FROM {configuration.get("table")} AS e
LEFT JOIN users AS u ON u.id = pr
WHERE e.event NOT LIKE 'FERMETURE%'
AND e.event NOT LIKE '%[JAN-PRO]'
AND e.event NOT LIKE '%SIGNAL TRAITER%'
AND PR NOT IN ('001', '015')
AND e.event != 'TEST CODE GSM/IP'
AND
(
    TIME(e.datetime) < '07:00:00'
    OR TIME(e.datetime) >= '17:00:00'
    OR STRFTIME('%w', e.datetime) IN ('0', '6')
)

-- Exclusions
AND DATE(e.datetime) NOT IN (
    '2025-03-15'
    , '2025-05-05'
    , '2025-07-06'
    , '2025-08-17'
    , '2025-11-09'
    , '2025-11-24'
)
AND DATE(e.datetime) != '2025-08-17'
AND PR != '006'

ORDER BY e.datetime ASC
;
"""
        data_frame = query(sql, connection, arguments.verbose)
        with option_context("display.max_rows", None):
            print(data_frame)

    disconnect(connection, arguments.verbose)


def parse_arguments() -> Namespace:
    argument_parser: ArgumentParser = ArgumentParser(description="Process data files and store them in a SQLite database.")
    argument_parser.add_argument("-g", "--get_data", nargs="?", const="", type=str, help="Get data")
    argument_parser.add_argument("-q", "--query", action="store_true", help="Query data")
    argument_parser.add_argument("-v", "--verbose", action="store_true", help="Verbose")
    arguments: Namespace = argument_parser.parse_args()

    return arguments


def get_data(path: str | list[str], verbose: bool = False) -> DataFrame:
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


if __name__ == "__main__":
    main()
