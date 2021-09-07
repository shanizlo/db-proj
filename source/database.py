import sqlite3

from source.entities import *

# _conn = sqlite3.Connection
# _cursor = sqlite3.Cursor
connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

sql_file = open("init_script.sql")
sql_as_string = sql_file.read()
cursor.executescript(sql_as_string)

def insert_song(song):
    with connection:
        cursor.execute("INSERT INTO songs VALUES (:song_id, :author, :title, :album, :copyright , :creation_date)",
                       {'song_id': None, 'author': song.author, 'title': song.title, 'album': song.album , 'copyright': song.copyright, 'creation_date': song.creation_date})

def insert_word(word):
    with connection:
        cursor.execute("INSERT INTO words VALUES (:word_id, :word_value, :word_length)",
                       {'word_id': None, 'word_value': word.value, 'word_length': word.length})




#################################### Tests ###############
song1 = Song("Freddie Mercury", "Love of my life" )
word1 = Word("hello")

insert_song(song1)
insert_word(word1)


print(word1.value)

for row in cursor.execute("SELECT * FROM songs"):
    print(row)

for row in cursor.execute("SELECT * FROM words"):
    print(row)


connection.commit()
connection.close()
