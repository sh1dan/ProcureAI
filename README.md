# ProcureAI CPV Predictor

Projekt uniwersytecki - system klasyfikacji zamówień publicznych z wykorzystaniem uczenia maszynowego.

## Opis

ProcureAI to aplikacja webowa do przewidywania kodów CPV (Common Procurement Vocabulary) na podstawie parametrów przetargu. System wykorzystuje model Random Forest do klasyfikacji zamówień publicznych.

## Technologie

- **Backend:** Python, Flask
- **Frontend:** React, Vite
- **ML:** scikit-learn (Random Forest)
- **Model:** 15 kategorii CPV, 40 cech, 1000 rekordów treningowych

## Instalacja

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python run.py
```

Backend działa na: `http://localhost:5000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend działa na: `http://localhost:5173`

## Użycie

### API Endpoint: POST `/api/predict`

```json
{
  "VALUE_EURO": 250000,
  "CAE_NAME": "Urząd Miasta Warszawa",
  "NUTS": "PL911",
  "TYPE_OF_CONTRACT": "SERVICES"
}
```

Odpowiedź zawiera ranking Top 5 kodów CPV z prawdopodobieństwami.

### Przykład w Python

```python
import requests

response = requests.post('http://localhost:5000/api/predict', json={
    "VALUE_EURO": 150000,
    "CAE_NAME": "Szpital Miejski",
    "NUTS": "PL911",
    "TYPE_OF_CONTRACT": "SUPPLIES"
})

print(response.json())
```

## Struktura projektu

```
ProcureAI/
├── backend/          # Flask API + model ML
│   ├── app/         # Aplikacja Flask
│   ├── models/      # Model ML (model.pkl)
│   └── data/        # Dane treningowe
├── frontend/        # React aplikacja
│   └── src/         # Komponenty React
└── README.md
```

## Konfiguracja

Skopiuj `.env.example` do `.env` w folderach `backend/` i `frontend/`, następnie uzupełnij wartości.

## Autorzy

Projekt uniwersytecki - ProcureAI Team

## Licencja

MIT License
