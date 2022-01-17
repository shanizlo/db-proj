def parse(lyrics):  # returns a list of lists of the form [theWord, verse_num, sentence_num, word_position]
    """
        This file contains this single method that parses given text from a text file which contains lyrics to songs.
        Moving from verse to verse uses two newline characters.
        Moving from sentence to sentence uses one newline character.

        Parameters
        -----------
        lyrics
            A string containing lyrics to songs.

        Returns
        -----------
        list
            List of lists of the form [word, which verse, which sentence, which position].
    """
    which_sentence = 0  # counts the sentence we are on
    which_verse = 1  # counts the verse we are on
    the_words = []  # the list of lists of the form
    the_sentences = lyrics.splitlines(True)
    i = 0
    while i < len(the_sentences):
        if the_sentences[i] == "":  # for good measure
            i = i + 1
            break
        elif the_sentences[i] == "\n":  # means we jumped a verse
            if which_sentence == 0: #To handle song that starts with newlines
                i = i + 1
                continue
            if i + 1 < len(the_sentences): # to avoid skipping verse if there twice new line
                if the_sentences[i+1] == "\n":
                    i = i + 1
            which_verse += 1
            which_sentence = 0
            i = i + 1
        else:
            which_sentence += 1
            the_sentences[i] = the_sentences[i].lower()  # so we have a uniform standard for the words
            the_sentences[i] = the_sentences[i].strip()  # to remove newline characters at the end of each sentence
            for c in the_sentences[i]:
                if not (48 <= ord(c) & ord(c) <= 57) | (97 <= ord(c) & ord(c) <= 122) | (ord(c) == 39) | (
                        c == ' '):  # not 0-9, a-z, ', space
                    the_sentences[i] = the_sentences[i].replace(c, '')
            the_split = the_sentences[i].split(" ")
            for j in range(len(the_split)):
                if the_split[j] != '':
                    the_words.append([the_split[j], which_verse, which_sentence, j + 1])
            i = i + 1

    return the_words
