# 🤖 ProcureAI CPV Predictor

> Projekt uniwersytecki - system klasyfikacji zamówień publicznych z wykorzystaniem uczenia maszynowego

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18.2+-61dafb.svg)](https://reactjs.org/)

---

## 📋 Opis

ProcureAI to aplikacja webowa do przewidywania kodów **CPV** (Common Procurement Vocabulary) na podstawie parametrów przetargu. System wykorzystuje model **Random Forest** do automatycznej klasyfikacji zamówień publicznych.

### ✨ Funkcje

- 🎯 **Predykcja kodów CPV** - Automatyczna klasyfikacja na podstawie parametrów przetargu
- 📊 **Ranking Top 5** - Pięć najbardziej prawdopodobnych kodów z poziomem pewności
- 🌐 **Interfejs webowy** - Nowoczesny UI w React z obsługą wielu języków
- 🔌 **REST API** - Gotowe API do integracji

---

## 🛠️ Technologie

| Kategoria | Technologie |
|-----------|------------|
| **Backend** | Python 3.8+, Flask 3.0+ |
| **Frontend** | React 18.2+, Vite 5.0+ |
| **Machine Learning** | scikit-learn (Random Forest) |
| **Model** | 15 kategorii CPV, 40 cech, 1000 rekordów treningowych |

---

## 🚀 Instalacja

### Wymagania

- Python 3.8+
- Node.js 16+
- npm lub yarn

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python run.py
```

Backend będzie dostępny pod adresem: `http://localhost:5000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend będzie dostępny pod adresem: `http://localhost:5173`

---

## 📖 Użycie

### API Endpoint: `POST /api/predict`

Przewiduje kod CPV na podstawie parametrów przetargu.

**Request:**
```json
{
  "VALUE_EURO": 250000,
  "CAE_NAME": "Urząd Miasta Warszawa",
  "NUTS": "PL911",
  "TYPE_OF_CONTRACT": "SERVICES"
}
```

**Response:**
Odpowiedź zawiera ranking Top 5 kodów CPV z prawdopodobieństwami.

### Przykład w Python

```python
import requests

url = "http://localhost:5000/api/predict"
data = {
    "VALUE_EURO": 150000,
    "CAE_NAME": "Szpital Miejski",
    "NUTS": "PL911",
    "TYPE_OF_CONTRACT": "SUPPLIES"
}

response = requests.post(url, json=data)
result = response.json()
print(result)
```

### Przykład w JavaScript

```javascript
const response = await fetch('http://localhost:5000/api/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    VALUE_EURO: 500000,
    CAE_NAME: 'Urząd Miasta',
    NUTS: 'PL911',
    TYPE_OF_CONTRACT: 'WORKS'
  })
});

const result = await response.json();
console.log(result);
```

---

## 📁 Struktura projektu

```
ProcureAI/
├── backend/              # Flask API + model ML
│   ├── app/             # Aplikacja Flask
│   │   ├── api/         # Endpointy API
│   │   ├── models/      # Ładowanie modelu ML
│   │   └── services/    # Serwis predykcji
│   ├── models/          # Model ML (model.pkl)
│   ├── data/            # Dane treningowe
│   └── requirements.txt
├── frontend/            # React aplikacja
│   ├── src/             # Komponenty React
│   └── package.json
└── README.md
```

---

## ⚙️ Konfiguracja

1. Skopiuj `.env.example` do `.env` w folderach `backend/` i `frontend/`
2. Uzupełnij wartości w plikach `.env`:
   - **Backend:** `SECRET_KEY`, `FLASK_DEBUG`, `PORT`
   - **Frontend:** `VITE_API_BASE`

---

## 🧪 Model Machine Learning

- **Algorytm:** Random Forest Classifier
- **Kategorie CPV:** 15
- **Cechy wejściowe:** 40
- **Dane treningowe:** 1000 rekordów (syntetyczne)
- **Wersja:** 1.0

---

## 👥 Autorzy

Projekt uniwersytecki - **ProcureAI Team**

---

## 📝 Licencja

Ten projekt jest dostępny na licencji [MIT](LICENSE).

---

<div align="center">
Made with ❤️ for university project
</div>
