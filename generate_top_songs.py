import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import defaultdict

# Autenticación con Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("spotify-wrapped-personal-476133760b00.json", scope)
client = gspread.authorize(creds)

# Abrir la hoja de cálculo y cargar Sheet1
spreadsheet = client.open("Spotify Wrapped Personal")
sheet1 = spreadsheet.worksheet("Sheet1")

# Obtener datos actuales de Sheet1
data = sheet1.get_all_values()[1:]  # Ignorar la primera fila (encabezados)

# Diccionario para contar reproducciones
song_count = defaultdict(int)

for row in data:
    if len(row) < 4:  # Si la fila está vacía o incompleta, saltarla
        continue
    song, artist, album = row[1], row[2], row[3]
    song_count[(song, artist, album)] += 1

# Ordenar por número de reproducciones
sorted_songs = sorted(song_count.items(), key=lambda x: x[1], reverse=True)

# Preparar datos para escribir en Top Songs
top_songs_data = [["Canción", "Artista", "Álbum", "Reproducciones"]]
top_songs_data += [[song, artist, album, count] for (song, artist, album), count in sorted_songs]

# Crear o abrir la hoja Top Songs
try:
    top_songs_sheet = spreadsheet.worksheet("Top Songs")
except gspread.exceptions.WorksheetNotFound:
    top_songs_sheet = spreadsheet.add_worksheet(title="Top Songs", rows="1000", cols="4")

# Limpiar la hoja y actualizar con los datos
top_songs_sheet.clear()
top_songs_sheet.update("A1", top_songs_data)

print("✅ Top Songs actualizado correctamente.")
