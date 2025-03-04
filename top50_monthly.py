import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-top-read playlist-modify-public playlist-modify-private"
))

# Nombre de la playlist personalizada
PLAYLIST_NAME = "Top 50 del Mes"

# 1️⃣ Buscar si la playlist ya existe
def get_playlist_id(name):
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        if playlist['name'] == name:
            return playlist['id']
    return None

playlist_id = get_playlist_id(PLAYLIST_NAME)

# 2️⃣ Si no existe, crearla
if not playlist_id:
    print(f"🔹 La playlist '{PLAYLIST_NAME}' no existe. Creando nueva...")
    playlist = sp.user_playlist_create(sp.me()['id'], PLAYLIST_NAME, public=True)
    playlist_id = playlist['id']
else:
    print(f"✅ La playlist '{PLAYLIST_NAME}' ya existe. Se actualizará.")

# 3️⃣ Obtener las canciones más escuchadas y añadirlas a la playlist
top_tracks = sp.current_user_top_tracks(limit=50, time_range="medium_term")  # Últimos 6 meses
track_uris = [track['uri'] for track in top_tracks['items']]

if track_uris:
    sp.user_playlist_replace_tracks(sp.me()['id'], playlist_id, track_uris)
    print("🎶 Playlist actualizada con tus canciones favoritas.")
else:
    print("⚠️ No se encontraron canciones para actualizar la playlist.")
