import imp
from urllib.parse import quote_plus
import requests
baseUrl = "https://www.spotifycodes.com/downloadCode.php?uri="


path = "jpeg/000000/white/640/"


def getSpotifyCode(uri):
    url = baseUrl + quote_plus(path + uri)
    print(url)
    response = requests.get(url)
    file = open("code.png", "wb")
    file.write(response.content)
    file.close()
    return "code.png"