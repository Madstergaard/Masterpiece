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



# List Files ---------------------------vv--------------------------



# Create doc ---------------------------vv--------------------------

def createDoc_returnID():
	r = requests.post("https://www.googleapis.com/upload/drive/v3/files", data = {'uploadType':'multipart'})
	return r["id"]



