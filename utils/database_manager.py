import sqlite3
from docopt import docopt
import getpass
import sys

class DatabaseManager():
    def __init__(self, path) -> None:
        self.path = path
        self.conn = None
        self.cursor = None

    def connect(self) -> None:
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()
        if not self.conn and not self.cursor:
            print("\nconnect success.\n")

    def build(self) -> None:
        self.connect()

        self.cursor.execute("create table if not exists facebook(id text, pass text)")
        self.cursor.execute("create table if not exists instagram(id text, pass text)")
        self.close()
        print("database file created.")
    
    def edit(self) -> None:
        self.connect()

        print("\ntable reset.")
        self.cursor.execute("delete from facebook")
        self.cursor.execute("delete from instagram")
        print("table reset success.\n")
        
        print("get new infomation.\n" + '-' *  20)
        facebook_id = input("facebook id: ")
        facebook_pw = getpass.getpass("facebook pw: ")
        insta_id = input("instagram id: ")
        insta_pw = getpass.getpass("instagram pw: ")
        print('-' * 20)

        print("write account information into database.")
        self.cursor.execute(f"insert into facebook values('{facebook_id}', '{facebook_pw}')")
        self.cursor.execute(f"insert into instagram values('{insta_id}', '{insta_pw}')")
        self.conn.commit()
        self.close()
        print("write success.")

    def get_insta_acc(self) -> tuple:
        self.connect()
        self.cursor.execute("select * from instagram")
        result = self.cursor.fetchall()[0]
        return result

    def get_facebook_acc(self) -> tuple:
        self.connect()
        self.cursor.execute("select * from facebook")
        result = self.cursor.fetchall()[0]
        return result

    def close(self):
        self.cursor.close()
        self.conn.close()
        self.cursor = None
        self.conn = None

def main():
    args = docopt("""
    Usage:
        database_manager.py [-c] [-e] [-h]

    Options:
        -c        create database file
        -e        edit account data
        -h        show this help message and exit
    """)
    create = args.get('-c', "")
    edit = args.get('-e', "")

    if len(sys.argv) == 1:
        print("usage: database_manager.py <options...>")

    builder = DatabaseManager("user_account.db")

    if create:
        builder.build()
    if edit:
        builder.edit()
    

if __name__ == '__main__':
    main()