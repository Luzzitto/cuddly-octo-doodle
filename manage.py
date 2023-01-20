import sys
import os


def init():
    exit_command = ["done", "goodbye", "complete"]
    absolute_exit_command = ["exit", "die"]
    print("#### Initializing Project ####")
    print("Creating `collection` folder...")
    collection_folder = os.path.join(os.getcwd(), "collection")

    if os.path.exists(collection_folder):
        print("collection folder already exists! Please delete to continue")
        sys.exit()
    else:
        os.makedirs(collection_folder)
        print("Folder created!")

    media_list = {}

    while True:
        media = str(input("Enter media: ")).lower()

        if media in exit_command:
            break
        elif media in absolute_exit_command:
            sys.exit()

        if media not in media_list:
            media_list[media] = []
        else:
            print(f"{media} already exists!")

        while True:
            media_type = str(input(f"Enter {media} type: ")).lower()
            if media_type in exit_command:
                break
            elif media_type in absolute_exit_command:
                sys.exit()

            if media_type not in media_list[media]:
                media_list[media].append(media_type)

    for key in media_list.keys():
        print(f"Making {key} directory...")
        key_path = os.path.join(collection_folder, key)
        os.makedirs(key_path)
        for subkey in media_list[key]:
            print(f"Making {key}/{subkey} directory...")
            os.makedirs(os.path.join(key_path, subkey))

    print(media_list)


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
