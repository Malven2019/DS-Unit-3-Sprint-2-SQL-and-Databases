import os
import sqlite3

# construction of  a path to wherever the database exists
# DB_FILEPATH = "rpg_db.sqlite3.db"
DB_FILEPATH = os.path.join(os.path.dirname(__file__), "rpg_db.sqlite3")

connection = sqlite3.connect(DB_FILEPATH)
# print("CONNECTION:", connection)

cursor = connection.cursor()
# print("CURSOR", cursor)

# How many total characters?
# In Table charactercreator_character

# Commenting out the code on why they are taking a specific action
# print(len(c1.execute('SELECT * FROM charactercreator_character;').fetchall()[0][2:]))

count_characters = "SELECT COUNT(*) FROM charactercreator_character;"
print("The total number of characters is",
      cursor.execute(count_characters).fetchall())

# How many characters of each specific subclass?

count_characters_cleric = "SELECT COUNT(*) FROM charactercreator_cleric;"
print("The total number of cleric characters is",
      cursor.execute(count_characters_cleric).fetchall())

count_characters_fighter = "SELECT COUNT(*) FROM charactercreator_fighter;"
print("The total number of fighter characters is",
      cursor.execute(count_characters_fighter).fetchall())

count_characters_mage = "SELECT COUNT (*) FROM charactercreator_mage;"
print("The total number of mage characters is",
      cursor.execute(count_characters_mage).fetchall())

count_characters_necromancer = "SELECT COUNT(*) FROM charactercreator_necromancer;"
print("The total number of necromancer characters is",
      cursor.execute(count_characters_necromancer).fetchall())

count_characters_thief = "SELECT COUNT (*) FROM charactercreator_thief;"
print("The total number of thief characters is",
      cursor.execute(count_characters_thief).fetchall())

# How many total Items?

count_armory_items = "SELECT COUNT (*) FROM armory_item;"
print("The total number of armory items is",
      cursor.execute(count_armory_items).fetchall())

# How many of the Items are weapons? How many are not?

count_armory_weapons = "SELECT COUNT (*) FROM armory_weapon;"
print("The total number of armory weapons is",
      cursor.execute(count_armory_weapons).fetchall())

# Items which are not weapons

armory_not_weapons = (174 - 37)
print("The number of non-weapon armory items is:", armory_not_weapons)

# How many Items does each character have? (Return first 20 rows)

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

print("The average items per character", cursor.execute(
    average_items_per_character).fetchall())


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
print("The average weapons per character", cursor.execute(
    average_weapons_per_character).fetchall())
