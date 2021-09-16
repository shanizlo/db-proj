import sqlite3

from source import TxtParser
from source.entities import *

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

sql_file = open("init_script.sql")
sql_as_string = sql_file.read()
cursor.executescript(sql_as_string)


def insert_into_database(author, title, album, copyright, lyrics):
    the_song = Song(author, title, album, copyright)  # making the song for inserting
    # If there was an error inserting the song - don't continue
    try:
        song_id = insert_song(the_song)  # inserting the song and getting its id for the contains
        the_words_with_context = TxtParser.parse(lyrics)  # the parsed lyrics with all their information

        for wc in the_words_with_context:
            insert_word(Word(wc[0]))
            word_id = get_id_from_word(wc[0])
            insert_contains(word_id, song_id, wc[1], wc[2], wc[3])

    except sqlite3.Error as err:
        return err


def insert_song(song: Song):
    with connection:
        try:
            cursor.execute("INSERT INTO songs VALUES (:song_id, :author, :title, :album, :copyright) returning song_id;",
                           {'song_id': None, 'author': song.author, 'title': song.title, 'album': song.album,
                            'copyright': song.copyright})
            # returning id of the last insert
            return cursor.fetchone()[0]
        except sqlite3.Error as err:
            print("Error occured: ", err)
            return 0


def insert_word(word: Word):
    with connection:
        cursor.execute("INSERT OR IGNORE INTO words VALUES (:word_id, :word_value, :word_length) returning word_id;",
                       {'word_id': None, 'word_value': word.value, 'word_length': word.length})
        inserted_word_id = cursor.fetchone()
        # This is needed in case word ignored and there no word_id created
        if inserted_word_id is not None:
            return inserted_word_id[0]
        else:
            return None


def get_id_from_word(word_str: str):
    with connection:
        # cursor.execute("SELECT word_id FROM words WHERE word_value = %s",
        cursor.execute("SELECT word_id FROM words WHERE word_value = (:word_str)",
                       {'word_str': word_str})
        return cursor.fetchone()[0]


def insert_contains(word_id, song_id, verse_num, sentence_num, word_position):
    with connection:
        cursor.execute("INSERT INTO contains VALUES(:word_id, :song_id, :verse_num, :sentence_num, :word_position)",
                       {'word_id': word_id, 'song_id': song_id, 'verse_num': verse_num, 'sentence_num': sentence_num,
                        'word_position': word_position})


def create_group(group_name):
    with connection:
        cursor.execute("INSERT INTO groups VALUES (:group_id, :group_name) returning group_id;",
                       {'group_id': None, 'group_name': group_name.group_name})
        return cursor.fetchone()[0]

# TODO: add words to group - find group by id and add words
#
#  TODO: add create phrase

# TODO: add words to phrase



###### Tests ######## Tests ######### Tests ######### Tests ############ Tests ###############
copyright_test = "copyright There are plenty of tutorials on the 877834 2948923"
album_test = "Some Album 13"
author_test = "Shani Zlotnik"
title_test = "Title Chuck"
lyrics_test = """There are plenty of tutorials on the internet on using unittest but something I couldn’t find while doing a project was a tutorial on how to mock a database for testing.
I believe a similar method can be used for pytest as well.
When doing continual 
testing as the software is developed or improved upon, testing has to be done to ensure expected functionality.
There may be methods or functions that can alter the data in the database. 
When testing these functions, it’s best to use a separate database. 
It’s most definitely not recommended to use the production database while testing.
When testing is automated it’s not possible to manually change the database 
that each function is using. So, it’s necessary to patch in the test database to the production database. 
For that, we use the patch function available in the mock package. This is available in the Python standard library, available as unittest.mock, but for this tutorial, we’ll be using the mock package."""

word1 = Word("hello")
group1 = Group("chuck")
insert_into_database(author_test, title_test, album_test, copyright_test, lyrics_test)
insert_into_database(author_test, title_test, album_test, copyright_test, lyrics_test)
song1 = Song(author_test, title_test, album_test, copyright_test)

# song1Id = insert_song(song1)
# print("song_id: ", song1Id)
print("printing song")
for row in cursor.execute("SELECT * FROM songs"):
    print(row)

# word1_id = insert_word(word1)
# print("inserted word, the id: ", word1_id)

# id1 = get_id_from_word("hello")
# insert_contains(1, 1, 1, 1, 1)
# create_group(group1)

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
