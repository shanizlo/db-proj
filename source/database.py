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

def insert_contains(word_id, song_id, verse_num, sentence_num, word_position):
    with connection:
        cursor.execute("INSERT INTO contains VALUES(:word_id, :song_id, :verse_num, :sentence_num, :word_position)",
                       {'word_id': word_id, 'song_id': song_id, 'verse_num': verse_num, 'sentence_num': sentence_num, 'word_position': word_position})

def create_group(group_name):
    with connection:
        cursor.execute("INSERT INTO groups VALUES (:group_id, :group_name)",
                       {'group_id': None, 'group_name': group_name.group_name})

#  TODO: add words to group - find group by id and add words
#
#  TODO: add create phrase

# TODO: add words to phrase



###### Tests ######## Tests ######### Tests ######### Tests ############ Tests ###############
song1 = Song("Freddie Mercury", "Love of my life" )
word1 = Word("hello")
group1 = Group("chuck")

insert_song(song1)
insert_word(word1)
insert_contains(1, 1, 1, 1,1)
create_group(group1)


print(word1.value)

for row in cursor.execute("SELECT * FROM songs"):
    print(row)

for row in cursor.execute("SELECT * FROM words"):
    print(row)

for row in cursor.execute("SELECT * FROM contains"):
    print(row)

for row in cursor.execute("SELECT * FROM groups"):
    print(row)

connection.commit()
connection.close()
