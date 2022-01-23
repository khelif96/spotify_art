from lib2to3.pytree import convert
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import requests 
import convert_image 
import spotifycode

load_dotenv()

scope = "user-library-read user-read-currently-playing user-read-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

track = sp.current_user_playing_track()

#print(track)

url = track["item"]["album"]["images"][0]["url"]
song = track["item"]["album"]["name"]
artist = track["item"]["artists"][0]["name"]
uri = track["item"]["uri"]
print(artist)
print(song)
print(uri)

if url == None:
    print("No image found")
response = requests.get(url)

file = open("track.png", "wb")
file.write(response.content)
file.close()

convert_image.transformAll()

spotifycode.getSpotifyCode(uri)

convert_image.attachSpotifyCode("track.png", "code.png")

# color = convert_image.getAverageColor("track.png")
convert_image.wordFilter("track.png", artist + " ", color=(0,0,0))

convert_image.combineImages()


# convert_image.getAverageColor("track.png")