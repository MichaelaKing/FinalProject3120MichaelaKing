import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import matplotlib.pyplot as plt

# Identity of the user
CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'https://oauth.pstmn.io/v1/callback'


scope = 'user-top-read'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope
))
# Getter for the top user data
def get_user_top_data():
    print("Fetching user's top artists and tracks...")
    top_artists = sp.current_user_top_artists(limit=20, time_range='medium_term')
    top_tracks = sp.current_user_top_tracks(limit=20, time_range='medium_term')
    
    artists_data = [{
        'Name': artist['name'],
        'Genres': ', '.join(artist['genres']),
        'Popularity': artist['popularity']
    } for artist in top_artists['items']]

    tracks_data = [{
        'Name': track['name'],
        'Artist': ', '.join([artist['name'] for artist in track['artists']]),
        'Popularity': track['popularity'],
        'Danceability': sp.audio_features(track['id'])[0]['danceability'],
        'Energy': sp.audio_features(track['id'])[0]['energy']
    } for track in top_tracks['items']]

    return pd.DataFrame(artists_data), pd.DataFrame(tracks_data)

# Analyze users music taste by breaking comparing them to popular artists
def analyze_music_taste(artists_df, tracks_df):
    # Most popular artists
    top_artists = artists_df.sort_values('Popularity', ascending=False).head(5)
    print("\nTop Artists:")
    print(top_artists)

    # Danceability and Energy Analysis
    print("\nTracks Danceability & Energy:")
    print(tracks_df[['Name', 'Danceability', 'Energy']])

    # Plot: Danceability vs Energy
    plt.figure(figsize=(10, 6))
    plt.scatter(tracks_df['Danceability'], tracks_df['Energy'], alpha=0.7)
    for i in range(len(tracks_df)):
        plt.text(tracks_df['Danceability'].iloc[i], tracks_df['Energy'].iloc[i], tracks_df['Name'].iloc[i], fontsize=9)
    plt.title('Danceability vs Energy of Tracks')
    plt.xlabel('Danceability')
    plt.ylabel('Energy')
    plt.grid()
    plt.show()

    # Popularity distribution
    plt.figure(figsize=(10, 6))
    plt.hist(tracks_df['Popularity'], bins=10, alpha=0.7, color='blue')
    plt.title('Track Popularity Distribution')
    plt.xlabel('Popularity')
    plt.ylabel('Frequency')
    plt.grid()
    plt.show()

# Main
def main():
    artists_df, tracks_df = get_user_top_data()
    analyze_music_taste(artists_df, tracks_df)

if __name__ == "__main__":
    main()
