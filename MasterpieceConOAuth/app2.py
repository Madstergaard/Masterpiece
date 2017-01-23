from flask import Flask, render_template, session, redirect, url_for, request
from utils import accounts, initTables, docs, info
from json import loads, dumps

app = Flask(__name__)
app.secret_key = '95c7fbca92ac5083afda62a564a3d014fc3b72c9140e3cb99ea6bf12'

def isLoggedIn():
    if "access_token" in session:
        return True
    else:
        return False


@app.route("/", methods = ['GET', 'POST'])
def login():
    if 'access_token' in session:
        session['access_token'] = docs.refresh(session['refresh_token'])
        return redirect(url_for("home"))
    else:
        auth_url = docs.authentication_url()
        return render_template('home.html', logged_in = False, auth_url = auth_url, CLIENT_ID = docs.CLIENT_ID)

@app.route("/logout/")
def logout():
    session.pop('access_token')
    session.pop('refresh_token')
    return redirect(url_for("login"))

@app.route("/home/", methods = ['GET'])
def home():
    if not isLoggedIn():
        return redirect(url_for("login"))
    return render_template('library.html') # my workshop when created

@app.route("/library/")
# title, description, URL to book cover image, author names
def library():
    entries = accounts.getLibraryInfo()
    return render_template('library.html', lib = entries)

if __name__ == "__main__":
    app.debug = True
    app.run()
