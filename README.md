# spotify-auto-playlist
Generate a new playlist with songs on spotify based on your emotions with AI.

This is how it works:

1.- Create an .env file to put yor credentials in this format:

SPOTIPY_CLIENT_ID="YOUR_CLIENT_ID"
SPOTIPY_CLIENT_SECRET="YOUR_CLIENT_SECRET"
SPOTIPY_REDIRECT_URI="URL"

2.- Load yor .env variables with load_dotenv().
3.- Authenticate and get Spotify user (just to ensure connection).
4.- vader_lexicon is a tool that helps you to identify lexic emotions (you can download it once, then you can coment that line).
5.- Get emotion based on the user input.
6.- Create playlist for that emotion (if not exist).
7.- Add songs without repeating them.
