import sqlite3, hashlib

#-----------------------------ACCOUNTS TABLE-----------------------------

# if username given matches a username in the database, return true
# else, return false
def userExists(user):
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    cmd = "SELECT * FROM accounts;"
    sel = c.execute(cmd)
    for record in sel:
        if user == record[0]:
            db.close()
            return True
    db.close()
    return False

# adds user to the database
def register(user, hashedPass):
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    cmd = "SELECT userID FROM accounts ORDER BY userID DESC;"
    sel = c.execute(cmd)
    userID = 1
    iList = ""
    for record in sel:
        userID = userID + record[0]
        break
    entry = "INSERT INTO accounts VALUES ('%s','%s','%d');"%(user, hashedPass, userID)
    c.execute(entry)
    db.commit()
    db.close()    

# if username and hashed password given match a username and its corresponding hashed password in the database, return true
# else, return false
def verify(user, hashedPass):
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    cmd = "SELECT * FROM accounts;"
    sel = c.execute(cmd)
    for record in sel:
        if user == record[0] and hashedPass == record[1]:
            db.close()
            return True
    db.close()
    return False

# returns the unique userID associated with a user account
def getUID(user):
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    id = ""
    cmd = "SELECT * FROM accounts;"
    sel = c.execute(cmd)
    for record in sel:
        if user == record[0]:
            id = record[2]
    db.close()
    return id

# returns a hashed version of the password
def hashPass(password):
    return hashlib.sha224(password).hexdigest()
    
# returns a user's hashed password
def getPass(userID):
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    cmd = "SELECT hashedPass FROM accounts WHERE userID = %d;"%(userID)
    sel = c.execute(cmd).fetchone()
    return sel[0]

# changes a user's hashed password
def changePass(newHashedPass, userID):
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    cmd = "UPDATE accounts SET hashedPass = '%s' WHERE userID = %d;"%(newHashedPass, int(userID))
    sel = c.execute(cmd)
    db.commit()
    db.close()

#-------------------------------DOCS TABLE-------------------------------

# adds a document and its settings into the docs table
def addDoc(title, content, userID, status, comments):
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    cmd = "INSERT INTO docs VALUES ('%s','%s','%d','%s','%s');"%(title, content, userID, status, comments)
    c.execute(cmd)
    db.commit()
    db.close()

# changes a document's title
def changeTitle(title, userID, newTitle):
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    cmd = "UPDATE docs SET title = '%s' WHERE userID = %d AND title = '%s';"%(newTitle, int(userID), title)
    sel = c.execute(cmd)
    db.commit()
    db.close()

# changes a document's status from private to public or public to private
def changeStatus(title, userID, newStatus):
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    cmd = "UPDATE docs SET status = '%s' WHERE userID = %d AND title = '%s';"%(newStatus, int(userID), title)
    sel = c.execute(cmd)
    db.commit()
    db.close()

# returns the list of comments from a particular document
def getComments(title, userID):
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    cmd = "SELECT comments FROM docs WHERE userID = %d AND title = '%s';"%(int(userID), title)
    sel = c.execute(cmd).fetchone()
    return sel[0]

# adds a comment to a particular document
def addComment(title, userID, comment):
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    tmp = getComments(title, userID) + comment + ";"
    cmd = "UPDATE docs SET comments = '%s' WHERE userID = %d AND title = '%s';"%(tmp, int(userID), title)
    sel = c.execute(cmd)
    db.commit()
    db.close()

# if given comment exists, return true
# else, return false
def commentExists(title, userID, comment):
    comments = getComments(title, userID)
    comments = comments[:len(comments)-1].split(";")
    for c in comments:
        if c == comment:
            return True
    return False

# removes a comment from a particular document
def rmComment(title, userID, comment):
    comments = getComments(title, userID)
    comments = comments[:len(comments)-1].split(";")
    newComments = ""
    for c in comments:
        if c != comment:
            newComments += c + ";"
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    cmd = "UPDATE docs SET comments = '%s' WHERE userID = %d AND title = '%s';"%(newComments, int(userID), title)
    sel = c.execute(cmd)
    db.commit()
    db.close()

# if we end up storing the content
# if not, function is unnecessary because link does not change
def updateContent(title, userID, newContent):
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    cmd = "UPDATE docs SET content = '%s' WHERE userID = %d AND title = '%s';"%(newContent, int(userID), title)
    sel = c.execute(cmd)
    db.commit()
    db.close()
