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
REDIRECT_URI = 'http://127.0.0.1:5000/login/'
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()
STATE = str(uuid.uuid4())

# The parameter for the authentication url (the 'MOSSY wants to connect to your account' page)
auth_query_params = {
    'response_type': 'token',
    'client_id': CLIENT_ID,
    'redirect_uri': REDIRECT_URI,
    'scope': 'profile',
    'state': STATE,
    'prompt': 'select_account consent',
    'include_granted_scopes': 'true'
    
}

# Formats the params above into a nice url
def authentication_url():
    url_args = urllib.urlencode(auth_query_params)
    auth_url = '{}/?{}'.format(GOOGLE_AUTH_URL, url_args)
    return auth_url

def check_state(state):
    return state == STATE

# After the user accepts the request from MOSSY, a POST request is made with the auth_token to obtain
# an access_token and a refresh_token
def token_request(auth_token):
    # Request body params
    post_query_params = {
        'grant_type': 'authorization_code',
        'code': str(auth_token),
        'redirect_uri': REDIRECT_URI
    }
    # Header Parameter (encodes the CLIENT_ID and CLIENT_SECRET)
    encoded_secret = base64.b64encode('{}:{}'.format(CLIENT_ID, CLIENT_SECRET))
    headers = {'Authorization': 'Basic {}'.format(encoded_secret)}
    # POST request
    post_request = requests.post(GOOGLE_TOKEN_URL, data=post_query_params, headers=headers)
    # Response JSON data with 'access_token', 'token_type', 'scope', 'expires_in' and 'refresh_token'
    # **Right now the app's only using the access_token, but once it expires, there's no fallback
    response_data = json.loads(post_request.text)
    return response_data

# Returns new access_token
def refresh(refresh_token):
    params = {
        'grant_type':'refresh_token',
        'refresh_token':refresh_token
    }
    encoded_secret = base64.b64encode('{}:{}'.format(CLIENT_ID, CLIENT_SECRET))
    headers = {'Authorization': 'Basic {}'.format(encoded_secret)}
    request = requests.post(GOOGLE_TOKEN_URL, data=params, headers=headers)
    return json.loads(request.text)['access_token']


