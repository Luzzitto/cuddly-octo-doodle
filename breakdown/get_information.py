import datetime
import hashlib
import json
import os
import math
import sys
import threading

from queue import Queue


class Folder:
    def __init__(self, src, num_threads=8):
        self.src = src
        self.files = []
        self.total = 0
        self.num_threads = num_threads
        self.queue = Queue()
        self.create_workers()
        self.fill_queue()

    def create_workers(self):
        for _ in range(self.num_threads):
            t = threading.Thread(target=self.get_file_information)
            t.daemon = True
            t.start()

    def get_file_information(self):
        while True:
            src_item, index = self.queue.get()
            print(f"{index}/{self.total}: {os.path.basename(src_item)}")
            f = File(src_item)
            self.files.append(f.run())
            self.queue.task_done()

    def fill_queue(self):
        self.total = len(os.listdir(self.src))
        for i, item in enumerate(os.listdir(self.src)):
            self.queue.put((os.path.join(self.src, item), i))

    def run(self):
        self.queue.join()
        with open(f"transactions/{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json", "w") as fi:
            json.dump(self.files, fi, indent=4, ensure_ascii=False)


class File:
    def __init__(self, path):
        self.path = path
        self.read_size = 1024 ** 2

    def get_size(self):
        return os.path.getsize(self.path)

    def get_hash(self):
        sha1 = hashlib.sha1()
        with open(self.path, "rb") as f:
            for byte_block in iter(lambda: f.read(self.read_size), b""):
                sha1.update(byte_block)
        return sha1.hexdigest()

    def get_ctime(self):
        return os.path.getctime(self.path)

    def get_name(self):
        return os.path.basename(self.path)

    def get_extension(self):
        return os.path.splitext(self.path)[1]

    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def run(self):
        file_information = {"name": "", "extension": "", "size": "", "hash": "", "created": ""}

        # print("\tFile name", end=" = ")
        file_information["name"] = self.get_name()
        # print(file_information["name"], end="\n")

        # print("\tFile extension", end=" = ")
        file_information["extension"] = self.get_extension()
        # print(f'{str(file_information["extension"][1:]).lower()}', end="\n")

        # print("\tFile size", end=" = ")
        file_information["size"] = self.get_size()
        # print(self.convert_size(file_information["size"]), end="\n")

        # print("\tFile hash", end=" = ")
        file_information["hash"] = self.get_hash()
        # print(file_information["hash"], end="\n")

        # print("\tFile created", end=" = ")
        file_information["created"] = self.get_ctime()
        # print(datetime.datetime.fromtimestamp(file_information["created"]).strftime("%a, %B %d, %Y %I:%M:%S %p"), end="\n")

        return file_information


if __name__ == '__main__':
    try:
        folder_path = str(sys.argv[1])
    except Exception:
        print("Missing folder")
        sys.exit()

    if not os.path.isdir(folder_path):
        print(f"{folder_path} is not a directory")
        sys.exit()

    folder = Folder(folder_path)
    folder.run()
