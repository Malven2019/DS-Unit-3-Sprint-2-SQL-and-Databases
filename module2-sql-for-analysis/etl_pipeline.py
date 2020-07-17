
import os
import csv
from dotenv import load_dotenv
import psycopg2
import json
import sqlite3
from psycopg2.extras import execute_values

load_dotenv()  # loads contents of the .env file into the script's environment

DB_NAME = os.getenv('DB_NAME', default='OOPS')
DB_USER = os.getenv('DB_USER', default='OOPS')
DB_PASSWORD = os.getenv('DB_PASSWORD', default='OOPS')
DB_HOST = os.getenv('DB_HOST', default='OOPS')

# Filepath to connect to sqlite database
DB_FILEPATH = os.path.join(os.path.dirname(
    __file__), "..", "module1-introduction-to-sql", "rpg_db.sqlite3")


class SqliteService():

    def __init__(self, db_filepath=DB_FILEPATH):
        self.connection = sqlite3.connect(db_filepath)
        self.cursor = self.connection.cursor()

    def fetch_characters(self):
        self.cursor.execute(
            'SELECT * FROM charactercreator_character;').fetchall()

        # class ElephantSQLService():

        #     def __init__(self):
        #         self.connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        #     def __init__(self, db_name=DB_NAME, db_user=DB_USER, db_password=DB_PASSWORD, db_host=DB_HOST):
        #         self.connection = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host)
        #         self.cursor = self.connection.cursor()

        #     def create_characters_table(self):


class StorageService():
    if __name__ == '__main__':

        #  EXTRACT AND TRANSFORM

        sqlite_service = SqliteService()

        characters = sqlite_service.fetch_characters()
        print(type(characters), len(characters))
        print(characters[0])

        exit()

        # LOAD

        pg_service = ElephantSQLService()

        pg_service.create_characters_table()

        pg_service.insert_characters(characters)
