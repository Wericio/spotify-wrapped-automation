import os
import gspread
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Autenticación con Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-read-recently-played"
))

# Conectar con Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("spotify-wrapped-personal-476133760b00.json", scope)
gc = gspread.authorize(credentials)

# Abrir la hoja de cálculo
sheet = gc.open_by_key("1MqjxBBqDmeUS-1U_lJHYopsj6FmNg4rI13gliS2Uzso").sheet1  # Usa el ID de la hoja de cálculo

# Obtener las últimas 10 canciones reproducidas
recent_tracks = sp.current_user_recently_played(limit=10)

# Formatear los datos para Google Sheets
data = [["Fecha", "Canción", "Artista", "Álbum"]]
for item in recent_tracks["items"]:
    track = item["track"]
    data.append([
        item["played_at"],  # Fecha y hora de reproducción
        track["name"],  # Nombre de la canción
        track["artists"][0]["name"],  # Nombre del artista
        track["album"]["name"]  # Nombre del álbum
    ])

# Guardar en Google Sheets (sobreescribe desde la fila 1)
sheet.clear()
sheet.append_rows(data)

print("✅ Datos guardados en Google Sheets correctamente.")