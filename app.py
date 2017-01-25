from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from apiai import apiai
from utils import accounts, initTables, info, docs
import json

app = Flask(__name__)
app.secret_key = '95c7fbca92ac5083afda62a564a3d014fc3b72c9140e3cb99ea6bf12'
agent = apiai.ApiAI('5294825b21dc4746851ba49e25ff909b') # client access token

writingType = ''
topic = ''

#-------------------------------HELPER FUNCTIONS----------------------------------
def isLoggedIn():
    return 'username' in session

def checkImage(img):
    extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
    for ext in extensions:
        if ext in img:
            return True
    return False

# replaces all instances of ' or " to ` to prevent sqlite errors
def cleanString(s):
    s = s.replace("'", '`')
    s = s.replace('"', '`')
    return s

#string = "That's great, but I\"d rather not."
#print cleanString(string)

# converts string to a list of strings
# primarily for authors/comments retrieved from the db
def stringToList(s):
    strings = s[:len(s)-3].split(';;;')
    return strings

#print stringToList('hello;;;nice to meet you;;;')

# converts tuple to list
def tupleToList(t):
    newList = []
    for entry in t:
        entry = list(entry)
        lEntry = []
        for item in entry:
            if isinstance(item, int):
                lEntry.append(item)
            else:
                if ';;;' in item:
                    lEntry.append(stringToList(str(item)))
                else:
                    lEntry.append(str(item))
        newList.append(lEntry)
    return newList

#-------------------------------API.AI FUNCTIONS----------------------------------

def saveType(inputType):
    writingType = inputType
    return writingType

def saveTopic(inputTopic):
    topic = inputTopic
    quote = info.firstQuote(topic)[0]
    return quote

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
        return render_template('home.html', msg = msg, CLIENT_ID = docs.CLIENT_ID, REDIRECT_URI = docs.REDIRECT_URI)

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
        title  = cleanString(str(request.form['title']))
        print title
        if accounts.titleExists(title, session['userID']):
            return render_template('create.html', msg = "Title already exists. Choose another title.")
        else:
            description = cleanString(str(request.form['description']))
            image = request.form['image']
            if not checkImage(image):
                image = 'http://www.kalahandi.info/wp-content/uploads/2016/05/sorry-image-not-available.png'
            privacy = request.form['privacy']
            content = "" #probably GoogleDocs link
            userID = session['userID']
            comments = ""
            authors = session['username'] + ";;;"
            
            if len(title) < 1 or len(description) < 1 or len(image) < 1:
                return render_template('create.html', msg = "Missing fields. Please complete all the fields in the form.")
            
            accounts.addDoc(title, content, userID, privacy, comments, description, image, authors)
            author = str(session['username'])
            title = str(title)
            return redirect(url_for("doc", author = author, title = title, CLIENT_ID = docs.CLIENT_ID, REDIRECT_URI = docs.REDIRECT_URI))

@app.route("/temp/")
def temp():
    return render_template('chat.html')
        
@app.route("/chat/", methods = ['POST'])
def chat():
    userInput = request.form['input']
    #print userInput
    q = agent.text_request()
    q.session_id = "<session_id>"
    q.query = userInput
    response = q.getresponse().read()
    d = json.loads(response)
    result = d['result']
    botResponse = result['fulfillment']['speech']
    #print botResponse
    if result['action'] == 'saveType':
        print saveType(userInput)
    if result['action'] == 'saveTopic':
        botResponse += saveTopic(userInput)
        
    return jsonify({'botOutput' : botResponse }) 
        
@app.route("/<author>/<title>/")
def doc(author, title):
    if not isLoggedIn():
        return redirect(url_for("login"))
    else:
        print "author" + author
        ogAuthor = accounts.getUID(author)
        #print ogAuthor
        doc = accounts.getContent(title, ogAuthor)
        #print doc
        privacy = accounts.getStatus(title, ogAuthor)
        #print privacy
        description = accounts.getDescription(title, ogAuthor)
        #print description
        authors = stringToList(str(accounts.getAuthors(title, ogAuthor)))
        #print authors
        if privacy == 'private':
            if accounts.authorExists(title, ogAuthor, session['username']):
                return render_template('doc.html', title = title, doc = doc, privacy = privacy, description = description, authors = authors, CLIENT_ID = docs.CLIENT_ID, REDIRECT_URI = docs.REDIRECT_URI)
            else:
                return render_template('doc.html', msg = 'You don\'t have access to this document.', CLIENT_ID = docs.CLIENT_ID, REDIRECT_URI = docs.REDIRECT_URI)
        # if doc is public
        return render_template('doc.html', title = title, doc = doc, privacy = privacy, description = description, authors = authors, CLIENT_ID = docs.CLIENT_ID, REDIRECT_URI = docs.REDIRECT_URI)

@app.route("/workshop/")
def workshop():
    if not isLoggedIn():
        return redirect(url_for("login"))
    else:
        docs = list(accounts.getUserDocs(session['userID']))
        docs = tupleToList(docs)
        print docs
        return render_template('workshop.html', work = docs)

@app.route("/library/")
# title, description, URL to book cover image, author names
def library():
    if not isLoggedIn():
        return redirect(url_for("login"))
    else:
        entries = accounts.getLibraryInfo()
        entries = tupleToList(entries)
        print entries
        return render_template('library.html', lib = entries, CLIENT_ID = docs.CLIENT_ID, REDIRECT_URI = docs.REDIRECT_URI)

if __name__ == "__main__":
    app.debug = True
    app.run()
