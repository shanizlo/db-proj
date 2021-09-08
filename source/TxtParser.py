def parse(lyrics):  # returns a list of lists of the form [theWord, verse_num, sentence_num, word_position]
    which_sentence = 0  # counts the sentence we are on
    which_verse = 1  # counts the verse we are on
    the_words = []  # the list of lists of the form
    the_sentences = lyrics.splitlines(True)
    for sentence in the_sentences:
        if sentence == "":  # for good measure
            break
        elif sentence == "\n":  # means we jumped a verse
            which_verse += 1
        else:
            which_sentence += 1
            sentence = sentence.lower()  # so we have a uniform standard for the words
            sentence = sentence.strip()  # to remove newline characters at the end of each sentence
            for c in sentence:
                if not (48 <= ord(c) & ord(c) <= 57) | (97 <= ord(c) & ord(c) <= 122) | (ord(c) == 39) | (
                        c == ' '):  # not 0-9, a-z, ', space
                    sentence = sentence.replace(c, '')
            the_split = sentence.split(" ")
            for i in range(len(the_split)):
                the_words.append([the_split[i], which_verse, which_sentence, i + 1])
    return the_words


# TODO: move this file to source directory