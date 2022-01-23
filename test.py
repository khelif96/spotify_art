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
artists = ""
for artist in track["item"]["artists"]:
    artists += artist["name"] + " "
uri = track["item"]["uri"]
print(artists)
print(song)
print(uri)

if url == None:
    print("No image found")
response = requests.get(url)

file = open("out/track.png", "wb")
file.write(response.content)
file.close()

color = convert_image.getAverageColor("out/track.png")
spotifycode.getSpotifyCode(uri)

convert_image.wordFilter("out/track.png", artists,  background=color)
convert_image.grayscale("out/track.png")
convert_image.blur("out/track.png", radius=10)
convert_image.pixelate("out/track.png", size=3)
convert_image.invert("out/track.png")
convert_image.mirror("out/track.png" )
convert_image.circleCropped("out/track.png")
convert_image.combineImages(["track.png", "track_blurred.png", "track_pixelated.png","track_word.png" ], output="track_combined.png", path="out/", background=color)
# convert_image.attachSpotifyCode("track_combined.png", "code.png", color=color)

# convert_image.getAverageColor("track.png")