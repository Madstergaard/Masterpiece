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
    db.close()
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
# userID for original author, authors for all contributors
def addDoc(title, content, userID, status, comments, description, coverURL, authors):
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    cmd = "INSERT INTO docs VALUES ('%s','%s','%d','%s','%s','%s','%s','%s');"%(title, content, userID, status, comments, description, coverURL, authors)
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
    db.close()
    return sel[0]

# if given comment exists, return true
# else, return false
def commentExists(title, userID, comment):
    comments = getComments(title, userID)
    comments = comments[:len(comments)-3].split(";;;")
    for cmt in comments:
        if cmt == comment:
            return True
    return False

# adds a comment to a particular document
def addComment(title, userID, comment):
    if not commentExists(title, userID, comment):
        db = sqlite3.connect("data/database.db")
        c = db.cursor()
        tmp = getComments(title, userID) + comment + ";;;"
        cmd = "UPDATE docs SET comments = '%s' WHERE userID = %d AND title = '%s';"%(tmp, int(userID), title)
        sel = c.execute(cmd)
        db.commit()
        db.close()

# removes a comment from a particular document
def rmComment(title, userID, comment):
    if commentExists(title, userID, comment):
        comments = getComments(title, userID)
        comments = comments[:len(comments)-3].split(";;;")
        newComments = ""
        for cmt in comments:
            if cmt != comment:
                newComments += cmt + ";;;"
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

# changes a document's description
def changeDescription(title, userID, newDescription):
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    cmd = "UPDATE docs SET description = '%s' WHERE userID = %d AND title = '%s';"%(newDescription, int(userID), title)
    sel = c.execute(cmd)
    db.commit()
    db.close()

# changes a document's book cover url
def changeCoverURL(title, userID, newCoverURL):
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    cmd = "UPDATE docs SET coverURL = '%s' WHERE userID = %d AND title = '%s';"%(newCoverURL, int(userID), title)
    sel = c.execute(cmd)
    db.commit()
    db.close()

# returns the list of authors from a particular document
def getAuthors(title, userID):
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    cmd = "SELECT authors FROM docs WHERE userID = %d AND title = '%s';"%(int(userID), title)
    sel = c.execute(cmd).fetchone()
    db.close()
    return sel[0]
    
# if given comment exists, return true
# else, return false
def authorExists(title, userID, author):
    authors = getAuthors(title, userID)
    authors = authors[:len(authors)-3].split(";;;")
    for a in authors:
        if a == author:
            return True
    return False

# adds an author to a particular document
def addAuthor(title, userID, author):
    if not authorExists(title, userID, author):
        db = sqlite3.connect("data/database.db")
        c = db.cursor()
        tmp = getAuthors(title, userID) + author + ";;;"
        cmd = "UPDATE docs SET authors = '%s' WHERE userID = %d AND title = '%s';"%(tmp, int(userID), title)
        sel = c.execute(cmd)
        db.commit()
        db.close()

# removes an author from a particular document
def rmAuthor(title, userID, author):
    if authorExists(title, userID, author):
        authors = getAuthors(title, userID)
        authors = authors[:len(comments)-3].split(";;;")
        newComments = ""
        for a in authors:
            if a != author:
                newAuthors += a + ";;;"
                db = sqlite3.connect("data/database.db")
                c = db.cursor()
                cmd = "UPDATE docs SET authors = '%s' WHERE userID = %d AND title = '%s';"%(newAuthors, int(userID), title)
                sel = c.execute(cmd)
                db.commit()
                db.close()

# returns the title, description, URL to book cover image, author names for all documents
def getLibraryInfo():
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    cmd = "SELECT title, description, coverURL, authors FROM docs;"
    sel = c.execute(cmd)
    db.close()
    return sel
