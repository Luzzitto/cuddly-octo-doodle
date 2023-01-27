import mysql.connector
import os
from dotenv import load_dotenv


class DB:
    def __init__(self):
        load_dotenv()
        self.cnx = mysql.connector.connect(
            host=os.environ["DB_HOST"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASS"],
            database=os.environ["DB_NAME"]
        )
        self.cursor = self.cnx.cursor()

    def query(self, query: str, params: list=list()):
        self.cursor.execute(query, params)

        if query.split(" ")[0] == "SELECT":
            data = self.cursor.fetchall()
            return data

        self.cnx.commit()

    def last_id(self):
        return self.cursor.lastrowid