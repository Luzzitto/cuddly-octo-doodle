import os
import sys
import mysql.connector
from dotenv import load_dotenv


class DB:
    def __init__(self):
        self.cnx = mysql.connector.connect(
            host=os.environ["DB_HOST"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASS"],
            database=os.environ["DB_NAME"]
        )
        self.cursor = self.cnx.cursor()

    def query(self, query: str, params: list=list()):
        self.cursor.execute(query, params)

        if query.split(" ")[0] == "SELECT":
            data = self.cursor.fetchall()
            return data

        self.cnx.commit()


def register_media():
    pass


def ask(arr: dict):
    for key in arr.keys():
        user_input = str(input(f"Enter {key}: "))
        arr[key] = user_input
    return arr


def register_drive():
    drive_information = {
        "name": "",
        "description": "",
    }
    ask(drive_information)
    print(drive_information)


def main():
    try:
        device_type = sys.argv[1] if sys.argv[1] in ["drive", "media"] else sys.exit()
    except Exception:
        print("Usage: py register.py [device_type]")
        sys.exit()

    if device_type == "media":
        register_media()

    if device_type == "drive":
        register_drive()


if __name__ == '__main__':
    load_dotenv()
    main()
