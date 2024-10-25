import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

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
lawnmower = 'spotify:track:0ABtPTOutryfKhLRASnNNX'

def lambda_handler(event, context):
    devices = sp.devices()
    if not devices:
        logger.info("No active devices found.")
        return
    
    for device in devices['devices']:
        logger.info(f"Found device {device["name"]}")
        device_id = device['id']
        try:
            logger.info("Fixing your Spotify Wrapped...")
            
            logger.info("Turning volume to 0...")
            sp.volume(0, device_id=device_id)

            logger.info("Starting playback...")
            sp.start_playback(device_id=device_id, uris=[lawnmower])
            
            logger.info("Turning repeat on...")
            sp.repeat(state='track', device_id=device_id)
            logger.info("Done!")

        except Exception as e:
            logger.info(f"Error: {e}")
