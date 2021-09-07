import sqlite3

# _conn = sqlite3.Connection
# _cursor = sqlite3.Cursor
connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

sql_file = open("init_script.sql")
sql_as_string = sql_file.read()
cursor.executescript(sql_as_string)


connection.commit()
connection.close()
#
# for row in cursor.execute("SELECT * FROM songs"):
#     print row