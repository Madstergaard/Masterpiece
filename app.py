from flask import Flask, render_template, session, redirect, url_for, request
from utils import accounts, initTables, info

app = Flask(__name__)
app.secret_key = '95c7fbca92ac5083afda62a564a3d014fc3b72c9140e3cb99ea6bf12'


#-------------------------------HELPER FUNCTIONS----------------------------------
def isLoggedIn():
    return 'username' in session

#------------------------------------OTHER----------------------------------------
@app.route("/", methods = ['GET', 'POST'])
def login():
    if isLoggedIn():
        return redirect(url_for("library"))
    else:
        msg = ''
        if request.method == 'POST':
            username = request.form['user']
            password = request.form['pass']
            hashedPass = accounts.hashPass(password)
            if 'login' in request.form:
                if not accounts.userExists(username):
                    msg = 'User does not exist'
                else:
                    if accounts.verify(username, hashedPass):
                        session['username'] = username
                        session['userID'] = accounts.getUID(username)
                        return redirect(url_for("library"))
                    else:
                        msg = 'Wrong password'
            if 'register' in request.form:
                if not accounts.userExists(username):
                    accounts.register(username, hashedPass)
                    msg = 'Successfully logged in'
                    session['username'] = username
                    session['userID'] = accounts.getUID(username)
                    return redirect(url_for("library"))
                else:
                    msg = 'User already exists'
        return render_template('home.html', msg = msg)

@app.route("/logout/")
def logout():
    session.pop('username')
    session.pop('userID')
    return redirect(url_for("login"))

@app.route("/create/")
def create():
    if not isLoggedIn():
        return redirect(url_for("login"))
    else:
        return render_template('create.html')

@app.route("/createDoc/", methods = ['POST'])
def createDoc():
    if not isLoggedIn():
        return redirect(url_for("login"))
    else:
        title  = request.form['title']
        description = request.form['description']
        image = request.form['image']
        privacy = request.form['privacy']
        content = "" #probably GoogleDocs link
        userID = session['userID']
        comments = ""
        authors = session['username'] + ";;;"
        accounts.addDoc(title, content, userID, privacy, comments, description, image, authors)
        return redirect(url_for('library')) # redirects to doc page when created

'''
@app.route("<author>/<title>")
def doc(author, title):
    if not isLoggedIn():
        return redirect(url_for("login"))
    else:
        ogAuthor = getUID(author)
        doc = getContent(title, ogAuthor)
        privacy = getStatus(title, ogAuthor)
        description = getDescription(title, ogAuthor)
        authors = getAuthors(title, ogAuthor)
        # if doc is private, check if authorExists(title, ogAuthor, session['username'])
        return render_template('doc.html')
'''

@app.route("/workshop/")
def workshop():
    if not isLoggedIn():
        return redirect(url_for("login"))
    else:
        docs = accounts.getUserDocs(session['userID'])
        return render_template('workshop.html', work = docs)

@app.route("/library/")
# title, description, URL to book cover image, author names
def library():
    if not isLoggedIn():
        return redirect(url_for("login"))
    else:
        entries = accounts.getLibraryInfo()
        print entries
        return render_template('library.html', lib = entries)

if __name__ == "__main__":
    app.debug = True
    app.run()
