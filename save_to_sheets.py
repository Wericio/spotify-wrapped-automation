import gspread
from oauth2client.service_account import ServiceAccountCredentials
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar autenticación con Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("spotify-wrapped-personal-476133760b00.json", scope)
client = gspread.authorize(creds)

# Abrir la hoja de cálculo y la hoja de trabajo principal
spreadsheet = client.open("Spotify Wrapped Personal")
sheet = spreadsheet.worksheet("Sheet1")

# Obtener datos actuales en la hoja
data = sheet.get_all_values()
existing_tracks = [(row[0], row[1], row[2], row[3]) for row in data[1:]]  # (Fecha, Canción, Artista, Álbum)

# Configurar autenticación con Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-read-recently-played"
))

# Obtener las últimas canciones reproducidas en Spotify
recent_tracks = sp.current_user_recently_played(limit=50)

# Formatear los datos obtenidos
new_tracks = []
for item in recent_tracks['items']:
    track = item['track']
    played_at = item['played_at']
    song_name = track['name']
    artist_name = track['artists'][0]['name']
    album_name = track['album']['name']

    # Si la reproducción no está en la hoja, agrégala
    if (played_at, song_name, artist_name, album_name) not in existing_tracks:
        new_tracks.append((played_at, song_name, artist_name, album_name))

if new_tracks:
    # Insertar nuevas canciones en la parte superior de la hoja
    sheet.insert_rows(new_tracks, 2)
    print("✅ Nuevas canciones agregadas correctamente.")
else:
    print("✅ No hay nuevas canciones para agregar.")
