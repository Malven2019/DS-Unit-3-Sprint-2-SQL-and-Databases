import os
import sqlite3
import json

# construct a path to wherever your database exists
#DB_FILEPATH = "demo_data.sqlite3.db"
DB_FILEPATH = os.path.join(os.path.dirname(__file__), "demo_data.sqlite3")

connection = sqlite3.connect(DB_FILEPATH)
#print("CONNECTION:", connection)

# Avoiding the table already exists error
connection.commit()

print("CONNECTION", connection)
# A "cursor", a structure to iterate over db records to perform queries
cursor = connection.cursor()
print("CURSOR", cursor)

#sql_create = """CREATE TABLE demo (s text, x int, y int)"""

sql_create = """DROP TABLE IF EXISTS demo; CREATE TABLE demo (s text, x int, y int)"""

# Avoiding the table already exists error

# cursor.execute(sql_create)


# Avoiding the table already exists error
connection.commit()


# Avoiding the table already exists error
# count_characters = "SELECT COUNT(*) FROM charactercreator_character;"
# print(cursor.execute(count_characters).fetchall())

# cursor.execute(sql_create).fetchall()

# Avoiding the table already exists error
# connection.commit()

# Assign the demo_data to a reader object

# Record count

# Insert information into the database

sqlInsert = """INSERT INTO demo (s, x, y) VALUES (g, 3, 9), (v, 5, 7), (f, 8, 7);"""
cursor.execute(sqlInsert).fetchall()
# cursor.execute(sqlInsert).fetchall()
