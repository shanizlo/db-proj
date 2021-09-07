class Song:
    def __init__(self, author, title, album = None, copyright = None, creation_date = None):
        # TODO: check for a date format
        self.author = author
        self.title = title
        self.album = album
        self.copyright = copyright
        self.creation_date = creation_date

class Word:
    def __init__(self, value):
        self.value = value
        self.length = len(value)

class Group:
    def __init__(self, group_name):
        self.group_name = group_name


class Phrase:
    def __init__(self, phrase_name):
        self.phrase_name = phrase_name
