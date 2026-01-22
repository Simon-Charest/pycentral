
from pandas import DataFrame, read_sql
from pathlib import Path
from sqlite3 import Connection, connect
from typing import Literal


def get_connection(database: Path, verbose: bool = False) -> Connection:
    connection: Connection = connect(database)

    if verbose:
        print(f'Connected to database "{database}".')

    return connection


def write(data_frame: DataFrame, connection: Connection, name: str, if_exists: Literal["fail", "replace", "append", "delete_rows"] = "replace", index: bool = False, verbose: bool = False) -> None:
    data_frame = drop_duplicates(data_frame, verbose)
    data_frame.to_sql(name, connection, if_exists=if_exists, index=index)

    if verbose:
        print(f"Wrote {len(data_frame)} row(s) to database.")


def drop_duplicates(data_frame: DataFrame, verbose: bool = False) -> DataFrame:
    data_frame = data_frame.drop_duplicates()

    if verbose:
        print(f"Removed duplicate(s).")

    return data_frame


def query(sql: str, connection: Connection, verbose: bool = False) -> DataFrame:
    if verbose:
        print(f"Querying database...")

    data_frame: DataFrame = read_sql(sql, connection)
    
    if verbose:
        print(f"Fetched {len(data_frame)} row(s).")

    return data_frame


def disconnect(connection: Connection, verbose: bool = False) -> None:
    connection.close()

    if verbose:
        print("Disconnected from database.")
