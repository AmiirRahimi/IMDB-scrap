from crawl import get_movies_info,get250MoviesHref
import mysql.connector

cursor = None

# check if db exist connect to it and if does'nt exist create it 
db = mysql.connector.connect(
 host="localhost",
 user="root",
 password="0762",
)

cursor = db.cursor()

cursor.execute(f"SHOW DATABASES")

databases = cursor.fetchall()

new_data_bases = []

for database in databases:
 new_data_bases.append(database[0])

if 'IMDB' not in new_data_bases:
 cursor.execute('CREATE DATABASE IMDB')

cursor.execute("USE IMDB")

# check if table exist drop it
def dropTable(table_name):
 global cursor
 cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
 table_exists = cursor.fetchone()
 if table_exists:
  cursor.execute(f"DROP TABLE {table_name}")

# drop if exist and create movie table
def createMovieTable():
 global cursor
 dropTable('movie')
 cursor.execute("CREATE TABLE movie (id VARCHAR(255), title VARCHAR(255), year INT, runtime INT, parental_guide VARCHAR(255), gross_us_canada INT)")

# drop if exist and create person table
def createPersonTable():
 global cursor
 dropTable('person')
 cursor.execute("CREATE TABLE person (id VARCHAR(255), name VARCHAR(255))")

# drop if exist and create cast table
def createCastTable():
 global cursor
 dropTable('cast')
 cursor.execute("CREATE TABLE cast (id INT AUTO_INCREMENT PRIMARY KEY, movie_id VARCHAR(255), person_id VARCHAR(255))")

# drop if exist and create crew table
def createCrewTable():
 global cursor
 dropTable('crew')
 cursor.execute("CREATE TABLE crew (id INT AUTO_INCREMENT PRIMARY KEY, movie_id VARCHAR(255), person_id VARCHAR(255), role VARCHAR(255))")

# drop if exist and create genre table
def createGenreTable():
 global cursor
 dropTable('genre')
 cursor.execute("CREATE TABLE genre (id INT AUTO_INCREMENT PRIMARY KEY, movie_id VARCHAR(255), genre VARCHAR(255))")

# method to call table create methods
def createTables():
 createMovieTable()
 createPersonTable()
 createCastTable()
 createCrewTable()
 createGenreTable()

# run method to call table create methods
createTables()

# insert into movie table
def insertIntoMovie(info):
 sql = "INSERT INTO movie (id, title , year, runtime, parental_guide, gross_us_canada) VALUES (%s,%s,%s,%s,%s,%s)"
 value = (info['id'], info['title'], info['year'], info['runtime'], info['parental_guide'], info['gross_us_canada'])
 cursor.execute(sql,value)
 db.commit()

# insert into person table
def insertDifferentPersons(id, name):
 sql = "INSERT INTO person (id, name) VALUES (%s,%s)"
 value = (id, name)
 cursor.execute(sql,value)
 db.commit()

# check if person exist in table
def checkIfPersonExist(id):
 try:
  sql = "SELECT * FROM person WHERE id = %s"
  cursor.execute(sql, (id,))
  result = cursor.fetchone()
  if result:
   return True
  return False
 except mysql.connector.Error as err:
  return False
 

 # insert data (director, writer, star) with another method into person table
def insertIntoPerson(info):
  if not checkIfPersonExist(info['director']['id']):
     insertDifferentPersons(info['director']['id'], info['director']['name'])
  for writer in info['writer']:
   if not checkIfPersonExist(writer['id']):
    insertDifferentPersons(writer['id'], writer['name'])
  for actor in info['star']:
   if not checkIfPersonExist(actor['id']):
    insertDifferentPersons(actor['id'], actor['name'])

def insertDifferentPersonsIntoCast(person_id, movie_id):
 sql = "INSERT INTO cast (movie_id, person_id) VALUES (%s, %s)"
 cursor.execute(sql, (movie_id, person_id))
 db.commit()
 
def insertDifferentPersonsIntoCrew(person_id, movie_id, role):
 sql = "INSERT INTO crew (movie_id, person_id, role) VALUES (%s, %s, %s)"
 cursor.execute(sql, (movie_id, person_id, role))
 db.commit()

def insertIntoCast(info):
 for actor in info['star']:
  insertDifferentPersonsIntoCast(actor['id'], info['id'])

def insertIntoCrew(info):
 insertDifferentPersonsIntoCrew(info['director']['id'], info['id'], 'Director')
 for writer in info['writer']:
  insertDifferentPersonsIntoCrew(writer['id'], info['id'], 'Writer')

def insertIntoGenre(info):
 sql = "INSERT INTO genre (movie_id, genre) VALUES (%s, %s)"
 for genre in info['genre']:
  cursor.execute(sql, (info['id'], genre))
  db.commit()

def insertMovieInfo():
 hrefs = get250MoviesHref()
 for href in hrefs:
  info = get_movies_info(href)
  insertIntoMovie(info)
  insertIntoPerson(info)
  insertIntoCast(info)
  insertIntoCrew(info)
  insertIntoGenre(info)


# start fetch and insert into tables
insertMovieInfo()

  












