import hashlib
import win32api
import os


def choose(options: list, name: str = "option") -> str:
    """
    Takes a selection and return a selected option
    Args:
        options (list): list of selection
        name (str): name for options
    Return:
        str: Selected option from list of options
    """
    while True:
        for i, option in enumerate(options):
            print(f"{i}: {option}")

        user_input = input(f"Select {name}: ")

        if user_input.isnumeric() and int(user_input) in range(0, len(options)):
            return options[int(user_input)]
        elif user_input in ["exit", "quit", "die", "goodbye", "done"]:
            return "done"
        else:
            print(f"{user_input} is invalid!")


# https://www.quickprogrammingtips.com/python/how-to-calculate-sha256-hash-of-a-file-in-python.html
def get_hash(file_path):
    sha1 = hashlib.sha1()
    read_size = 1024 ** 2
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(read_size), b""):
            sha1.update(byte_block)
    return sha1.hexdigest()


def ask_path():
    # Get drive
    drives = [drive for drive in str(win32api.GetLogicalDriveStrings()).split('\x00')if drive not in ['']] # 'C:\\', 'D:\\',
    root_dir = os.path.normpath(choose(drives))
    while True:
        dirs = [d for d in os.listdir(root_dir) if os.path.join(root_dir, d)]
        user_input = choose(dirs, f"directory {root_dir}")
        print()

        if user_input == "done":
            break

        root_dir = os.path.join(root_dir, user_input)
    return root_dir
