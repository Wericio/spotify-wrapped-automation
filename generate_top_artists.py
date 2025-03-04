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

# Diccionario para contar reproducciones por artista
artist_count = defaultdict(int)

for row in data:
    if len(row) < 3:  # Si la fila está vacía o incompleta, saltarla
        continue
    artist = row[2]  # Columna de artista
    artist_count[artist] += 1

# Ordenar por número de reproducciones
sorted_artists = sorted(artist_count.items(), key=lambda x: x[1], reverse=True)

# Preparar datos para escribir en "Top Artists"
top_artists_data = [["Artista", "Reproducciones"]]
top_artists_data += [[artist, count] for artist, count in sorted_artists]

# Crear o abrir la hoja "Top Artists"
try:
    top_artists_sheet = spreadsheet.worksheet("Top Artists")
except gspread.exceptions.WorksheetNotFound:
    top_artists_sheet = spreadsheet.add_worksheet(title="Top Artists", rows="1000", cols="2")

# Limpiar la hoja y actualizar con los datos
top_artists_sheet.clear()
top_artists_sheet.update("A1", top_artists_data)

print("✅ Top Artists actualizado correctamente.")
