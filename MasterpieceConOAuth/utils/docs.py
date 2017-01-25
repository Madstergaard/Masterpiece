import json 
import requests 
import base64 
import urllib 
import uuid 

# Client Keys
CLIENT_ID = json.loads(open("keys.json").read())['web']['client_id'] 
CLIENT_SECRET = json.loads(open("keys.json").read())['web']['client_secret'] 

# Spotify URLS
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://accounts.google.com/o/oauth2/token"

# Server-side Parameters
REDIRECT_URI = 'http://localhost:5000/home/'

