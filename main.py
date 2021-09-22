from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = "077cbc4a62834b4db155ecd4ebea9907"

client_secret = "915b68abe03a4ac79b5ac5e34bf835a4"

date = input("Enter the date you want to travel back in yyyy-mm-dd format : ")

# params = {
#     "client_id": client_id,
#     "client_secret": client_secret,
#     "redirect_uri": "http://example.com",
#     "scope": "playlist-modify-private"
# }

url = "https://www.billboard.com/charts/hot-100/" + date

response = requests.get(url)
browser = response.text

soup = BeautifulSoup(browser, "html.parser")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt",
    )
)




span_tags = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
# # print(span_tags)
#
#
# print(song_titles)

song_titles = []
for tag in span_tags:
    text = tag.getText()
    song_titles.append(text)

# <span class="chart-element__information__song text--truncate color--primary">What's Luv?</span>

user_id = sp.current_user()['id']

# print(user_id)


song_uris = []
year = date.split("-")[0]
for song in song_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

print(song_uris)

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)