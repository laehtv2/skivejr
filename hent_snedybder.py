import requests
from bs4 import BeautifulSoup
import csv
import datetime
import time

# Liste over lande, vi vil hente fra (navnet skal matche URL-strukturen på skisport.dk)
lande = ['italien', 'oestrig', 'frankrig', 'norge', 'sverige']

# Filnavn til output
output_file = 'snedybder.csv'

# Vi forbereder listen med data og tilføjer headers
csv_data = [['Dato', 'Land', 'Destination', 'Dal (cm)', 'Top (cm)']]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for land in lande:
    url = f"https://www.skisport.dk/snevejr/{land}/"
    print(f"Henter data fra {land}...")
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Tjekker om siden blev hentet korrekt
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Vi leder efter tabellen. På skisport.dk er det ofte en simpel tabel struktur.
        # Vi finder alle rækker (tr) i tabellerne.
        rows = soup.find_all('tr')
        
        for row in rows:
            cols = row.find_all('td')
            
            # Vi tjekker om rækken har nok kolonner (Navn, Dal, Top, Webcam...)
            # Typisk er der 4-5 kolonner.
            if len(cols) >= 3:
                dest_name = cols[0].get_text(strip=True)
                dal_sne = cols[1].get_text(strip=True)
                top_sne = cols[2].get_text(strip=True)
                
                # Simpel validering: Tjek om 'dal_sne' faktisk er et tal (eller tomt)
                # Dette sorterer overskrifter og reklamer fra
                if dal_sne.isdigit() or dal_sne == "" or top_sne.isdigit():
                    # Vi renser data (hvis der står tekst)
                    # Her gemmer vi bare rå tallene
                    today = datetime.date.today()
                    csv_data.append([today, land, dest_name, dal_sne, top_sne])
                    
        # Vent lidt for ikke at overbelaste serveren (god skik)
        time.sleep(1)

    except Exception as e:
        print(f"Fejl ved hentning af {land}: {e}")

# Gem til CSV fil
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(csv_data)

print(f"Færdig! Data gemt i {output_file}")
