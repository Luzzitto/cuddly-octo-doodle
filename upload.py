import os
import sys
from db import DB
from fun import ask_path, get_hash
from datetime import datetime


class Upload:
    def __init__(self):
        # self.path = ask_path()
        self.path = "D:\\programming\\python\\cuddly-octo-doodle\\collection\\"
        self.id = ""
        self.db = DB()
        self.extensions = {}

    def run(self):
        try:
            arg = str(sys.argv[1]).upper()
            if self.db.query(f"SELECT id FROM media WHERE name='{arg}'"):
                self.id = self.db.query(f"SELECT id FROM media WHERE name='{arg}'")[0][0]
        except Exception:
            print("Missing an argument")
            sys.exit()

        for dirs, subdirs, files in os.walk(self.path):
            for f in files:
                file = os.path.join(dirs, f)
                file_information = {
                    "name": os.path.basename(file),
                    "size": os.path.getsize(file),
                    "hash": get_hash(file),
                    "created": os.path.getctime(file),
                    "extension": os.path.splitext(file)[1]
                }

                if file_information["extension"] in self.extensions:
                    self.extensions[file_information["extension"]] += 1
                else:
                    self.extensions[file_information["extension"]] = 1

                if self.db.query(f"SELECT hash FROM file WHERE hash='{file_information['hash']}'"):
                    print(f"{file_information['name']} has a duplicate")
                    continue

                # Register file information
                self.db.query(f"INSERT INTO file (id, name, size, hash, created) VALUES "
                              f"(uuid(), '{file_information['name']}', "
                              f"'{file_information['size']}', "
                              f"'{file_information['hash']}', "
                              f"'{datetime.fromtimestamp(file_information['created'])}')")
                # Get file_id
                file_id = self.db.query(f"SELECT id FROM file WHERE created='{datetime.fromtimestamp(file_information['created']).strftime('%Y-%m-%d %H:%M:%S')}'")[0][0]
                # Register relation to media
                self.db.query(f"INSERT INTO media_files (file_id, media_id) VALUES ('{file_id}', '{self.id}')")
        print("Finished uploading files")
        print(self.extensions)


if __name__ == '__main__':
    up = Upload()
    up.run()
