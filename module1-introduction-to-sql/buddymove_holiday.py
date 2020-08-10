#!/usr/bin/env python

"""
Buddy csv
"""

import pandas as pd
import sqlite3

# Count the number of rows you should have (249)
df = pd.read_csv('buddymove_holidayiq.csv')
print(df.shape)

conn = sqlite3.connect('buddymove_holidayiq.sqlite3')
curs = conn.cursor()
df.to_sql('user_review', conn)

counts = """SELECT COUNT (*) FROM user_review;"""

# How many users who reviewed at least 100 'Nature' also reviewed
# at least '100' in Shopping.
print("Total number of users:", curs.execute(counts).fetchall()[0][0])

assign2 = """SELECT COUNT (*) FROM user_review WHERE Nature >= 100 AND Shopping >= 100"""

print("The number of users who scored 100 or more in both nature and shopping is",
      curs.execute(assign2).fetchall()[0][0])
