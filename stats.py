import sys
import gspread
import sqlite3
from datetime import datetime
from pprint import pprint
from selenium import webdriver
from oauth2client.service_account import ServiceAccountCredentials
from time import sleep


class GSheet:
    def __init__(self, creds, sheet):
        self.scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(creds, self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open(sheet).sheet1


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_table(conn):

    with conn:
        #
        sql = """
            CREATE TABLE IF NOT EXISTS  stats(
            rowid integer PRIMARY KEY,
            event_id integer,
            Date text,
            Event text,
            Placing integer,
            Faction text,
            GA text,
            Use integer,
            GamesPlayed integer,
            NumberofWins integer,
            Player text,
            FactionKey text); """
        cur = conn.cursor()
        cur.execute(sql)


if __name__ == '__main__':


    database = "stats_sqlite.db"
    mysheet = GSheet("private.json", "stats")
    matches = mysheet.sheet.get_all_records()
    print(len(matches))

    # create a database connection
    conn = create_connection(database)
    create_table(conn)

    conn = create_connection(database)
    with conn:

        for match in matches:
            sql = ''' INSERT INTO stats(rowid,event_id,Date,Event,Placing,Faction,GA,Use,GamesPlayed,NumberofWins,Player,FactionKey)
                      VALUES(?,?,?,?,?,?,?,?,?,?,?,?) '''
            cur = conn.cursor()
            cur.execute(sql, match)

