from database import *
from helpers_validators import *


# Finds song by author and title and shows it words in alphabetic order as text
def SearchSongWords(author: str, title: str):
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


# Finds song by author and title and shows it words in alphabetic order as list, in case of error returns "None"
def SearchSongWordsOrReturnNone(author: str, title: str):
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


def SearchWordByPositionInSong(author, title, verseNum, lineNum, wordNum):
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


def ReturnWordContext(author: str, title: str, word_value):
    # get all wordId where value=value and song_id=song_id
    # TODO: find a way to reuse song_id from a previos search and maybe words as well
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
    song_id = search_song_id(author, title)
    if song_id is not None:
        number_of_words = 0
        number_of_characters = 0
        number_of_verses = 0
        number_of_sentences = 0

        words_in_song = search_words_ids_song_contains(song_id) # fetchall returns a list of tuples
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
        return [number_of_words, number_of_characters / number_of_sentences, number_of_characters / number_of_verses]

    else:
        return None


def stringOk(s: str):
    return s is not None and s != ""


def From_UI_Into_Group(name: str, words):
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
    group_id = find_group_id_by_name(name)
    if group_id is None:
        return None
    else:
        return [search_word_by_id(r[0]) for r in all_words_in_group(group_id)]

def Get_All_Indices_From_Words_In_Group(name: str):
    group_id = find_group_id_by_name(name)
    if group_id is None:
        return None
    else:
        word_ids_of_group = [r[0] for r in all_words_in_group(group_id)]
        all_songs = [r[0] for r in get_all_songs_in_db()]
        if len(all_songs) == 0:
            return 0
        else:
            word_formatted = []  # list of lists of the form - (title, author, word, verse_num, sentence_num, word_position)
            for s_id in all_songs:
                song_definition = get_song_definition_from_id(s_id)
                for w_id in word_ids_of_group:
                    word_positions = get_word_positions(s_id, w_id)
                    for r in word_positions:
                        word_formatted.append([song_definition[0], song_definition[1], search_word_by_id(w_id), r[0], r[1], r[2]])

            return word_formatted
