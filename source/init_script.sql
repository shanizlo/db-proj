CREATE TABLE IF NOT EXISTS songs (
    song_id INTEGER NOT NULL PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    creation_date DATETIME,
    copyright TEXT,
    UNIQUE(title, author),
    CHECK(title <> ''),
    CHECK(author <> '')
);

CREATE TABLE IF NOT EXISTS words (
    word_id INTEGER NOT NULL PRIMARY KEY,
    word_value TEXT NOT NULL,
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

CREATE TABLE IF NOT EXISTS words_group (
    group_id INTEGER NOT NULL PRIMARY KEY,
    group_name TEXT NOT NULL UNIQUE,
    word_id INTEGER NOT NULL,
    word_position INTEGER NOT NULL,
    FOREIGN KEY(word_id) REFERENCES words,
    CHECK(group_name <> '')
);

CREATE TABLE IF NOT EXISTS phrase (
    id INTEGER NOT NULL PRIMARY KEY,
    word_id INTEGER NOT NULL,
    word_position INTEGER,
    FOREIGN KEY(word_id) REFERENCES words
);