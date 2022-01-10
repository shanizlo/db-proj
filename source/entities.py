class Song:
    def __init__(self, author, title, album = None, copyright = None):
        self.author = author
        self.title = title
        self.album = album
        self.copyright = copyright


class Word:
    def __init__(self, value):
        self.value = value
        self.length = len(value)


class Group:
    def __init__(self, group_name):
        self.group_name = group_name