import datetime
import json
import sys
import os
import win32api


def input_choice(name: str, subsection: bool):
    absolute_exit_command = ["exit", "quit", "die"]
    exit_command = ["done", "goodbye", "complete", "ok"]
    arr = {} if subsection else []
    while True:
        first_input = str(input(f"Enter {name}: ")).lower()

        if first_input in exit_command:
            if not subsection:
                return arr
            break
        elif first_input in absolute_exit_command:
            sys.exit()

        if first_input not in arr:
            if subsection:
                arr[first_input] = []
            else:
                arr.append(first_input)

        if not subsection:
            continue

        while True:
            second_input = str(input(f"Enter {first_input}: "))

            if second_input in exit_command:
                break
            elif second_input in absolute_exit_command:
                sys.exit()

            if second_input not in arr[first_input]:
                arr[first_input][second_input] = []
    return arr


def init():
    output = {}
    print("#### Initializing Project ####")
    print("Creating `collection` folder...")
    collection_folder = os.path.join(os.getcwd(), "collection")

    if os.path.exists(collection_folder):
        print("collection folder already exists!")
    else:
        os.makedirs(collection_folder)
        print("Folder created!")

    print("Making Media")
    output["media"] = input_choice("media", True)

    print("")

    print("Making drive")
    output["drive"] = input_choice("drive", False)

    media_path = os.path.join(collection_folder, "media")
    os.makedirs(media_path)
    drive_path = os.path.join(collection_folder, "drive")
    os.makedirs(drive_path)

    for key in output["media"].keys():
        print(f"Making {key} directory...")
        key_path = os.path.join(media_path, key)
        os.makedirs(key_path)

        for subkey in output["media"][key]:
            print(f"Making {key}/{subkey} directory...")
            os.makedirs(os.path.join(key_path, subkey))

    for drive in output["drive"]:
        print(f"Making {drive}'s drive")
        os.makedirs(os.path.join(drive_path, drive))

    with open(os.path.join(collection_folder, "devices.json"), "w") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print("Completed!")


def choose(options: list):
    while True:
        for i, option in enumerate(options):
            print(f"{i}: {option}")
        user_input = input("Select option: ")

        if user_input.isnumeric() and int(user_input) in range(0, len(options)):
            break
    return options[int(user_input)]


def remove_default_drives(variable):
    if variable in ['C:\\', 'D:\\']:
        return False
    else:
        return True


def register():
    try:
        device_type = sys.argv[2]
    except Exception:
        print("Usage: py manage.py register [device_type]")
        sys.exit()

    list_of_devices = filter(remove_default_drives, win32api.GetLogicalDriveStrings().split('\0')[:-1])
    device = choose(list_of_devices)
    path = os.path.join(os.getcwd(), "collection", "media" if device_type == "media" else "drive")

    # Register drive
    while True:
        ask_user = input("Enter drive name: ")
        if ask_user in os.listdir(path):
            path = os.path.join(path, str(ask_user).lower())
            break

    # Register media
    device_name = choose(os.listdir(path))
    device_type = choose(os.listdir(os.path.join(path, device_name)))

    register_device_name = input_choice("device_name", False)

    with open(os.path.join(path, device_name, device_type, f"{register_device_name}.json"), "w") as f:
        device_info = {
            "name": device_name,
            "type": device_type,
            "files": [],
            "transactions": [
                datetime.datetime.now().timestamp(),
            ]
        }
        json.dump(device_info, f, indent=4, ensure_ascii=False)


def main():
    try:
        subcommand = sys.argv[1]
    except Exception:
        subcommand = "help"

    if subcommand in ["init", "register"]:
        globals()[subcommand]()

    if subcommand == "help":
        print("Usage: py manage.py [subcommand] [nargs]")
        print("    \033[1mSubcommand \033[0m")
        print("init")
        print("\tInitialize application")
        print("register")
        print("\tRequire `media` or `drive` as an argument")

    sys.exit()


if __name__ == '__main__':
    main()
