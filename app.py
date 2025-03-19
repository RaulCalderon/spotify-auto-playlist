import spotipy, os, random, nltk
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Load .env variabes
load_dotenv()

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id = os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri="URL",
    scope="playlist-modify-public"
))

# Get the user ID from Spotify
user = spotify.me()['id']

# Ensure VADER is available
# NOTE: If downloaded it once, you can comment this line
nltk.download('vader_lexicon')

# Determine an emotion based on what user type
def analyze_emotion(txt):

    # Create the emotion analyzer
    mood = SentimentIntensityAnalyzer()

    score = mood.polarity_scores(txt)

    if score['compound'] > 0.1:
        return "happy"
    elif score['compound'] < -0.1:
        return "sad"
    else:
        return "neutral"

# Search songs related to that emotion
def search_songs_emotion(mood):
    if mood == "happy":
        query = "happy"
    elif mood == "sad":
        query = "sad"
    else:
        query = "neutral"

    results = spotify.search(q=query, type="track", limit=10)

    songs = []
    
    # Gets through the items and adds them to the songs array
    for item in results["tracks"]["items"]:
        songs.append((item["name"], item["id"]))
    
    return songs

# Create a playlist for that emotion (if not exists)
def create_playlist_emotion(user, name, description="Playlist generated with AI"):

    # Get all the user playlists (until 50)
    various_playlist = spotify.current_user_playlists(limit=50)["items"]

    # Check if currently there is a playlist with the same name
    for playlist in various_playlist:
        if playlist["name"].lower() == name.lower():
            print(f"Playlist {name} already exists.")
            return playlist["id"]

    # If not exists, create it
    playlist = spotify.user_playlist_create(user, name, description=description)
    print(f"{name} playlist was created.")
    return playlist["id"]

# Add NON existing songs to that playlist
def add_songs_to_playlist(playlist_id, songs):

    # Get songs IDs
    ids = [song[1] for song in songs]

    # Get current songs on playlist
    existing_tracks = spotify.playlist_tracks(playlist_id)["items"]
    existing_ids = [track["track"]["id"] for track in existing_tracks]

    # Filter only songs that are not in the playlist
    filtered = [id for id in ids if id not in existing_ids]

    if filtered:
        spotify.playlist_add_items(playlist_id, filtered)
        print("Songs added.")
    else:
        print("Songs already exists on the playlist.")

def get_random_songs(gender, quantity=10):
    results = spotify.search(q=f"genre:{gender}", type="track", limit=50)
    songs = [(track["name"], track["uri"]) for track in results["tracks"]["items"]]
    return random.sample(songs, quantity)

def add_random_songs(playlist_id, available_songs, quantity=10):

    # Add 10 random songs without duplicate an existing one
    existing_tracks = spotify.playlist_tracks(playlist_id)["items"]
    existing_ids = [track["track"]["id"] for track in existing_tracks]

    # Get all the available songs IDs
    ids = [c[1] for c in available_songs]

    # Filter songs that are not in the playlist
    new_songs = [id for id in ids if id not in existing_ids]

    # Pick randomly new songs
    songs_to_add = random.sample(new_songs, min(quantity, len(new_songs)))

    if songs_to_add:
        spotify.playlist_add_items(playlist_id, songs_to_add)
        print(f"{len(songs_to_add)} new songs added.")
    else:
        print("No songs to add.")

# Get the user input
user_input = input("Tell me, how are you feeling today? ")

# Get the detected emotion
mood = analyze_emotion(user_input)

# Create Playlist
playlist_name = f"{mood.capitalize()} playlist"
playlist_id = create_playlist_emotion(user, playlist_name)

# Search songs
search_songs = search_songs_emotion(mood)

# Add these songs to the playlist (only once when create playlist)
add_songs_to_playlist(playlist_id, search_songs)

# Match Music gender with emotions (can be changed if needed)
genders = {
    "happy": "electronic",
    "sad": "blues",
    "neutral": "jazz"
}

gender = genders[mood]

# Add more non existing songs to that playlist
random_songs = get_random_songs(gender)
add_random_songs(playlist_id, random_songs)