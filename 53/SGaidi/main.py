import sys
import spotipy
import spotipy.util as util

### connect ###

username='SGaidi'

token = util.prompt_for_user_token(
	username=username,
	client_id='3be626cc1d6148f9bc7d96a4fd1caaf0',
	client_secret='d33e28120be349b2b949decd6447d28f',
	scope="user-library-read",
	redirect_uri='http://localhost:8888/callback'
	)
	
if token:
    sp = spotipy.Spotify(auth=token)
else:
    raise RuntimeError("Can't get token for {}".format(username))
	
### search for specific artist ###
# https://github.com/plamere/spotipy/blob/master/examples/artist_albums.py

def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None
		
def show_artist_albums(artist):
    albums = []
    results = sp.artist_albums(artist['id'], album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    seen = set() # to avoid dups
    albums.sort(key=lambda album:album['name'].lower())
    for album in albums:
        name = album['name']
        if name not in seen:
            print((' ' + name))
            seen.add(name)
		
name = raw_input("Specify artist:")
show_artist_albums(get_artist(name))

