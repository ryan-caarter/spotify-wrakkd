import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from datetime import datetime
import pytz

client_id = os.environ["SPOTIFY_CLIENT_ID"]  
client_secret = os.environ["SPOTIFY_CLIENT_SECRET"]
redirect_uri = os.environ["SPOTIFY_REDIRECT_URI"]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    open_browser=False,
    scope="user-modify-playback-state,user-read-playback-state"
))

ywf = 'spotify:track:5HQVUIKwCEXpe7JIHyY734'
track_uri = 'spotify:track:0ABtPTOutryfKhLRASnNNX'

def lambda_handler(event, context):
    devices = sp.devices()
    for device in devices['devices']:
        try:
            nzt_timezone = pytz.timezone("Pacific/Auckland")
            current_time_nzt = datetime.now(nzt_timezone)

            if current_time_nzt.hour > 5 and current_time_nzt.hour < 22:
                sp.volume(100, device_id=device['id'])
                print(f"Volume set to {100}% on device '{device['name']}'")
                # sp.add_to_queue(ywf, device_id=device['id'])
            
                sp.pause_playback(device_id=device['id'])
                sp.repeat(state='off', device_id=device['id'])
                print(f"Pausing device {device['name']}")
            else:
                sp.volume(0, device_id=device['id'])
                print(f"Volume set to {0}% on device '{device['name']}'")
                # sp.add_to_queue(ywf, device_id=device['id'])
            
                sp.start_playback(device_id=device['id'], uris=[track_uri])
                sp.repeat(state='track', device_id=device['id'])
                print(f"Playing track {track_uri} on device {device['name']}")
        except Exception as e:
            print(f"Error setting volume: {e}")
        print(device['name'])


print("No active devices found.") 

