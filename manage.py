import os
import sys

def register():
    args = sys.argv[2:]
    register_type = args[0]
    allowed_register_type = ["hdd", "media"]

def init():
    dirs = [
        os.path.join(os.getcwd(), "collection"),
    ]
    print("#### Program Initializing ####")
    print(f"Making dir: \x1b[0;37;44m {dir[0]} \x1b[0m")
    if not os.path.exists(dirs[0]):
        os.makedirs(dirs[0])
    
    print("Making directories for media type ")
    media_types = {}
    terminator_keywords = ["done", "break", "complete"]
    while True:
        user_input = input("Media type: ")
        if user_input in terminator_keywords:
            break
        media_types[user_input] = []
        while True:
            media_name = input("Media name: ")
            if media_name in terminator_keywords:
                break
            media_types[user_input].append(media_name)
            


def main():
    try:
        subcommand = sys.argv[1]
    except Exception:
        print("Usage: py manage.py [subcommand]")
    
    if subcommand in ["register", "init"]:
        globals()[subcommand]()
    
if __name__ == "__main__":
    main()
