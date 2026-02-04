from argparse import ArgumentParser, Namespace
from glob import glob
from io import TextIOWrapper
from pandas import DataFrame, set_option
from pathlib import Path
from sqlite3 import Connection
from typing import Any

from src.get_alarm_data import get_alarm_data
from src.get_token_data import get_token_data
from src.load_configuration import load_configuration
from src.sqlite import disconnect, get_connection, query, write


def main() -> None:
    arguments: Namespace = parse_arguments()
    configuration: dict[str, Any] = load_configuration(Path(__file__).parent.joinpath("config.json"), arguments.verbose)
    connection: Connection = get_connection(configuration["database"], arguments.verbose)
    path: str
    data: DataFrame

    set_option("display.max_rows", None)
    set_option("display.max_columns", None)
    set_option("display.width", None)

    if arguments.get_alarm_data is not None:
        if len(arguments.get_alarm_data):
            path = arguments.get_data

        else:
            path = configuration["alarm"]["data"]
        
        data = get_alarm_data(path, arguments.verbose)
        write(data, connection, "alarms", "replace", False, arguments.verbose)

    if arguments.get_token_data is not None:
        if len(arguments.get_token_data):
            path = arguments.get_data

        else:
            path = configuration["token"]["data"]

        data = get_token_data(path, arguments.verbose)
        write(data, connection, "tokens", "replace", False, arguments.verbose)

    if arguments.get_user_data is not None:
        write(DataFrame(configuration["user"]["data"]), connection, "users", "replace", False, arguments.verbose)

    if arguments.list:
        paths: list[str] = glob("sql/**/*.sql", recursive=True)
       
        for path in paths:  
                print(Path(path).as_posix())

    if arguments.query:
        stream: TextIOWrapper = open(Path(__file__).parent.joinpath(arguments.query))
        sql: str = stream.read()
        stream.close()
        data = query(sql, connection, arguments.verbose)
        print(data)

    disconnect(connection, arguments.verbose)


def parse_arguments() -> Namespace:
    argument_parser: ArgumentParser = ArgumentParser(description="Process data files and store them in a SQLite database.")
    argument_parser.add_argument("-A", "--get_alarm_data", nargs="?", const="", type=str, help="Get alarm data")
    argument_parser.add_argument("-T", "--get_token_data", nargs="?", const="", type=str, help="Get token data")
    argument_parser.add_argument("-U", "--get_user_data", nargs="?", const="", type=str, help="Get user data")
    argument_parser.add_argument("-l", "--list", action="store_true", help="List available queries")
    argument_parser.add_argument("-q", "--query", help="Query data")
    argument_parser.add_argument("-v", "--verbose", action="store_true", help="Verbose")
    arguments: Namespace = argument_parser.parse_args()

    return arguments


if __name__ == "__main__":
    main()
