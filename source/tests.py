import unittest
from sqlite3 import IntegrityError

from source.entities import *
from source.database import *

#  Name of the test should be test_<name of function which is being tested>
# Make sure to check all the functionality

class DataBaseFunctionsTests(unittest.TestCase):
    def test_insert_into_database(self):
        #  Prepare
        copyright_test = "copyright There are plenty of tutorials on the 877834 2948923"
        album_test = "Some Album 13"
        author_test = "Shani Zlotnik"
        title_test = "Title Chuck"
        first_word = "there"
        second_word = "are"
        third_word = "plenty"
        lyrics_test = """
        There are plenty of tutorials on the inte
        
        find while doing a project was a tuto
        When doing continual 
        
        There may be methods or functions that can alter the data in the database. 
        
        When testing is automated it’s not possible 
        to manually change the database 
        """

        # Check adding new song that doesn't exist
        # Execute
        result = insert_into_database(author_test, title_test, album_test, copyright_test, lyrics_test)
        expected_song_entries_result = (1, 'Shani Zlotnik', 'Title Chuck', 'Some Album 13', 'copyright There are plenty of tutorials on the 877834 2948923')

        #  Assert
        # Check that add to database returned song_id which is not 0
        self.assertIsInstance(result, int)
        self.assertNotEqual(result, 0)

        # Check entries
        # Check that song is added to the DB songs
        song_entry = cursor.execute("SELECT * FROM songs WHERE song_id = (:result)",
                       {'result': result}).fetchone()
        self.assertEqual(song_entry, expected_song_entries_result)

        # Check that first three words are existing in words DB
        first_word_found = cursor.execute("SELECT * FROM words WHERE word_value = (:word1)",
                       {'word1': first_word}).fetchone()
        self.assertEqual(first_word_found[1], first_word)

        second_word_found = cursor.execute("SELECT * FROM words WHERE word_value = (:word2)",
                                          {'word2': second_word}).fetchone()
        self.assertEqual(second_word_found[1], second_word)

        third_word_found = cursor.execute("SELECT * FROM words WHERE word_value = (:word3)",
                       {'word3': third_word}).fetchone()
        self.assertEqual(third_word_found[1], third_word)

        # Check that adding again song with same title and author will not add it to db - check that returns error
        result2 = insert_into_database(author_test, title_test, album_test, copyright_test, lyrics_test)
        self.assertEqual(str(result2), 'UNIQUE constraint failed: songs.title, songs.author')

        # Check that added new entry with song_id and word_id in table contains: search by word_id and validate this entry has song_id
        result3 = cursor.execute("SELECT * FROM contains WHERE word_id = (:word2_id)",
                       {'word2_id': second_word_found[0]}).fetchone()
        expected_result = (second_word_found[0], song_entry[0], 1, 1, 2)
        self.assertEqual(result3, expected_result)

        # Check that can add another song with same author but different title
        result4 = insert_into_database('Another author', title_test, album_test, copyright_test, lyrics_test)
        # Check that added to database and returned song_id which is not 0
        self.assertIsInstance(result, int)
        self.assertNotEqual(result, 0)

    def test_insert_word(self):
        #  Prepare
        word1 = Word("hello")

        # Execute
        result = insert_word(word1)
        result2 = insert_word(word1)
        # This test will fail when running separately because word_id would be 1
        # In this case uncomment next line
        # expected_word_entry = (1, 'hello', 5)
        expected_word_entry = (92, 'hello', 5)

        # Assert
        # Check that add to database returned word_id which is not None
        self.assertIsInstance(result, int)
        #  Check that adding same word will not add it to db - returned None
        self.assertEqual(result2, None)

        # Check that word is added to the DB
        word_entry = cursor.execute("SELECT * FROM words WHERE word_id = (:result)",
                                      {'result': result}).fetchone()
        self.assertEqual(word_entry, expected_word_entry)

    def test_insert_song(self):
        # Prepare
        copyright_test = "copyright There are plenty of tutorials on the 877834 2948923"
        album_test = "Some Album 13"
        author_test = "Shani Zlotnik"
        title_test = "Other Title Chuck"
        song1 = Song(author_test, title_test, album_test, copyright_test)

        # Execute
        song_id = insert_song(song1)

        # Assert
        # Check that add to database returned song_id which is not 0
        self.assertIsInstance(song_id, int)
        self.assertNotEqual(song_id, 0)

    def test_get_id_from_word(self):
        # Prepare
        word1 = Word('plenty')
        word2 = "wordNotInDatabase"

        # Execute
        inserted_id = insert_word(word1)
        result = get_id_from_word('plenty')
        result2 = get_id_from_word(word2)


        # Assert
        self.assertEqual(result, inserted_id)

        # Check that searching for non-existing word returns None
        self.assertEqual(result2, None)

    def test_create_group(self):
        # Prepare
        group1 = Group("chuck")

        # Execute
        result = create_group(group1)

        # Assert
        self.assertEqual(result, 1)

        # Check that adding again song with same title and author will not add it to db - check that returns error
        result2 = create_group(group1)
        self.assertEqual(str(result2), 'UNIQUE constraint failed: groups.group_name')

        # Check the entry in db
        result3 = cursor.execute("SELECT * FROM groups WHERE group_id = (:group_id)",
                                 {'group_id': result}).fetchone()
        expected_result = (result, 'chuck')
        self.assertEqual(result3, expected_result)

    # This test doesn't work
    # def test_search_song_id(self):
    #     # Prepare
    #     copyright_test = ""
    #     album_test = "Album 13"
    #     author_test = "Zlotnik"
    #     title_test = "Chuck"
    #     song_search_test = Song(author_test, title_test, album_test, copyright_test)
    #
    #     # Execute
    #     song_id = insert_song(song_search_test)
    #     all_songs = getAllSongEntries()
    #
    #     # Execute
    #     result = search_song_id(author_test, title_test)
    #
    #     # Assert
    #     self.assertEqual(result, song_id)
    #     self.assertNotEqual(result, None)

    def test_search_words_ids_song_contains(self):
        #  Prepare
        copyright_test = "2948923"
        album_test = "Some Album 13"
        author_test = "Shani Zlotnik"
        title_test = "Title Chuck"
        lyrics_test = """
                There are plenty of tutorials on the inte

                find while doing a project was a tuto
                When doing continual 

                There may be methods or functions that can alter the data in the database. 

                When testing is automated it’s not possible 
                to manually change the database 
                """
        song_id = insert_into_database(author_test, title_test, album_test, copyright_test, lyrics_test)

        # Execute
        words_in_song = search_words_ids_song_contains(song_id)
        all_songs = getAllSongEntries()

        # Validate that 45 entries found
        # Assert
        self.assertNotEqual(len(words_in_song), 0)
        self.assertEqual(len(words_in_song), 45)

        # Test "search_word_by_id" #
        #  Execute
        word_val = search_word_by_id(30)

        # Assert
        self.assertEqual(word_val, "data")

        # Test "search_word_id_by_position" #
        # Execute
        word_id_found = search_word_id_by_position(1, 2, 2, 3)

        # Assert
        self.assertEqual(word_id_found, 19)