import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configurar autenticación con Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-read-recently-played"
))

# Obtener las últimas canciones reproducidas
recent_tracks = sp.current_user_recently_played(limit=10)

# Mostrar resultados
for idx, item in enumerate(recent_tracks['items']):
    track = item['track']
    print(f"{idx + 1}. {track['name']} - {track['artists'][0]['name']}")
