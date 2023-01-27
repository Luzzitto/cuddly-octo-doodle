import os
import sys
from db import DB


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
    db = DB()
    db.query(f"INSERT INTO drive (id, name, description) VALUES (uuid(), '{drive_information['name']}', '{drive_information['description']}')")
    print(f"INSERTED INTO DATABASE")


def ask_path(path):
    while True:
        dirs = os.listdir(path)
        count = len(dirs)
        for i, p in enumerate(dirs):
            if not os.path.isdir(os.path.join(path, p)):
                continue
            print(f"{i}: {os.path.join(path, p)}")
        user_input = input(f"Select path ({path}): ")
        if user_input.isnumeric() and int(user_input) in range(0, count):
            path = os.path.join(path, dirs[int(user_input)])
        elif user_input in ["done", "exit"]:
            return path
        else:
            print(f"{user_input} is invalid option!")


def choose(options: list, name: str = "option"):
    while True:
        for i, option in enumerate(options):
            print(f"{i}: {option}")
        user_input = input(f"Select {name}: ")
        if user_input.isnumeric() and int(user_input) in range(0, len(options)):
            return options[int(user_input)]


def register_media():
    # Collect information
    media_information = {
        "name": "",
        "description": ""
    }
    ask(media_information)

    db = DB()
    type_ids = [d[0] for d in db.query("SELECT name FROM media_type")]
    get_type_id = db.query(f"SELECT id FROM media_type WHERE name='{choose(type_ids, 'type')}'")[0][0]

    # Upload to database
    db.query(f"INSERT INTO media (id, name, description, type_id) VALUES (uuid(), '{media_information['name']}', '{media_information['description']}', '{get_type_id}')")
    last_id = db.query(f"SELECT id FROM media WHERE name='{media_information['name']}' AND type_id='{get_type_id}'")[0][0]
    print(f"INSERTED INTO DATABASE: {last_id}")


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
    main()
