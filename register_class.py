import os
import sys
from db import DB
from fun import choose


class Register:
    def __init__(self):
        self.information = {
            "name": "",
            "description": "",
        }
        self.device_type = ""
        self.type_id = ""
        self.db = DB()

    def run(self):
        try:
            self.device_type = str(sys.argv[1]).lower() if sys.argv[1] in ["drive", "media"] else sys.exit()
        except IndexError:
            print(f"Usage: py {os.path.basename(__file__)} [device_type] ")
            sys.exit()

        print(f"#### Creating {self.device_type} ####")
        self.ask()

        fields = "(id, name, description)" if self.device_type == "drive" else "(id, name, description, type_id)"

        if self.device_type == "media":
            type_ids = [d[0] for d in self.db.query("SELECT name FROM media_type")]
            self.type_id = self.db.query(f"SELECT id FROM media_type WHERE name='{choose(type_ids, 'type')}'")[0][0]

        values = f"(uuid(), '{self.information['name']}', '{self.information['description']}')" \
            if self.device_type == "drive" else \
            f"(uuid(), '{self.information['name']}', '{self.information['description']}', '{self.type_id}')"
        query = f"INSERT INTO {self.device_type} {fields} VALUES {values}"

        self.db.query(query)

        print(f"{str(self.device_type).upper()} (\033[1m{self.information['name']}\033[0m) INSERTED INTO DATABASE")

    def ask(self):
        for key in self.information.keys():
            user_input = str(input(f"Enter {key}: "))
            self.information[key] = user_input


if __name__ == '__main__':
    register = Register()
    register.run()
