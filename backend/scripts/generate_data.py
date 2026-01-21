"""
Skrypt do generowania przykładowych danych TED dla projektu BidInsight.

Generuje plik CSV z 1000 wierszami zawierającymi:
- CPV: kody CPV (Common Procurement Vocabulary)
- VALUE_EURO: wartości kontraktów w euro
- CAE_NAME: nazwy zamawiających
- NUTS: kody lokalizacji NUTS
- TYPE_OF_CONTRACT: typy kontraktów
"""

import csv
import random
import math
from pathlib import Path

# Konfiguracja
RANDOM_SEED = 42
NUM_ROWS = 1000
# Ścieżka względna do folderu data
BASE_DIR = Path(__file__).parent.parent
OUTPUT_FILE = BASE_DIR / 'data' / 'ted_sample.csv'

# Ustawienie seeda dla reprodukowalności
random.seed(RANDOM_SEED)

# Przykładowe kody CPV (najczęściej występujące w danych TED)
CPV_CODES = [
    77200000,  # Usługi leśne
    80320000,  # Usługi edukacyjne
    30200000,  # Sprzęt komputerowy
    45200000,  # Roboty budowlane
    48000000,  # Oprogramowanie
    50000000,  # Usługi naprawcze
    60000000,  # Transport
    70000000,  # Usługi architektoniczne
    71000000,  # Usługi architektoniczne, inżynierskie
    72000000,  # Usługi IT
    73000000,  # Usługi badawcze
    75000000,  # Usługi administracyjne
    79000000,  # Usługi biznesowe
    80000000,  # Usługi edukacyjne i szkoleniowe
    85000000,  # Usługi zdrowotne i społeczne
]

# Przykładowe nazwy zamawiających (polskie instytucje)
CAE_NAMES = [
    'Urząd Miasta Warszawa',
    'Gmina Kraków',
    'Urząd Marszałkowski Województwa Mazowieckiego',
    'Gmina Wrocław',
    'Urząd Miasta Poznań',
    'Gmina Gdańsk',
    'Urząd Miasta Łódź',
    'Gmina Katowice',
    'Urząd Miasta Lublin',
    'Gmina Białystok',
    'Urząd Miasta Szczecin',
    'Gmina Bydgoszcz',
    'Urząd Miasta Rzeszów',
    'Gmina Toruń',
    'Urząd Miasta Olsztyn',
    'Gmina Zielona Góra',
    'Urząd Miasta Opole',
    'Gmina Kielce',
    'Urząd Miasta Radom',
    'Gmina Sosnowiec',
]

# Przykładowe kody NUTS (polskie regiony)
NUTS_CODES = [
    'PL911',  # Warszawa
    'PL213',  # Kraków
    'PL127',  # Wrocław
    'PL224',  # Poznań
    'PL633',  # Gdańsk
    'PL113',  # Łódź
    'PL228',  # Katowice
    'PL314',  # Lublin
    'PL343',  # Białystok
    'PL424',  # Szczecin
    'PL613',  # Bydgoszcz
    'PL323',  # Rzeszów
    'PL616',  # Toruń
    'PL628',  # Olsztyn
    'PL432',  # Zielona Góra
    'PL516',  # Opole
    'PL326',  # Kielce
    'PL127',  # Radom
    'PL228',  # Sosnowiec
]

# Typy kontraktów
CONTRACT_TYPES = [
    'SERVICES',
    'SUPPLIES',
    'WORKS',
]

def generate_lognormal(mean, sigma):
    """Generuje wartość z rozkładu log-normalnego."""
    normal_value = random.gauss(mean, sigma)
    return round(abs(math.exp(normal_value)), 2)

# Tworzenie folderu jeśli nie istnieje
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Generowanie danych
print(f"Generowanie {NUM_ROWS} wierszy danych...")

with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['CPV', 'VALUE_EURO', 'CAE_NAME', 'NUTS', 'TYPE_OF_CONTRACT']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for _ in range(NUM_ROWS):
        writer.writerow({
            'CPV': random.choice(CPV_CODES),
            'VALUE_EURO': generate_lognormal(10, 1.5),
            'CAE_NAME': random.choice(CAE_NAMES),
            'NUTS': random.choice(NUTS_CODES),
            'TYPE_OF_CONTRACT': random.choice(CONTRACT_TYPES),
        })

print(f"Wygenerowano plik: {OUTPUT_FILE}")
print(f"Liczba wierszy: {NUM_ROWS}")
print(f"Liczba kolumn: {len(fieldnames)}")

