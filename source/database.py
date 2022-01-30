import sqlite3

from text_parser import parse
from entities import *

"""
    This file connects to the database file and contains methods which are all one-line SQL queries, for use in
    the helpers_db.py file or for debugging.
"""

"""
    The following, non-method lines define the SQL program that will run on initiation of the code and connects 
    to the database
"""
# connection = sqlite3.connect(":memory:")
connection = sqlite3.connect("songs.db")
cursor = connection.cursor()

sql_file = open("init_script.sql")
sql_as_string = sql_file.read()
cursor.executescript(sql_as_string)


def insert_into_database(author, title, album, copyright, lyrics):
    """
    Inserts the given song into the database, according to the database schemes and tables, with all of it's parameters.

    Parameters
    -----------
    author: str
    title: str
    album: str
    copyright: str
    lyrics: str

    Returns
    -----------
    int
        The id of the song if it is added. Otherwise returns an sqlite3.Error if a song with this name and author
        already exists in the database, causing failure of the constraints on the songs table.
    """
    the_song = Song(author.lower(), title.lower(), album.lower(), copyright.lower())  # making the song for inserting
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
    """
        Inserts a new entry into the table defining this new song

        Parameters
        -----------
        song: Song
            An object of describing the song to be added into the database.

        Returns
        -----------
        int
            Returns the id of the song newly inserted into the table.
        None
            If such a song already existed.
        """
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
    """
        Inserts a word into the word table.

        Parameters
        -----------
        word: Word
            The word to add to the table

        Returns
        -----------
        int
            The id in the table of the newly inserted word.
        None
            If such a word already existed in the database.
        """
    with connection:
        cursor.execute("INSERT OR IGNORE INTO words VALUES (:word_id, :word_value, :word_length) returning word_id;",
                       {'word_id': None, 'word_value': word.value.lower(), 'word_length': word.length})
        inserted_word_id = cursor.fetchone()
        # This is needed in case word ignored and there no word_id created
        if inserted_word_id is not None:
            return inserted_word_id[0]
        else:
            return None


def get_id_from_word(word_str: str):
    """
        This method returns the table id of a word inserted into the database.

        Parameters
        -----------
        word_str: str
            The word to add to the table.

        Returns
        -----------
        int
            The id in the table of the newly inserted word.
        None
            If the given word doesn't exist in the table.
    """
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
    """
        Inserts a word into the its position in a given song, according to the database scheme.

        Parameters
        -----------
        word_id: int
        song_id: int
        verse_num: int
        sentence_num: int
        word_position: int
    """
    with connection:
        cursor.execute("INSERT INTO contains VALUES(:word_id, :song_id, :verse_num, :sentence_num, :word_position)",
                       {'word_id': word_id, 'song_id': song_id, 'verse_num': verse_num, 'sentence_num': sentence_num,
                        'word_position': word_position})


def search_song_id(author: str, title: str):
    """
        As we assume every song is uniquely identified by its author and title, this method returns the id of a song
        (if it exists in the table), according to its author and title.

        Parameters
        -----------
        author: str
        title: str

        Returns
        -----------
        int
            The id in the table of the song searched.
        None
            If such a song doesn't exist in the database.
    """
    with connection:
        cursor.execute("SELECT song_id FROM songs WHERE title = :song_title AND author = :song_author;",
                       {'song_title': title, 'song_author': author})
        found_song_id = cursor.fetchone()
        if found_song_id is not None:
            return found_song_id[0]
        else:
            return None

def search_words_ids_song_contains(song_id: int):
    """
        This method returns all information the database has in regards to the words in a given song.

        Parameters
        -----------
            song_id: int
                The song of which this function finds the words and their position.

        Returns
        -----------
            tuple
                Tuple of lists, each of the form [word_id, song_id, verse_num, sentence_num, word_position]
            None
                If no song with this song_id exists in the table.
    """
    with connection:
        cursor.execute("SELECT * FROM contains WHERE song_id = :song_id;",
                       {'song_id': song_id})
        found_words_ids = cursor.fetchall()
        return found_words_ids

def search_words_in_verse(song_id: int, verse_num: int):
    """
            This method returns all information regarding the words in a specified verse and its specified song.

            Parameters
            -----------
                song_id: int
                    The song of which this function finds the words and their position.
                verse_num: int
            Returns
            -----------
                tuple
                    Tuple of lists, each of the form [word_id, song_id, verse_num, sentence_num, word_position]
                    By specification, the verse_num of all these lists will be constant.
                None
                    If no song with this song_id exists in the table or no verse of this number in the song.
        """
    with connection:
        cursor.execute("SELECT * FROM contains WHERE song_id = :song_id AND verse_num = :verse_num",
                       {'song_id': song_id, 'verse_num': verse_num})
        return cursor.fetchall()


def search_word_by_id(word_id: int):
    """
            This method returns the word specified by some word_id

            Parameters
            -----------
                word_id: int
                    The song of which this function finds the words and their position.

            Returns
            -----------
                str
                    The value of the word searched in the db.
                None
                    If no word with this word_id exists in the db.
        """
    with connection:
        cursor.execute("SELECT word_value FROM words WHERE words.word_id = :word_id;",
                       {'word_id': word_id})
        word_found = cursor.fetchone()
        if word_found is not None:
            return word_found[0]
        else:
            return None


def search_word_id_by_position(songId: int, verseNum: int, sentenceNum: int, wordPos: int):
    """
            This method returns the word_id of a word by its position in some song.

            Parameters
            -----------
                songId: int
                verseNum: int
                sentenceNum: int
                wordPos: int
                    The position of the word to find in the sentence.
            Returns
            -----------
                int
                    The id of the word in some given position.
                None
                    If no position, as specified in the input exists in the database.
        """
    with connection:
        cursor.execute("SELECT word_id FROM contains WHERE song_id = :song_id AND verse_num = :verse_num AND sentence_num = :sentence_num AND word_position = :word_pos;",
                       {'song_id': songId, 'verse_num': verseNum, 'sentence_num': sentenceNum, 'word_pos': wordPos})
        word_id_found = cursor.fetchone()
        if word_id_found is not None:
            return word_id_found[0]
        else:
            return None


def get_word_positions(song_id: int, word_id: int):
    """
            This method returns all positions of a given word, specified by its id.

            Parameters
            -----------
                song_id: int
                    The id song of the song of which this function finds the words and their position.
                word_id: int
                    The id of the word to find in the given song.
            Returns
            -----------
                list
                    List of lists, each of the form [verse_num, sentence_num, word_position]
                None
                    If the input was bad - no song as given exists or no word as specified exists anywhere in the song.
        """
    with connection:
        cursor.execute("SELECT verse_num, sentence_num, word_position FROM contains WHERE song_id = :song_id AND word_id = :word_id;",
                       {'song_id': song_id, 'word_id': word_id})
        word_pos_found = cursor.fetchall()
        if word_pos_found is not None:
            return list(word_pos_found)
        else:
            return None

def get_all_songs_in_db():
    """
            Returns all the ids of all songs in the database.

            Returns
            -----------
                tuple
                    Tuple of lists, each of the form [song_id].
                None
                    If no song exists in the table.
        """
    with connection:
        cursor.execute("SELECT song_id FROM songs")
        return cursor.fetchall()

def get_words_in_line(song_id: int, verse: int, line: int):
    """
            This method returns all word_ids in a given sentence of a given song

            Parameters
            -----------
                song_id: int
                    The song of which this function finds the words in the specified positions.
                verse: int
                line: int

            Returns
            -----------
                tuple
                    Tuple of lists, each of the form [word_id]
                None
        """
    with connection:
        cursor.execute("SELECT word_id FROM contains WHERE song_id = :song_id AND verse_num = :verse_num AND sentence_num = :sen_num ORDER BY word_position ASC;",
                       {'song_id': song_id, 'verse_num': verse, 'sen_num': line})
        return cursor.fetchall()


def get_word_length(word_id: int):
    """
            This method returns the length of a given word specified by its id.
            This might raise an error if there doesn't exist a word with the given word_id.

            Parameters
            -----------
                word_id: int

            Returns
            -----------
                int
                    The length of the word

        """
    with connection:
        cursor.execute("SELECT word_length FROM words WHERE word_id = :word_id", {'word_id': word_id})
        return cursor.fetchone()[0]


# Function for debugging, not for functionality
def getAllSongEntries():
    with connection:
        cursor.execute("SELECT * FROM songs;")
        return cursor.fetchall()


def getAllWordPositionsInSong(song_id: int):
    """
            This method returns all words and their positions in a given song.

            Parameters
            -----------
                song_id: int
                    The song of which this function finds the words and their positions.

            Returns
            -----------
                tuple
                    Tuple of lists, each of the form [verse_num, sentence_num, word_position, word_id]
                None
                    If no song with this song_id exists in the table.
        """
    with connection:
        cursor.execute("SELECT verse_num, sentence_num, word_position, word_id FROM contains WHERE song_id = :song_id;", {'song_id': song_id})
        return cursor.fetchall()


# Function for debugging, not for functionality
def getfVersesNumsInSong():
    with connection:
        cursor.execute("SELECT verse_num FROM contains WHERE song_id = 1 ORDER BY verse_num DESC;")
        return cursor.fetchall()


def search_song_id(author: str, title: str):
    """
            This method returns the id of a song specified by its author and title.

            Parameters
            -----------
                author: str
                title: str

            Returns
            -----------
                int
                    The id of the song searched.
                None
                    If no song with this author and title is found in the database.
        """
    with connection:
        cursor.execute("SELECT song_id FROM songs WHERE title = :song_title AND author = :song_author;",
                       {'song_title': title.lower(), 'song_author': author.lower()})
        found_song_id = cursor.fetchone()
        if found_song_id is not None:
            return found_song_id[0]
        else:
            return None


def search_words_ids_song_contains(song_id: str):
    """
            This method returns all information the database has in regards to the words in a given song.

            Parameters
            -----------
                song_id: int
                    The song of which this function finds the words and their position.

            Returns
            -----------
                tuple
                    Tuple of lists, each of the form [word_id, song_id, verse_num, sentence_num, word_position]
                None
                    If no song with this song_id exists in the table.
        """
    with connection:
        cursor.execute("SELECT * FROM contains WHERE song_id = :song_id;",
                       {'song_id': song_id})
        found_words_ids = cursor.fetchall()
        return found_words_ids


# Finds word value
def search_word_by_id(word_id: str):
    """
                This method returns the word specified by some word_id

                Parameters
                -----------
                    word_id: int
                        The song of which this function finds the words and their position.

                Returns
                -----------
                    str
                        The value of the word searched in the db.
                    None
                        If no word with this word_id exists in the db.
            """
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


def get_song_definition_from_id(song_id: str):
    """
               This method returns the title and author of a song from the given id.

               Parameters
               -----------
                   song_id: int

               Returns
               -----------
                   tuple
                       Tuple of the form (title, author)
                   None
                       If no song with this song_id exists in the table.
           """
    with connection:
        cursor.execute("SELECT title, author FROM songs WHERE song_id = :song_id", {'song_id': song_id})
        return cursor.fetchone()


def get_words_in_line(song_id: str, verse: int, line: int):
    """
                This method returns all word_ids in a given sentence of a given song

                Parameters
                -----------
                    song_id: int
                        The song of which this function finds the words in the specified positions.
                    verse: int
                    line: int

                Returns
                -----------
                    tuple
                        Tuple of lists, each of the form [word_id]
                    None
            """
    with connection:
        cursor.execute("SELECT word_id FROM contains WHERE song_id = :song_id AND verse_num = :verse_num AND sentence_num = :sen_num ORDER BY word_position ASC;",
                       {'song_id': song_id, 'verse_num': verse, 'sen_num': line})
        return cursor.fetchall()


def create_group(group_name):
    """
                This method creates a new group in the group table with the given group name.

                Parameters
                -----------
                    group_name: str

                Returns
                -----------
                    int
                        The id of the group if it was already created.
                    None
                        If a group fo this name existed in the database already
            """
    try:
        with connection:
            cursor.execute("INSERT INTO groups VALUES (:group_id, :group_name) returning group_id;",
                           {'group_id': None, 'group_name': group_name})
            # In case group with this name already exists
            return cursor.fetchone()[0]

    except sqlite3.Error as err:
        return err


def is_word_in_group(groupId: int, wordId: int):
    """
                This method returns if the given word is in a given group

                Parameters
                -----------
                    groupId: int
                        The id of the group to check if the existence of a given word.
                    wordId: int
                        The id of the word to check if it is in the group.
                Returns
                -----------
                    True
                        Given word is in the group.
                    False
                        Given word is not in the group.
    """
    with connection:
        cursor.execute("SELECT group_id FROM wordsInGroup WHERE group_id = :groupId AND word_id = :wordId",
                       {'groupId': groupId, 'wordId': wordId})
        return cursor.fetchone() is not None


def add_word_to_group(groupId: int, wordId: int):
    """
                    This method adds a word into a given group by the scheme of this database.

                    Parameters
                    -----------
                        groupId: int
                            The id of the group to add the word to.
                        wordId: int
                            The id of the word to add to the group.
    """
    with connection:
        cursor.execute("INSERT INTO wordsInGroup VALUES (:groupId, :wordId)", {'groupId': groupId, 'wordId': wordId})


def find_group_id_by_name(name: str):
    """
                    This method finds a given group's id by its name input.

                    Parameters
                    -----------
                        name: str
                            The name of the group to get it's id from.

                    Returns
                    -----------
                        int
                            The id of the group with the inputted name
                        None
                            Group with the given name doesn't exist.
        """
    with connection:
        cursor.execute("SELECT group_id FROM groups WHERE group_name = :name", {'name': name})
        id = cursor.fetchone()
        if id is None:
            return None
        else:
            return id[0]


def all_words_in_group(groupId: int):
    """
                    This method returns all the words in a given group

                    Parameters
                    -----------
                        groupId: int
                            The id of the group to get all its words.

                    Returns
                    -----------
                        tuple
                            Tuple of lists each of the form [word_id]
                        None
                            Group either doesn't exist or there don't exist any words in the given group.
        """
    with connection:
        cursor.execute("SELECT word_id FROM wordsInGroup WHERE group_id = :groupId", {'groupId': groupId})
        return cursor.fetchall()


def create_phrase(phrase: str, no_words: int):
    """
                    This method creates a phrase according to its definition in the database scheme.

                    Parameters
                    -----------
                        phrase: str
                            The phrase to be added to the database.
                        no_words: int
                            The number of words of the inputted phrase
        """
    with connection:
        cursor.execute("INSERT OR IGNORE INTO phrases VALUES (:phrase_id, :phrase_text, :words_count)",
                       {'phrase_id': None, 'phrase_text': phrase, 'words_count': no_words})


def max_verse(song_id: int):
    """
                    This method returns the number of verses in a given song.
                    May raise an error if the song doesn't exist in the database.

                    Parameters
                    -----------
                        song_id: int
                            The id of the song to get output from.

                    Returns
                    -----------
                        int
                            The number of verses in a given song.
        """
    with connection:
        cursor.execute("SELECT MAX(verse_num) FROM contains WHERE song_id = :song_id", {'song_id': song_id})
        return cursor.fetchone()[0]


def max_sentence(song_id: int):
    """
                    This method returns if the maximum amount of sentences in a verse of a given song.
                    May raise an error if a song with this id doesn't exist in the database.

                    Parameters
                    -----------
                        song_id: int
                            The id of the song to get output from.

                    Returns
                    -----------
                        int
                            The maximum amount of sentences in a verse of a given song.
        """
    with connection:
        cursor.execute("SELECT MAX(sentence_num) FROM contains WHERE song_id = :song_id", {'song_id': song_id})
        return cursor.fetchone()[0]


# Function for debugging, nor for functionality
def getAllSongEntries():
    with connection:
        cursor.execute("SELECT * FROM songs;")
        return cursor.fetchall()


# Function for debugging, nor for functionality
def getfVersesNumsInSong():
    with connection:
        cursor.execute("SELECT verse_num FROM contains WHERE song_id = 1 ORDER BY verse_num DESC;")
        return cursor.fetchall()

# Get all words values
def getAllWordsInDBAZ():
    with connection:
        cursor.execute("SELECT word_value from words ORDER BY word_value ASC;")
        return cursor.fetchall()

# Get all words and their count
def getAllWordsInDBCount():
    with connection:
        cursor.execute("SELECT words.word_value, COUNT(c.word_id) AS COUNT FROM words INNER JOIN contains c ON words.word_id = c.word_id GROUP BY words.word_id ORDER BY COUNT DESC ;")
        return cursor.fetchall()

def getTop10Songs():
    with connection:
        cursor.execute("SELECT songs.title, songs.author, COUNT(c.song_id) AS COUNT FROM songs INNER JOIN contains c ON songs.song_id = c.song_id GROUP BY songs.song_id ORDER BY COUNT DESC LIMIT 10;")
        return cursor.fetchall()

def getTop10WordsBySongId(song_id: str):
    with connection:
        cursor.execute("SELECT words.word_value, COUNT(c.word_id) AS COUNT FROM words INNER JOIN contains c ON words.word_id = c.word_id WHERE c.song_id = :song_id GROUP BY words.word_id ORDER BY COUNT DESC LIMIT 10;",
                       {'song_id': song_id})
        return cursor.fetchall()

# Get all songs sorted by title
def getAllSongsInDBByTitle():
    with connection:
        cursor.execute("SELECT title, author from songs ORDER BY title ASC;")
        return cursor.fetchall()

# Get all songs sorted by author
def getAllSongsInDBByAuthor():
    with connection:
        cursor.execute("SELECT author, title from songs ORDER BY author ASC;")
        return cursor.fetchall()

def getAllSongsUnDBByCount():
    with connection:
        cursor.execute("SELECT COUNT(c.song_id) AS COUNT, songs.title, songs.author FROM songs INNER JOIN contains c ON songs.song_id = c.song_id GROUP BY songs.song_id ORDER BY COUNT DESC;")
        return cursor.fetchall()

def getCountOfAllSongs():
    with connection:
        cursor.execute("SELECT COUNT(*) FROM songs;")
        return cursor.fetchone()

def getCountOfAllAuthors():
    with connection:
        cursor.execute("SELECT count(DISTINCT author) FROM songs;")
        return cursor.fetchone()

def getCountOfAllWords():
    with connection:
        cursor.execute("SELECT COUNT(*) FROM words;")
        return cursor.fetchone()

connection.commit()
# connection.close()
