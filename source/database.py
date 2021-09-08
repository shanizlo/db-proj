import sqlite3

from source import TxtParser
from source.entities import *

# _conn = sqlite3.Connection
# _cursor = sqlite3.Cursor
connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

sql_file = open("init_script.sql")
sql_as_string = sql_file.read()
cursor.executescript(sql_as_string)


def insert_into_database(author, title, album, copyright, lyrics):
    the_song = Song(author, title, album, copyright)  # making the song for inserting
    song_id = insert_song(the_song)  # inserting the song and getting its id for the contains
    the_words_with_context = TxtParser.parse(lyrics)  # the parsed lyrics with all their information

    for wc in the_words_with_context:
        insert_word(Word(wc[0]))
        word_id = get_id_from_word(wc[0])
        insert_contains(word_id, song_id, wc[1], wc[2], wc[3])


def insert_song(song):
    with connection:
        cursor.execute("INSERT INTO songs VALUES (:song_id, :author, :title, :album, :copyright)",
                       {'song_id': None, 'author': song.author, 'title': song.title, 'album': song.album,
                        'copyright': song.copyright})
        cursor.execute("SELECT  last_insert_rowid();")
        return cursor.fetchall()[0][0]


def insert_word(word):
    with connection:
        cursor.execute("INSERT OR IGNORE INTO words VALUES (:word_id, :word_value, :word_length)",
                       {'word_id': None, 'word_value': word.value, 'word_length': word.length})


def get_id_from_word(str):
    with connection:
        cursor.execute("SELECT word_id FROM words WHERE word_value = \"" + str + "\"")
        id = cursor.fetchone()
        # id = cursor.fetchall()
        # return id[0][0]
        return id[0]


def insert_contains(word_id, song_id, verse_num, sentence_num, word_position):
    with connection:
        cursor.execute("INSERT INTO contains VALUES(:word_id, :song_id, :verse_num, :sentence_num, :word_position)",
                       {'word_id': word_id, 'song_id': song_id, 'verse_num': verse_num, 'sentence_num': sentence_num,
                        'word_position': word_position})


def create_group(group_name):
    with connection:
        cursor.execute("INSERT INTO groups VALUES (:group_id, :group_name)",
                       {'group_id': None, 'group_name': group_name.group_name})

# TODO: add words to group - find group by id and add words
#
#  TODO: add create phrase

# TODO: add words to phrase



###### Tests ######## Tests ######### Tests ######### Tests ############ Tests ###############
word1 = Word("hello")
group1 = Group("chuck")
insert_word(word1)
insert_contains(1, 1, 1, 1, 1)
create_group(group1)
insert_into_database("chuck", "title", "alb", "cpergjj5", "hello import sqlite3  \n hjgsdf")

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
# connection.close()
