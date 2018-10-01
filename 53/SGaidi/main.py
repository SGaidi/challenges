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
        raise ValueError("This artist does not exist in Spotify: {}".format(name))
		
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

def get_playlist(user="spotify", playlist_name="This is: Deep Purple"):
	user_results = sp.user_playlists(user=user)
	items = user_results['items']
	playlist_results = []
	for item in items:
		if item['name'] == playlist_name:
			playlist_results.append(item)
	if len(playlist_results) > 0:
		return playlist_results[0]
	else:
		raise ValueError("User ({}) does not have playlist ({})".format(user, playlist_name))
		
def show_tracks(tracks):
	for i, item in enumerate(tracks['items']):
		track = item['track']
		print "   %d %32.32s %s" % (i, track['artists'][0]['name'], track['name'])
		
def get_tracks(playlist):
	#return playlist['tracks']
	return sp.user_playlist(username, playlist['id'], fields="tracks")['tracks']
		
name = raw_input("Specify artist:")
show_artist_albums(get_artist(name))

playlist_name = raw_input("Specify playlist:")
playlist = get_playlist(playlist_name=playlist_name)
show_tracks(get_tracks(playlist))


