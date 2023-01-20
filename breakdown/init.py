import json
import os
import sys


def input_select(name: str, subsection: bool):
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
            second_input = str(input(f"Enter {first_input}: ")).lower()

            if second_input in exit_command:
                break
            elif second_input in absolute_exit_command:
                sys.exit()

            if second_input not in arr[first_input]:
                arr[first_input][second_input] = []

    return arr


def main():
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
    output["media"] = input_select("media", True)

    print("")

    print("Making drive")
    output["drive"] = input_select("drive", False)

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


if __name__ == '__main__':
    main()
