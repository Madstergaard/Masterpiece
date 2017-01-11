from flask import Flask, render_template, session, redirect, url_for, request
from utils import accounts, initTables, docs, info

app = Flask(__name__)
app.secret_key = '95c7fbca92ac5083afda62a564a3d014fc3b72c9140e3cb99ea6bf12'

@app.route("/", methods = ['GET', 'POST'])
def login():
    msg = ""
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
                    return redirect(url_for("home"))
                else:
                    msg = 'Wrong password'
        if 'register' in request.form:
            if not accounts.userExists(username):
                accounts.register(username, hashedPass)
                msg = 'Successfully logged in'
            else:
                msg = 'User already exists'

    return render_template('home.html', msg = msg)

@app.route("/logout/")
def logout():
    session.pop('username')
    return redirect(url_for("login"))

@app.route("/home/", methods = ['GET'])
def home():
    return render_template('home.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
