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
    
    def insert_odds(self, games):
        cursor = self.db.cursor()
        insert_statement = """INSERT INTO fbsprod.suggested_bets_current
            (start_time, home_team, away_team, bovada_odds, dk_odds, wh_odds, bovada_last_updated, dk_last_updated, wh_last_updated, minimum_suggested_odds, pick)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        truncate_statement = "truncate table fbsprod.suggested_bets_current;"
        cursor.execute(truncate_statement)
        cursor.executemany(insert_statement, games)
        self.db.commit()
    
    def insert_odds_historical(self, games):
        cursor = self.db.cursor()
        insert_statement = """INSERT INTO fbsprod.suggested_bets_historical
            (start_time, home_team, away_team, bet_site, odds, last_updated, minimum_suggested_odds, pick)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        Delete_statement = "Delete FROM fbsprod.suggested_bets_historical where start_time > CONVERT_TZ(now(),'Etc/GMT','US/Central');"
        cursor.execute(Delete_statement)
        cursor.executemany(insert_statement, games)
        self.db.commit()

    def close(self):
        self.db.close()