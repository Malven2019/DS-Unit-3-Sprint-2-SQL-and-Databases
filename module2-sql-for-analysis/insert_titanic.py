
import os
import csv
from dotenv import load_dotenv
import psycopg2
import json
from psycopg2.extras import execute_values

load_dotenv()  # loads contents of the .env file into the script's environment

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')

print(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST)

# Connect to SQL-hosted PostgreSQL
connection = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

print('CONNECTION', connection)
# A "cursor", a structure to iterate over db records to perform queries
cursor = connection.cursor()
print('CURSOR', cursor)

sql_create = '''DROP TABLE IF EXISTS
person_table;
  CREATE TABLE person_table (
  id        SERIAL PRIMARY KEY,
  Survived int,
  Pclass int,
  Name varchar(100),
  Sex varchar(6),
  age float,
  SiblingsorSpouses int,
  ParentsorChildren int,
  Fare float
);
'''
# Avoiding the table already exists error
cursor.execute(sql_create)

# Avoiding the table already exists error
connection.commit()

# Assign the titanic csv to a reader object
reader = list(csv.reader(open('titanic.csv', 'r')))

# Record count

record_count = 0

# Insert information into the database
for row in reader[1:]:

    sqlInsert = '''INSERT INTO person_table (Survived, Pclass, Name, Sex, age, SiblingsorSpouses, ParentsorChildren, Fare)
    VALUES(%s, %s, %s, %s, %s, %s, %s,%s) '''

   # Execute query and commit changes.
    cursor.execute(sqlInsert, (row[0],
                               row[1],
                               row[2],
                               row[3],
                               row[4],
                               row[5],
                               row[6],
                               row[7]
                               ))

    # Increment the record count.
    record_count += 1


connection.commit()

# How many passengers survived, and how many died?
num_passengers_s_d = '''
SELECT Survived, COUNT(*)
FROM person_table
GROUP by Survived;
'''
cursor.execute(num_passengers_s_d)
num_passengers_s_d = cursor.fetchall()
print('The number of passengers that died and survived was',
      num_passengers_s_d[0][1], 'and', num_passengers_s_d[1][1], 'respectively')


# #ow many passengers were in each class?
num_passengers_c = '''
SELECT pclass, COUNT(*)
FROM person_table
GROUP by pclass;
'''
cursor.execute(num_passengers_c)
num_passengers_c = cursor.fetchall()
print('The number of passengers in class 1 was',
      num_passengers_c[2][1], ', class 2:', num_passengers_c[1][1], 'and class 3:', num_passengers_c[0][1])


# How many passengers survived/died within each class?
num_passengers_s_d_1 = '''
SELECT Survived, COUNT(*)
FROM person_table
WHERE pclass = 1
GROUP by Survived;
'''
cursor.execute(num_passengers_s_d_1)
num_passengers_s_d_1 = cursor.fetchall()
print('The number of passengers that died and survived in class 1 was',
      num_passengers_s_d_1[0][1], 'and', num_passengers_s_d_1[1][1], 'respectively')


num_passengers_s_d_2 = '''
SELECT Survived, COUNT(*)
FROM person_table
WHERE pclass = 2
GROUP by Survived;
'''
cursor.execute(num_passengers_s_d_2)
num_passengers_s_d_2 = cursor.fetchall()
print('The number of passengers that died and survived in class 2 was',
      num_passengers_s_d_2[0][1], 'and', num_passengers_s_d_2[1][1], 'respectively')


num_passengers_s_d_3 = '''
SELECT Survived, COUNT(*)
FROM person_table
WHERE pclass = 3
GROUP by Survived;
'''
cursor.execute(num_passengers_s_d_3)
num_passengers_s_d_3 = cursor.fetchall()
print('The number of passengers that died and survived in class 3 was',
      num_passengers_s_d_3[0][1], 'and', num_passengers_s_d_3[1][1], 'respectively')

# What was the average age of survivors vs nonsurvivors?

avg_age_s_d = '''
SELECT Survived, AVG(age)
FROM person_table
GROUP by Survived;
'''
cursor.execute(avg_age_s_d)
avg_age_s_d = cursor.fetchall()
print('The average age of survivors vs non-survivors was',
      '{0:.2f}'.format(avg_age_s_d[1][1]), 'and', '{0:.2f}'.format(avg_age_s_d[0][1]), 'respectively')

# What was the average age of each passenger class?

avg_age_p_c = '''
SELECT pclass, AVG(age)
FROM person_table
GROUP by pclass;
'''
cursor.execute(avg_age_p_c)
avg_age_p_c = cursor.fetchall()
print('The average age, in years, of passenger class 1 was',
      '{0:.2f}'.format(avg_age_p_c[2][1]), ', class 2:', '{0:.2f}'.format(avg_age_p_c[1][1]), 'and class 3:', '{0:.2f}'.format(avg_age_p_c[0][1]))

# What was the average fare by passenger class?

avg_fare_p_c = '''
SELECT pclass, AVG(fare)
FROM person_table
GROUP by pclass;
'''
cursor.execute(avg_fare_p_c)
avg_fare_p_c = cursor.fetchall()
print('The average fare of passenger class 1 was',
      '{0:.2f}'.format(avg_fare_p_c[2][1]), ', class 2:', '{0:.2f}'.format(avg_fare_p_c[1][1]), 'and class 3:', '{0:.2f}'.format(avg_fare_p_c[0][1]))

# What was the average fare by survival?
avg_fare_s_d = '''
SELECT Survived, AVG(fare)
FROM person_table
GROUP by Survived;
'''
cursor.execute(avg_fare_s_d)
avg_fare_s_d = cursor.fetchall()
print('The average fare by survival was:',
      '{0:.2f}'.format(avg_fare_s_d[1][1]), 'for survivors and', '{0:.2f}'.format(avg_fare_s_d[0][1]), 'for non-survivors')


# How many siblings/spouses aboard on average, by passenger class?
avg_sib_spouses_p_c = '''
SELECT pclass, AVG(SiblingsorSpouses)
FROM person_table
GROUP by pclass;
'''
cursor.execute(avg_sib_spouses_p_c)
avg_sib_spouses_p_c = cursor.fetchall()
print('The average number of siblings and/or spouses for class 1 was',
      '{0:.2f}'.format(avg_sib_spouses_p_c[2][1]), ', class 2:', '{0:.2f}'.format(avg_sib_spouses_p_c[1][1]), 'and class 3:', '{0:.2f}'.format(avg_sib_spouses_p_c[0][1]))

# How many siblings/spouses aboard on average, by survival?

avg_sib_spouses_s_d = '''
SELECT Survived, AVG(SiblingsorSpouses)
FROM person_table
GROUP by Survived;
'''
cursor.execute(avg_sib_spouses_s_d)
avg_sib_spouses_s_d = cursor.fetchall()
print('The average number of siblings and/or spouses by survival was:',
      '{0:.2f}'.format(avg_sib_spouses_s_d[1][1]), 'for survivors and', '{0:.2f}'.format(avg_sib_spouses_s_d[0][1]), 'for non-survivors')


# How many parents/children aboard on average, by passenger class?

avg_parents_children_p_c = '''
SELECT pclass, AVG(parentsorchildren)
FROM person_table
GROUP by pclass;
'''
cursor.execute(avg_parents_children_p_c)
avg_parents_children_p_c = cursor.fetchall()
print('The average number of parents and/or children for class 1 was',
      '{0:.2f}'.format(avg_parents_children_p_c[2][1]), ', class 2:', '{0:.2f}'.format(avg_parents_children_p_c[1][1]), 'and class 3:', '{0:.2f}'.format(avg_parents_children_p_c[0][1]))

# How many parents/children aboard on average, by survival?

avg_parents_children_s_d = '''
SELECT Survived, AVG(parentsorchildren)
FROM person_table
GROUP by survived;
'''
cursor.execute(avg_parents_children_s_d)
avg_parents_children_s_d = cursor.fetchall()
print('The average number of siblings and/or spouses by survival was:',
      '{0:.2f}'.format(avg_parents_children_s_d[1][1]), 'for survivors and', '{0:.2f}'.format(avg_parents_children_s_d[0][1]), 'for non-survivors')


# Do any passengers have the same name?

duplicate_names = '''
SELECT name, COUNT(name)
FROM person_table
GROUP BY name
HAVING COUNT(name) > 1;
'''
cursor.execute(duplicate_names)
duplicate_names = cursor.fetchall()
print('The number of passengers with duplicate names is:',
      duplicate_names)

cursor.close()
connection.close()
