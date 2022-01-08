CREATE TABLE IF NOT EXISTS songs (
    song_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    copyright TEXT,
    album TEXT,
    UNIQUE(title, author),
    CHECK(title <> ''),
    CHECK(author <> '')
);

CREATE TABLE IF NOT EXISTS words (
    word_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    word_value TEXT NOT NULL UNIQUE,
    word_length INTEGER,
    CHECK(word_value <> '')
);

CREATE TABLE IF NOT EXISTS contains (
    word_id INTEGER NOT NULL,
    song_id INTEGER NOT NULL,
    verse_num INTEGER,
    sentence_num INTEGER,
    word_position INTEGER,
    FOREIGN KEY(song_id) REFERENCES songs,
    FOREIGN KEY(word_id) REFERENCES words
);

CREATE TABLE IF NOT EXISTS wordsInGroup (
    group_id INTEGER NOT NULL,
    word_id INTEGER NOT NULL,
    FOREIGN KEY(word_id) REFERENCES words,
    FOREIGN KEY(group_id) REFERENCES groups
);

CREATE TABLE IF NOT EXISTS groups (
    group_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    group_name TEXT NOT NULL UNIQUE,
    CHECK(group_name <> '')
);

CREATE TABLE IF NOT EXISTS phrases (
    phrase_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    phrase_name TEXT NOT NULL UNIQUE,
    CHECK(phrase_name <> '')

);

CREATE TABLE IF NOT EXISTS wordsInPhrase (
    phrase_id INTEGER NOT NULL,
    word_id INTEGER NOT NULL,
    word_position INTEGER,
    FOREIGN KEY(word_id) REFERENCES words,
    FOREIGN KEY(phrase_id) REFERENCES phrases
);