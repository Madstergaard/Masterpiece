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


@app.route('/')
def index():
    '''
    # Check if logged in
    if 'access_token' in session:
        # Refresh access token
        print "REFRESHING TOKEN"
        session['access_token'] = auth.refresh(session['refresh_token'])
        return render_template(
            'dashboard.html',
            logged_in = True,
            #artist_data = artist_data,
            event_list = event_list
        )
    else:
        # Authentication url is a Spotify page
        auth_url = auth.authentication_url()
        return render_template('dashboard.html', logged_in = False, auth_url=auth_url)
    '''        
    return render_template('home.html', CLIENT_ID = docs.CLIENT_ID, REDIRECT_URI = docs.REDIRECT_URI)

@app.route('/signIn/')

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
