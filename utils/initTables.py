import sqlite3

# creating the tables in the database
db = sqlite3.connect("data/database.db")
c = db.cursor()
cmd = "CREATE TABLE IF NOT EXISTS accounts(user TEXT, hashedPass TEXT, userID INTEGER);"
c.execute(cmd)
cmd = "CREATE TABLE IF NOT EXISTS docs(title TEXT, content TEXT, userID INTEGER, status TEXT, comments TEXT);"
c.execute(cmd)

db.commit()
db.close()
