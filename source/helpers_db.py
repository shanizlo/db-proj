from database import *
from helpers_validators import *
from entities import *

""" 
    This file is the middle ground between the database and our GUI. 
    As the writers, we found that executing SQL queries directly in the ui is tedious and unreadable.
    Furthermore, we do not wish to allow the UI to affect and change the db directly.
    Hence, this file was created. It allows for using the one-line SQL queries in the database.py file, 
    as subroutines for the GUI to use, in a compact and more readable way.
"""

def SearchSongWords(author: str, title: str):
    """
        This method returns the words of a given song in alphabetic order.
        The two parameters are needed to identify precisely the song which one wants the output from.

        Parameters
        -----------
        author: str
            The name of the author of the song.
        title: str
            The name of the song.

        Returns
        -----------

        str
            A string with the words of the song in alphabetical order, with newlines between them.
            If a string without newlines is returned, the input was bad.
    """
    if author == "" or title == "":
        return "Please enter author and title."
    song_id = search_song_id(author, title)
    words_ids = search_words_ids_song_contains(song_id)
    song_words_list = []
    for w in words_ids:
        w_value = search_word_by_id(w[0])
        if (w_value is not None) and (w_value not in song_words_list):
            song_words_list.append(w_value)
    song_words_list.sort()
    song_words_as_text = "\n".join(song_words_list)
    if len(song_words_as_text) == 0:
        song_words_as_text = "Song with this title and author not found."
    return song_words_as_text


def Deparse(author: str, title: str):
    """
        This method returns the lyrics of a given song.
        Because the song text isn't saved outside of the database, querying the database to get the raw song text
        is necessary.
        The two parameters are needed to identify precisely the song which one wants the output from.

        Parameters
        -----------
        author: str
            The name of the author of the song.
        title: str
            The name of the song.

        Returns
        ----------
        None:
            Either the inputted song doesn't exist or the input was bad.
        str:
            The lyrics of the inputted song in correct verse/sentence/position format.

    """
    if author == "" or title == "":
        return None  # either song doesn't exist or bad song input
    song_id = search_song_id(author, title)
    if song_id is None:
        return None
    else:
        words_in_song = [list(x) for x in getAllWordPositionsInSong(song_id)]
        words_in_song.sort()
        lyrics = ""
        curr_verse = 1
        curr_sentence = 1
        for w_info in words_in_song:
            word = search_word_by_id(w_info[-1])
            if w_info[0] == curr_verse + 1:
                curr_verse += 1
                curr_sentence = 1
                lyrics += "\n\n" + word + " "
            elif w_info[1] == curr_sentence + 1:
                curr_sentence += 1
                lyrics += "\n" + word + " "
            else:
                lyrics += word + " "
        return lyrics


def Insert_Word(word: str):
    """
        Inserts a given word into the database.

        Parameters
        -----------
        word: str
            A given word to enter into the database.

        Returns
        -----------
        int:
            Returns the inserted word id.
    """
    return insert_word(Word(word))


def Get_Line(song_id: int, verse: int, line: int):
    """
        Returns a line in a given song by its position with respect to its verse and sentence within the verse position.

        Parameters
        -----------
        song_id: int
            The id of the song from which we wish to receive the line
        verse: int
            The verse number we wish to find.
        line: int
            The sentence number we wish to find.

        Returns
        -----------
        str:
            Returns empty string if a line in a given verse don't exist for the given song.
            Otherwise, returns a string which is the given line.
    """
    words = get_words_in_line(song_id, verse, line)
    s = ""
    for w in words:
        s = s + search_word_by_id(w[0]) + " "
    return s


def SearchSongWordsOrReturnNone(author: str, title: str):
    """
        Finds song and shows its words in alphabetic order as a list, in case of error returns None
        The two parameters are needed to identify precisely the song which one wants the output from.

        Parameters
        -----------
        author: str
            The name of the author of the song.
        title: str
            The name of the song.

        Returns
        -----------
        list:
            Returns a list with the words of the given song in alphabetic order.
        None:
            If an error occurred - either the input is bad or the given song wasn't found.

    """
    if author == "" or title == "":
        return None
    song_id = search_song_id(author, title)
    words_ids = search_words_ids_song_contains(song_id)
    song_words_list = []
    for w in words_ids:
        w_value = search_word_by_id(w[0])
        if (w_value is not None) and (w_value not in song_words_list):
            song_words_list.append(w_value)
    song_words_list.sort()
    if len(song_words_list) == 0:
        return None
    return song_words_list


def SearchWordByPositionInSong(author: str, title: str, verseNum: int, lineNum: int, wordNum: int):
    """
        This method finds the word in a given position of the song (its verse number, sentence number and word number).
        The first two parameters are needed to identify precisely the song which one wants the output from.

        Parameters
        -----------
        author: str
            The name of the author of the song.
        title: str
            The name of the song.
        verseNum: int
            Which verse to find the word in.
        lineNum: int
            Which sentence to find the word in.
        wordNum: int
            Which position within the sentence to find the word in.

        Returns
        -----------
        str:
            If the string is has a whitespace, there occurred some error.
            Otherwise, the returned string is the word one seeks when calling this method.
    """
    validation_error = validate_values_find_word(author, title, verseNum, lineNum, wordNum)
    if validation_error is not None:
        return validation_error
    if author == "" or title == "":
        return "Please enter author and title."
    song_id = search_song_id(author, title)
    if song_id == None:
        return "Song with this title and author not found."
    word_id = search_word_id_by_position(song_id, verseNum, lineNum, wordNum)
    if word_id == None:
        return "Word with this position not found."
    return search_word_by_id(word_id)

# TODO: Add commenting to this method.
def ReturnWordContext(author: str, title: str, word_value):
    # get all wordId where value=value and song_id=song_id
    # TODO: find a way to reuse song_id from a previous search and maybe words as well
    song_id = search_song_id(author, title)
    # get all words from the song
    words_ids = search_words_ids_song_contains(song_id)
    relevant_word_ids = []
    # get all word_ids with relevant values (they all will have same id but different positions)
    for w_id in words_ids:
        w_value = search_word_by_id(w_id[0])
        if (w_value is not None) and (w_value == word_value):
            relevant_word_ids.append(w_id)
    # relevant_word_ids.sort()
    context_list = []
    # find context for each
    for w_id in relevant_word_ids:
        this_w_verse = w_id[2]
        this_w_line = w_id[3]
        this_w_pos = w_id[4]
        # returns id_s of words in this line
        this_w_context = []
        word_ids_in_this_line = get_words_in_line(song_id, this_w_verse, this_w_line)
        for id in word_ids_in_this_line:
            val = search_word_by_id(id[0])
            this_w_context.append(val)
        this_w_context_as_text = " ".join(this_w_context)
        this_w_context_as_text += (' (verse: %s, line: %s)\n' %(this_w_verse, this_w_line))
        context_list.append(this_w_context_as_text)
        print(context_list)
    context_as_text = "\n".join(context_list)
    return context_as_text


def StatisticsOutput(author: str, title: str):
    """
        This method returns what is necessary for the statistics page. It calculates the statistics required from the
        given song.
        The two parameters are needed to identify precisely the song which one wants the output from.

        Parameters
        -----------
        author: str
            The name of the author of the song.
        title: str
            The name of the song.

        Returns
        -----------
        None:
            If the song as it was inputted doesn't exist in the database
        list:
            A list of four elements, of the following form:
            [Number of words in song, Average number of characters per number of sentences, Average number of characters
            per number of verses, the database id of the inputted song].
    """
    song_id = search_song_id(author, title)
    if song_id is not None:
        number_of_words = 0
        number_of_characters = 0
        number_of_verses = 0
        number_of_sentences = 0

        words_in_song = search_words_ids_song_contains(song_id)
        sentences_seen_thus_far = []
        verses_seen_thus_far = []
        for w in words_in_song:
            number_of_words += 1
            number_of_characters += get_word_length(w[0])
            if not w[2] in verses_seen_thus_far:
                number_of_verses += 1
                verses_seen_thus_far.append(w[2])
            if not (w[2], w[3]) in sentences_seen_thus_far:
                number_of_sentences += 1
                sentences_seen_thus_far.append((w[2], w[3]))
        return [number_of_words, int(number_of_characters / number_of_sentences),
                int(number_of_characters / number_of_verses), song_id]

    else:
        return None


def stringOk(s: str):
    """
        Helper function which returns True if the inputted string is not None and is not empty.
    """
    return s is not None and s != ""


def From_UI_Into_Group(name: str, words: list):
    """
        This method either inputs words into a given group, or creates a group with the name and words given.

        Parameters
        -----------
        name: str
            The name of the group to add to or to create.
        words: list
            A list of strings which are the words one wishes to add to the group.

        Returns
        -----------
        True if the group didn't exist already, and this method created a group with the given words.
        False if the group didn't exist and we created a group with this new name.
    """
    group_id = create_group(name)
    group_existed = False
    if not isinstance(group_id, int):  # this means if creating the group failed - meaning the group existed
        group_id = find_group_id_by_name(name)
        group_existed = True
    for w in words:
        w_id = get_id_from_word(w)
        if not is_word_in_group(group_id, w_id):
            add_word_to_group(group_id, w_id)
    return group_existed

def Get_All_Words_In_Group(name: str):
    """
        This method returns a list of all the words in an inputted group.

        Parameters
        -----------
        name: str
            The name of the group of which we wish to receive all the words in it.

        Returns
        -----------
        None
            If a group by the given name doesn't exist in the database.
        list
            A list of strings, the words of the group.
    """
    group_id = find_group_id_by_name(name)
    if group_id is None:
        return None
    else:
        return [search_word_by_id(r[0]) for r in all_words_in_group(group_id)]

def Get_All_Indices_From_Words_In_Group(name: str):
    """
        This method returns the indices (positions) of all words in the group in all songs.

        Parameters
        -----------
        name: str
            The name of the group of whose we wish to find all indices.

        Returns
        -----------
        None
            If there doesn't exist a group by this name
        list
            A list of the different positions of the words of the group in all songs. It is of the form:
            [title of song word is in, author of the song, the word that is in the group, the verse it's in,
            the sentence it's in, it's position within the sentence]
    """
    group_id = find_group_id_by_name(name)
    if group_id is None:
        return None
    else:
        word_ids_of_group = [r[0] for r in all_words_in_group(group_id)]
        all_songs = [r[0] for r in get_all_songs_in_db()]
        if len(all_songs) == 0:
            return 0
        else:
            word_formatted = []
            for s_id in all_songs:
                song_definition = get_song_definition_from_id(s_id)
                for w_id in word_ids_of_group:
                    word_positions = get_word_positions(s_id, w_id)
                    for r in word_positions:
                        word_formatted.append([song_definition[0], song_definition[1], search_word_by_id(w_id), r[0], r[1], r[2]])

            return word_formatted

def Insert_Phrase(phrase: str, no_words):
    """
        Inputs a given string as a phrase into the database. Requires the number of words in the phrase too.

        Parameters
        -----------
        phrase: str
            The phrase to insert into the database
        no_words: int
            Number of words in the phrase
    """
    create_phrase(phrase, no_words)

def Get_All_Songs_Id_Author_Title():
    """
        Returns all the pertinent information regarding all songs in the database.

        Returns
        -----------
        A list of lists, each of the lists on the inside of the form [song_id, song author, song title]
        for all songs in the database
    """
    all_song_entries = getAllSongEntries()
    return [[song[0], song[2], song[1]] for song in all_song_entries]

def Get_Maxes(song_id: int):
    """
    Returns the number of verses and maximum number of sentences in each verse of a given song.

    Parameters
    -----------
    song_id: int
        The song id of the song we wish to find the aforementioned parameters of.

    Returns
    -----------
    list
        A list with two elements - [the number of verses in the given song, the maximum number of sentences in any of
        the verses in the song]
    """
    return [max_verse(song_id), max_sentence(song_id)]


def getAllwordsInDbAscAz():
    """
        Returns all the words in a string with newlines between the words. Returns this in alphabetical order.
    """
    found_words = getAllWordsInDBAZ()
    display_words_list = []
    for w in found_words:
        display_words_list.append(w[0])
    # display_words_list.sort()
    display_words_as_text = "\n".join(display_words_list)
    return display_words_as_text

def getAllwordsInDbDescCount():
    """
        Returns all the words in the db in descending order from the amount they appear in the database.
    """
    found_words = getAllWordsInDBCount()
    display_words_list = []
    for w in found_words:
        word_plus_count = f"{w[0]} (count: {w[1]})"
        display_words_list.append(word_plus_count)
    display_words_as_text = "\n\n".join(display_words_list)
    return display_words_as_text

def getTop10SongsAndValues():
    """
        Returns the top 10 songs by number of words in the song.
        Returns two lists, one for the description of the song, the other for the number of words in the song.
    """
    songs_found = getTop10Songs()
    if len(songs_found) < 1:
        return None
    songs_arr = []
    count_words_arr = []
    for s in songs_found:
        songs_arr.append(f"{s[0]}\n(by {s[1]})")
        count_words_arr.append(s[2])
    return songs_arr, count_words_arr

def getTop10Words(songId: int):
    """
        Returns the top 10 words by number of appearances of these words in a given song.
        Returns two lists, one for the words, the other for the number of times the word appears in the given song.
    """
    words_found = getTop10WordsBySongId(songId)
    words_arr = []
    count_words_arr = []
    for w in words_found:
        words_arr.append(w[0])
        count_words_arr.append(w[1])
    return words_arr, count_words_arr

def getAllSongsInDbByTitle():
    found_songs = getAllSongsInDBByTitle()
    display_songs_list = []
    for s in found_songs:
        song_plus_author = f"\"{s[0]}\", by {s[1]}."
        display_songs_list.append(song_plus_author)
    display_songs_as_text = "\n\n".join(display_songs_list)
    return display_songs_as_text

def getAllSongsByAuthor():
    found_songs = getAllSongsInDBByAuthor()
    display_songs_list = []
    for s in found_songs:
        song_plus_author = f"{s[0]}  \"{s[1]}\""
        display_songs_list.append(song_plus_author)
    display_songs_as_text = "\n\n".join(display_songs_list)
    return display_songs_as_text

def getAllSongsByCount():
    found_songs = getAllSongsUnDBByCount()
    display_songs_list = []
    for s in found_songs:
        song_plus_author = f"({s[0]})  \"{s[1]}\", by {s[2]}."
        display_songs_list.append(song_plus_author)
    display_songs_as_text = "\n\n".join(display_songs_list)
    return display_songs_as_text