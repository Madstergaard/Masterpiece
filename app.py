from flask import Flask, render_template, session, redirect, url_for, request
from utils import accounts, initTables, docs, info

app = Flask(__name__)
app.secret_key = '95c7fbca92ac5083afda62a564a3d014fc3b72c9140e3cb99ea6bf12'


#-------------------------------HELPER FUNCTIONS----------------------------------
def isLoggedIn():
    return 'username' in session

#------------------------------------OTHER----------------------------------------
@app.route("/", methods = ['GET', 'POST'])
def login():
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
                    return redirect(url_for("home"))
                else:
                    msg = 'Wrong password'
        if 'register' in request.form:
            if not accounts.userExists(username):
                accounts.register(username, hashedPass)
                msg = 'Successfully logged in'
                session['username'] = username
                session['userID'] = accounts.getUID(username)
                return redirect(url_for("home"))
            else:
                msg = 'User already exists'
    return render_template('home.html', msg = msg)

@app.route("/logout/")
def logout():
    session.pop('username')
    return redirect(url_for("login"))

@app.route("/home/", methods = ['GET'])
def home():
    if not isLoggedIn():
        return redirect(url_for("login"))
    return render_template('library.html') # my workshop when created

@app.route("/create/", methods = ['POST'])
def create():
    if not isLoggedIn():
        return redirect(url_for("login"))
    title  = request.form['title']
    description = request.form['description']
    image = request.form['image']
    privacy = request.form['privacy']
    content = "" #probably GoogleDocs link
    userID = session['userID']
    comments = ""
    authors = session['username'] + ";;;"
    accounts.addDoc(title, content, userID, privacy, comments, description, image, authors)
    return redirect(url_for('home'))
    

@app.route("/library/")
# title, description, URL to book cover image, author names
def library():
    entries = accounts.getLibraryInfo()
    return render_template('library.html', lib = entries)

if __name__ == "__main__":
    app.debug = True
    app.run()
