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
        lyrics_test = """There are plenty of tutorials on the internet on using unittest but something I couldn’t 
        
        find while doing a project was a tutorial on how to mock a database for testing.
        I believe a similar method can be used for pytest as well.
        When doing continual 
        testing as the software is developed or improved upon, testing has to be done to ensure expected functionality.
        
        There may be methods or functions that can alter the data in the database. 
        When testing these functions, it’s best to use a separate database. 
        It’s most definitely not recommended to use the production database while testing.
        
        When testing is automated it’s not possible to manually change the database 
        that each function is using. So, it’s necessary to patch in the test database to the production database. 
        For that, we use the patch function available in the mock package. This is available in the Python standard"""

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
        expected_word_entry = (1, 'hello', 5)
        # expected_word_entry = (302, 'hello', 5)

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

    # TODO: fix this test
    def test_search_song_id(self):
        # Prepare
        copyright_test = "copyright There are plenty of tutorials on the 877834 2948923"
        album_test = "Some Album 13"
        author_test = "Shani Zlotnik"
        title_test = "Other Title Chuck"
        song1 = Song(author_test, title_test, album_test, copyright_test)

        # Execute
        song_id = insert_song(song1)
        all_songs = getAllSongEntries()

        # Execute
        result = search_song_id(author_test, title_test)

        # Assert
        self.assertEqual(result, song_id)
        self.assertNotEqual(result, None)