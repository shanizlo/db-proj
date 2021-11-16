import sqlite3

from text_parser import parse
from entities import *

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
        the_words_with_context = parse(lyrics)  # the parsed lyrics with all their information

        for wc in the_words_with_context:
            insert_word(Word(wc[0]))
            word_id = get_id_from_word(wc[0])
            insert_contains(word_id, song_id, wc[1], wc[2], wc[3])

        return song_id

    except sqlite3.Error as err:
        return err


def insert_song(song: Song):
    with connection:
        cursor.execute("INSERT INTO songs VALUES (:song_id, :author, :title, :album, :copyright) returning song_id;",
                       {'song_id': None, 'author': song.author, 'title': song.title, 'album': song.album,
                        'copyright': song.copyright})
        inserted_song_id = cursor.fetchone()
        # This is needed in case word ignored and there no word_id created
        if inserted_song_id is not None:
            return inserted_song_id[0]
        else:
            return None


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
    word_str = word_str.lower()
    with connection:
        cursor.execute("SELECT word_id FROM words WHERE word_value = (:word_str)",
                       {'word_str': word_str})
        found_word_id = cursor.fetchone()
        #  This is needed in case word not found
        if found_word_id is not None:
            return found_word_id[0]
        else:
            return None


def insert_contains(word_id, song_id, verse_num, sentence_num, word_position):
    with connection:
        cursor.execute("INSERT INTO contains VALUES(:word_id, :song_id, :verse_num, :sentence_num, :word_position)",
                       {'word_id': word_id, 'song_id': song_id, 'verse_num': verse_num, 'sentence_num': sentence_num,
                        'word_position': word_position})


def create_group(group_name):
    try:
        with connection:
            cursor.execute("INSERT INTO groups VALUES (:group_id, :group_name) returning group_id;",
                           {'group_id': None, 'group_name': group_name.group_name})
            # In case group with this name already exists
            return cursor.fetchone()[0]

    except sqlite3.Error as err:
        return err

def search_song_id(author: str, title: str):
    with connection:
        cursor.execute("SELECT song_id FROM songs WHERE title = :song_title AND author = :song_author;",
                       {'song_title': title, 'song_author': author})
        found_song_id = cursor.fetchone()
        if found_song_id is not None:
            return found_song_id[0]
        else:
            return None

def search_words_ids_song_contains(song_id: str):
    with connection:
        cursor.execute("SELECT * FROM contains WHERE song_id = :song_id;",
                       {'song_id': song_id})
        found_words_ids = cursor.fetchall()
        return found_words_ids

def search_words_in_verse(song_id: str, verse_num: int):
    with connection:
        cursor.execute("SELECT * FROM contains WHERE song_id = :song_id AND verse_num = :verse_num",
                       {'song_id': song_id, 'verse_num': verse_num})
        return cursor.fetchall()
# Finds word value
def search_word_by_id(word_id: str):
    with connection:
        cursor.execute("SELECT word_value FROM words WHERE words.word_id = :word_id;",
                       {'word_id': word_id})
        word_found = cursor.fetchone()
        if word_found is not None:
            return word_found[0]
        else:
            return None

def search_word_id_by_position(songId: str, verseNum: int, sentenceNum: int, wordPos: int):
    with connection:
        cursor.execute("SELECT word_id FROM contains WHERE song_id = :song_id AND verse_num = :verse_num AND sentence_num = :sentence_num AND word_position = :word_pos;",
                       {'song_id': songId, 'verse_num': verseNum, 'sentence_num': sentenceNum, 'word_pos': wordPos})
        word_id_found = cursor.fetchone()
        if word_id_found is not None:
            return word_id_found[0]
        else:
            return None

def get_word_position(song_id: str, word_id: str):
    with connection:
        cursor.execute("SELECT verse_num, sentence_num FROM contains WHERE song_id = :song_id AND word_id = :word_id;",
                       {'song_id': song_id, 'word_id': word_id})
        word_pos_found = cursor.fetchone()
        if word_pos_found is not None:
            return word_pos_found[0]
        else:
            return None

def get_words_in_line(song_id: str, verse: int, line: int):
    with connection:
        cursor.execute("SELECT word_id FROM contains WHERE song_id = :song_id AND verse_num = :verse_num AND sentence_num = :sen_num ORDER BY word_position ASC;",
                       {'song_id': song_id, 'verse_num': verse, 'sen_num': line})
        return cursor.fetchall()

def get_word_length(word_id: int):
    with connection:
        cursor.execute("SELECT word_length FROM words WHERE word_id = :word_id", {'word_id': word_id})
        return cursor.fetchone()[0]
# Function for debugging, nor for functionality
def getAllSongEntries():
    with connection:
        cursor.execute("SELECT * FROM songs;")
        return cursor.fetchall()

# Function for debugging, nor for functionality
def getAllWordPositionsInSongId():
    with connection:
        cursor.execute("SELECT * FROM contains WHERE song_id = 1;")
        return cursor.fetchall()

# Function for debugging, nor for functionality
def getfVersesNumsInSong():
    with connection:
        cursor.execute("SELECT verse_num FROM contains WHERE song_id = 1 ORDER BY verse_num DESC;")
        return cursor.fetchall()

def search_song_id(author: str, title: str):
    with connection:
        cursor.execute("SELECT song_id FROM songs WHERE title = :song_title AND author = :song_author;",
                       {'song_title': title, 'song_author': author})
        found_song_id = cursor.fetchone()
        if found_song_id is not None:
            return found_song_id[0]
        else:
            return None

def search_words_ids_song_contains(song_id: str):
    with connection:
        cursor.execute("SELECT * FROM contains WHERE song_id = :song_id;",
                       {'song_id': song_id})
        found_words_ids = cursor.fetchall()
        return found_words_ids

# Finds word value
def search_word_by_id(word_id: str):
    with connection:
        cursor.execute("SELECT word_value FROM words WHERE words.word_id = :word_id;",
                       {'word_id': word_id})
        word_found = cursor.fetchone()
        if word_found is not None:
            return word_found[0]
        else:
            return None

def search_word_id_by_position(songId: str, verseNum: int, sentenceNum: int, wordPos: int):
    with connection:
        cursor.execute("SELECT word_id FROM contains WHERE song_id = :song_id AND verse_num = :verse_num AND sentence_num = :sentence_num AND word_position = :word_pos;",
                       {'song_id': songId, 'verse_num': verseNum, 'sentence_num': sentenceNum, 'word_pos': wordPos})
        word_id_found = cursor.fetchone()
        if word_id_found is not None:
            return word_id_found[0]
        else:
            return None

def get_word_position(song_id: str, word_id: str):
    with connection:
        cursor.execute("SELECT verse_num, sentence_num FROM contains WHERE song_id = :song_id AND word_id = :word_id;",
                       {'song_id': song_id, 'word_id': word_id})
        word_pos_found = cursor.fetchone()
        if word_pos_found is not None:
            return word_pos_found[0]
        else:
            return None

def get_words_in_line(song_id: str, verse: int, line: int):
    with connection:
        cursor.execute("SELECT word_id FROM contains WHERE song_id = :song_id AND verse_num = :verse_num AND sentence_num = :sen_num ORDER BY word_position ASC;",
                       {'song_id': song_id, 'verse_num': verse, 'sen_num': line})
        return cursor.fetchall()

# Function for debugging, nor for functionality
def getAllSongEntries():
    with connection:
        cursor.execute("SELECT * FROM songs;")
        return cursor.fetchall()

# Function for debugging, nor for functionality
def getAllWordPositionsInSongId():
    with connection:
        cursor.execute("SELECT * FROM contains WHERE song_id = 1;")
        return cursor.fetchall()

# Function for debugging, nor for functionality
def getfVersesNumsInSong():
    with connection:
        cursor.execute("SELECT verse_num FROM contains WHERE song_id = 1 ORDER BY verse_num DESC;")
        return cursor.fetchall()

# TODO: add words to group - find group by id and add words
#  TODO: add create phrase

# TODO: add words to phrase



connection.commit()
# connection.close()
