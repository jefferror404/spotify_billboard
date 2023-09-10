import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

#---------------Spotify authentication-----------------
YOUR_APP_CLIENT_ID = "YOUR SPOTIFY APP CLIENT ID"
YOUR_APP_CLIENT_SECRET = "YOUR SPOTIFY APP CLIENT SECRET"
URI = "http://example.com"
USER_NAME = "YOUR USER NAME"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=YOUR_APP_CLIENT_ID,
                                               client_secret=YOUR_APP_CLIENT_SECRET,
                                               redirect_uri=URI,
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt",
                                               username=USER_NAME,
                                               ))
user_id = sp.current_user()["id"]

#---------------User Input for the date-----------------
chosen_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD ")
URL = f"https://www.billboard.com/charts/hot-100/{chosen_date}"

response = requests.get(URL)
billboard_page = response.text

#---------------Getting billboard top 100 songs list-----------------
soup = BeautifulSoup(billboard_page, "html.parser")
song_names_spans = soup.select("li ul li h3")
song_list = []
for song in song_names_spans:
    song_name = song.getText().strip()
    song_list.append(song_name)

#---------------Searching the songs of the song list on Spotify-----------------
song_uris = []
chosen_year = chosen_date.split("-")[0]
for song in song_list:
    result = sp.search(q=f"track:{song} year:{chosen_year}", type="track")
#    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} does not exist on Spotify. Skipped")
print(song_uris)

#---------------Creating the playlist on Spotify using the 100 songs uri-----------------
playlist = sp.user_playlist_create(user=user_id, name=f"{chosen_date} Billboard 100", public=False)
print(playlist)
playlist_id = playlist["id"]

sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)

