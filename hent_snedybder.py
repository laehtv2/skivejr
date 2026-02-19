import requests
from bs4 import BeautifulSoup
import csv
import datetime
import time

# Liste over lande og de specifikke destinationer vi leder efter
lande = ['italien', 'oestrig', 'frankrig', 'norge', 'sverige']
mine_favoritter = ['Avoriaz', 'Livigno', 'Wagrain', 'Hemsedal', 'Trysil', 'Sälen']

# Filnavne
output_file_all = 'snedybder.csv'
output_file_fav = 'snedybder_udvalgte.csv'

# Vi forbereder lister med data
csv_all = [['Dato', 'Land', 'Destination', 'Dal (cm)', 'Top (cm)']]
csv_fav = [['Dato', 'Land', 'Destination', 'Dal (cm)', 'Top (cm)']]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for land in lande:
    url = f"https://www.skisport.dk/snevejr/{land}/"
    print(f"Henter data fra {land}...")
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all('tr')
        
        for row in rows:
            cols = row.find_all('td')
            
            if len(cols) >= 3:
                dest_name = cols[0].get_text(strip=True)
                dal_sne = cols[1].get_text(strip=True)
                top_sne = cols[2].get_text(strip=True)
                
                # Validering
                if dal_sne.isdigit() or top_sne.isdigit():
                    today = datetime.date.today()
                    row_data = [today, land, dest_name, dal_sne, top_sne]
                    
                    # Tilføj til den store liste
                    csv_all.append(row_data)
                    
                    # Tjek om denne destination er i din favoritliste
                    if dest_name in mine_favoritter:
                        csv_fav.append(row_data)
                        
        time.sleep(1)

    except Exception as e:
        print(f"Fejl ved hentning af {land}: {e}")

# Gem alle destinationer
with open(output_file_all, 'w', newline='', encoding='utf-8') as f:
    csv.writer(f).writerows(csv_all)

# Gem kun de valgte favoritter
with open(output_file_fav, 'w', newline='', encoding='utf-8') as f:
    csv.writer(f).writerows(csv_fav)

print(f"Færdig! Alle data gemt i {output_file_all}, og dine favoritter i {output_file_fav}")
