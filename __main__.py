from argparse import ArgumentParser, Namespace
from cv2 import VideoCapture, imshow, waitKey, destroyAllWindows
from cv2.typing import MatLike
import ffmpeg
from glob import glob
from io import TextIOWrapper
from pandas import DataFrame, json_normalize, set_option
from pathlib import Path
from sqlite3 import Connection
from typing import Any
from urllib.parse import quote

from src.explode import explode
from src.get_alarm_data import get_alarm_data
from src.get_token_data import get_token_data
from src.load_configuration import load_configuration
from src.sqlite import disconnect, get_connection, query, write


def main() -> None:
    arguments: Namespace = parse_arguments()
    configuration: dict[str, Any] = load_configuration(Path(__file__).parent.joinpath("config.json"), arguments.verbose)
    connection: Connection = get_connection(configuration["database"], arguments.verbose)

    set_option("display.max_rows", None)
    set_option("display.max_columns", None)
    set_option("display.width", None)

    if arguments.get_alarm_data is not None:
        if len(arguments.get_alarm_data):
            path: str = arguments.get_data

        else:
            path: str = configuration["alarm"]["data"]
        
        data: DataFrame = get_alarm_data(path, arguments.verbose)
        write(data, connection, "alarms", "replace", False, arguments.verbose)

    if arguments.get_camera_data:
        filename: str = f"{configuration["camera"]["protocol"]}://{quote(configuration["camera"]["username"])}:{quote(configuration["camera"]["password"])}@{configuration["camera"]["ip"]}:{configuration["camera"]["port"]}/unicast/c{configuration["camera"]["channel"]}/s{configuration["camera"]["stream"]}/live"
        video_capture: VideoCapture = VideoCapture(filename)

        if not video_capture.isOpened():
            raise Exception("Failed to open stream.")

        return_value: bool
        frame: MatLike
        return_value, frame = video_capture.read()
        video_capture.release()

        if not return_value:
            raise Exception("Failed to read frame.")
        
        print(frame)

    if arguments.get_token_data is not None:
        if len(arguments.get_token_data):
            path: str = arguments.get_data

        else:
            path: str = configuration["token"]["data"]

        data: DataFrame = get_token_data(path, arguments.verbose)
        write(data, connection, "tokens", "replace", False, arguments.verbose)

    if arguments.get_user_data is not None:
        users: DataFrame = json_normalize(configuration["users"])
        users = users.drop(columns=["emails", "phones"])

        # Normalize emails
        emails: DataFrame = explode(configuration["users"], "emails")
        phones: DataFrame = explode(configuration["users"], "phones")
        write(users, connection, "users", "replace", False, arguments.verbose)
        write(emails, connection, "emails", "replace", False, arguments.verbose)
        write(phones, connection, "phones", "replace", False, arguments.verbose)

    if arguments.list:
        paths: list[str] = glob("sql/**/*.sql", recursive=True)
        path: str
       
        for path in paths:  
                print(Path(path).as_posix())

    if arguments.query:
        stream: TextIOWrapper = open(Path(__file__).parent.joinpath(arguments.query))
        sql: str = stream.read()
        stream.close()
        data: DataFrame = query(sql, connection, arguments.verbose)
        print(data)

    disconnect(connection, arguments.verbose)


def parse_arguments() -> Namespace:
    argument_parser: ArgumentParser = ArgumentParser(description="PyCentral: Data Acquisition & Analytics")
    argument_parser.add_argument("-A", "--get_alarm_data", nargs="?", const="", type=str, help="Get alarm data")
    argument_parser.add_argument("-C", "--get_camera_data", action="store_true", help="Get camera data")
    argument_parser.add_argument("-T", "--get_token_data", nargs="?", const="", type=str, help="Get token data")
    argument_parser.add_argument("-U", "--get_user_data", nargs="?", const="", type=str, help="Get user data")
    argument_parser.add_argument("-l", "--list", action="store_true", help="List available queries")
    argument_parser.add_argument("-q", "--query", help="Query data")
    argument_parser.add_argument("-v", "--verbose", action="store_true", help="Verbose")
    arguments: Namespace = argument_parser.parse_args()

    return arguments


if __name__ == "__main__":
    main()
