import mysql.connector
import os
from os.path import join, dirname
from datetime import date, datetime

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Db_Helper:
    db = None

    def __init__(self):
        dbhost = '35.184.181.27'
        dbuser = 'root'
        dbpassword = 'bHrNmtbKkkM9bav8'
        dbname = 'fbsprod'
        self.db = mysql.connector.connect(
            host=dbhost,
            user=dbuser,
            passwd=dbpassword,
            database=dbname
        )

    def get_teams(self):
        cursor = self.db.cursor()
        query = """SELECT * FROM fbsprod.teams;"""
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def close(self):
        self.db.close()