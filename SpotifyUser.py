import requests
import base64
import json
import webbrowser
import urllib.parse

#Spotify credentials (replace with your actual values)
CLIENT_ID = '8810837ef20d4cb7a5fdf4260e366409'
CLIENT_SECRET = '13e560bd868245e9b6dc58328837b2aa'
REDIRECT_URI = 'http://localhost:8888/callback'
SCOPE = 'user-top-read'

#Step 1: Get user authorization
def get_user_authorization():
    auth_url = 'https://accounts.spotify.com/authorize'
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPE
    }
    auth_request = f"{auth_url}?{urllib.parse.urlencode(params)}"
    print("Opening browser for Spotify authorization...")
    webbrowser.open(auth_request)

#Step 2: Exchange authorization code for an access token
def get_access_token(auth_code):
    token_url = 'https://accounts.spotify.com/api/token'
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {'Authorization': f"Basic {auth_header}"}
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI
    }
    response = requests.post(token_url, headers=headers, data=data)
    return response.json().get('access_token')

#Step 3: Fetch user's top artists
def fetch_top_artists(access_token):
    headers = {'Authorization': f"Bearer {access_token}"}
    endpoint = 'https://api.spotify.com/v1/me/top/artists'
    params = {'limit': 10}#Fetch top 10 artists
    response = requests.get(endpoint, headers=headers, params=params)
    return response.json()

#Main execution
if __name__ == "__main__":
    #Step 1: Ask the user to authorize
    print("Step 1: Authorize the app...")
    get_user_authorization()
    print("After authorization, copy the 'code' parameter from the URL and paste it here.")
    auth_code = input("Enter the authorization code: ").strip()

    #Step 2: Get access token
    print("\nStep 2: Fetching access token...")
    access_token = get_access_token(auth_code)
    if not access_token:
        print("Failed to get access token. Check your credentials and authorization code.")
        exit()

    #Step 3: Fetch top artists
    print("\nStep 3: Fetching your top artists...")
    top_artists = fetch_top_artists(access_token)

    #Display results
    print("\nYour Top Artists:")
    for idx, artist in enumerate(top_artists.get('items', []), start=1):
        print(f"{idx}. {artist['name']}")
