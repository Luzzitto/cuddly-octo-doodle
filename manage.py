import hashlib
import os
import sys
import win32api

from db import DB
from register import choose, ask_path


def get_hash(file_path):
    sha1 = hashlib.sha1()
    read_size = 1024 ** 2
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(read_size), b""):
            sha1.update(byte_block)
    return sha1.hexdigest()


def main():
    db = DB()
    try:
        arg = str(sys.argv[1]).upper()
        if db.query(f"SELECT id FROM media WHERE name='{arg}'"):
            id = db.query(f"SELECT id FROM media WHERE name='{arg}'")[0][0]
    except Exception:
        print("Missing an argument")
        sys.exit()

    # Insert Start transaction to database
    message = f"{id} is uploading files"
    db.query(f"INSERT INTO transaction (program, status, message) VALUES ('manage.py', 'START', '{message}')")

    # Get Drive
    drives = [drive for drive in win32api.GetLogicalDriveStrings().split('\000') if drive not in ['', 'D:\\', 'C:\\']]
    drive_to_use = choose(drives, drives)

    # Ask for path
    drive_path = ask_path(drive_to_use)

    # Iterate through the files list
    for dirs, subdirs, files in os.wak(drive_path):
        for f in files:
            file = os.path.join(dirs, f)
            file_information = {
                "name": os.path.basename(file),
                "size": os.path.getsize(file),
                "hash": get_hash(file),
                "created": os.path.getctime(file)
            }

            # Register file information
            db.query(f"INSERT INTO files (name, size, hash, created) VALUES ('{file_information['name']}', '{file_information['size']}', '{file_information['hash']}', '{file_information['created']}')")

    # End transaction to database
    message = f"{id} has finished uploading files, File count: #"
    db.query(f"INSERT INTO transaction (program, status, message) VALUES ('manage.py', 'END', '{message}')")


if __name__ == '__main__':
    main()
