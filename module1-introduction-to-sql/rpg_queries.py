import os
import sqlite3

# construct a path to wherever your database exists
#DB_FILEPATH = "rpg_db.sqlite3.db"
DB_FILEPATH = os.path.join(os.path.dirname(__file__), "rpg_db.sqlite3")

connection = sqlite3.connect(DB_FILEPATH)
#print("CONNECTION:", connection)

cursor = connection.cursor()
#print("CURSOR", cursor)

# How many total characters?
# In Table charactercreator_character

count_characters = "SELECT COUNT(*) FROM charactercreator_character;"
print(cursor.execute(count_characters).fetchall())

# How many characters of each specific subclass?

count_characters_cleric = "SELECT COUNT(*) FROM charactercreator_cleric;"
print(cursor.execute(count_characters_cleric).fetchall())

count_characters_fighter = "SELECT COUNT(*) FROM charactercreator_fighter;"
print(cursor.execute(count_characters_fighter).fetchall())

count_characters_mage = "SELECT COUNT (*) FROM charactercreator_mage;"
print(cursor.execute(count_characters_mage).fetchall())

count_characters_necromancer = "SELECT COUNT(*) FROM charactercreator_necromancer;"
print(cursor.execute(count_characters_necromancer).fetchall())

count_characters_thief = "SELECT COUNT (*) FROM charactercreator_thief;"
print(cursor.execute(count_characters_thief).fetchall())

# How many total Items?

count_armory_items = "SELECT COUNT (*) FROM armory_item;"
print(cursor.execute(count_armory_items).fetchall())

# How many of the Items are weapons? How many are not?

count_armory_weapons = "SELECT COUNT (*) FROM armory_weapon;"
print(cursor.execute(count_armory_weapons).fetchall())

# Items which are not weapons

armory_not_weapons = (174 - 37)
print("Number of items which are not weapons is:", armory_not_weapons)

# How many Items does each character have? (Return first 20 rows)

# merged_query = '''
# SELECT * FROM (charactercreator_character ,
# charactercreator_mage)
# WHERE
#charactercreator_character.character_id = charactercreator_mage.character_ptr_id;
# '''
# print(cursor.execute(merged_query).fetchall())

# merged1_query ='''
#SELECT * FROM
# charactercreator_character AS cc,
# armory_item AS ai,
# charactercreator_character_inventory AS cci
# WHERE
# cc.character_id = cci.character_id AND
#ai.item_id = cci.item_id;
#
# '''
# print(cursor.execute(merged1_query).fetchall())

item_number = '''
SELECT cc.character_id, COUNT(ai.item_id)
FROM
charactercreator_character AS cc,
armory_item AS ai,
charactercreator_character_inventory AS cci
WHERE
cc.character_id = cci.character_id AND
ai.item_id = cci.item_id
GROUP BY cc.character_id
LIMIT 20;
'''
print(cursor.execute(item_number).fetchall())

# How many Weapons does each character have? (Return first 20 rows)

# merged_query = '''
# SELECT * FROM (charactercreator_character ,
# charactercreator_mage)
# WHERE
#charactercreator_character.character_id = charactercreator_mage.character_ptr_id;
# '''
# print(cursor.execute(merged_query).fetchall())

# merged1_query ='''
#SELECT * FROM
# charactercreator_character AS cc,
# armory_weapon AS aw,
# charactercreator_character_inventory AS cci
# WHERE
# cc.character_id = cci.character_id AND
#aw.item_ptr_id = cci.item_id;
# '''
# print(cursor.execute(merged1_query).fetchall())

weapon_number = '''
SELECT cc.character_id, COUNT(aw.item_ptr_id)
FROM
charactercreator_character AS cc,
charactercreator_character_inventory AS cci,
armory_weapon AS aw
WHERE
cc.character_id = cci.character_id
AND
cci.item_id = aw.item_ptr_id
GROUP BY cc.character_id
LIMIT 20;
'''
print(cursor.execute(weapon_number).fetchall())

# On average,how many items does each character have?
# assume: include characters that do not have any items
# Output : two columns character_id, item_count
# row per character(302 total)

average_items_per_character = '''
SELECT AVG(item_count) as avg_items_per_char
FROM(
	SELECT
	cc.character_id,
	--cc.'name',
	--cci.*,
	--ai.*,
	count(distinct ai.item_id) as item_count
	FROM charactercreator_character cc
	LEFT JOIN charactercreator_character_inventory cci
	ON cc.character_id=cci.character_id
	LEFT JOIN armory_item ai
	ON cci.item_id=ai.item_id
	GROUP BY cc.character_id
)
'''

print(cursor.execute(average_items_per_character).fetchall())


# On average,how many weapons does each character have?
# assume: include characters that do not have any weapons
# two columns character_id, weapon_count
# row per character (302 total)

average_weapons_per_character = '''
SELECT AVG(weapon_count) as avg_weapons_per_char
FROM(
	SELECT
	cc.character_id,
	--cc.'name',
	--cci.*,
	--aw.*,
	count(distinct aw.item_ptr_id) as weapon_count
	FROM charactercreator_character cc
	LEFT JOIN charactercreator_character_inventory cci
	ON cc.character_id=cci.character_id
	LEFT JOIN armory_weapon aw
	ON cci.item_id=aw.item_ptr_id
	GROUP BY cc.character_id
)
'''
print(cursor.execute(average_weapons_per_character).fetchall())
