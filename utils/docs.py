import json 
import requests 
import base64 
import urllib 
import uuid 
import httplib
from apiclient.discovery import build
from oauth2client import file, client, tools

# Log in ---------------------------vv--------------------------

# Client Keys
CLIENT_ID = json.loads(open("../keys.json").read())['web']['client_id'] 
CLIENT_SECRET = json.loads(open("../keys.json").read())['web']['client_secret'] 

# Google URLS
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://accounts.google.com/o/oauth2/token"

# Server-side Parameters
REDIRECT_URI = 'http://localhost:5000/home/'

# Scopes
GOOGLE_SCOPES = "profile email https://www.googleapis.com/auth/drive.install https://www.googleapis.com/auth/drive.file"



# Storing an API token ---------------------------vv--------------------------

store = file.Storage('storage.json')
credz = store.get()
if not credz or credz.invalid:
	flow = client.flow_from_clientsecrets('../keys.json', GOOGLE_SCOPES)
	credz = tools.run(flow, store)

SERVICE = build('drive', 'v2', http=credz.authorise(httplib.Http()))
files = SERVICE.files().list().execute().get('items', [])
for f in files:
	print f['title'], f['mimeType']

# Create doc ---------------------------vv--------------------------

#