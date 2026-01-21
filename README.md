# ProcureAI CPV Predictor

<div align="center">

**AI-powered public procurement classification system**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-18.2+-61dafb.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## 📋 Описание / Description

**PL:** ProcureAI to system klasyfikacji zamówień publicznych wspierany sztuczną inteligencją. Aplikacja wykorzystuje model uczenia maszynowego (Random Forest) do przewidywania kodów CPV (Common Procurement Vocabulary) na podstawie parametrów przetargu.

**EN:** ProcureAI is an AI-powered public procurement classification system. The application uses a machine learning model (Random Forest) to predict CPV (Common Procurement Vocabulary) codes based on tender parameters.

### ✨ Funkcje / Features

- 🤖 **Predykcja kodów CPV** - Automatyczna klasyfikacja zamówień publicznych
- 📊 **Ranking Top 5** - Pięć najbardziej prawdopodobnych kodów z poziomem pewności
- 🎯 **Interfejs webowy** - Nowoczesny UI w React z obsługą wielu języków (PL/EN)
- 🔌 **REST API** - Gotowe API do integracji z innymi systemami
- ⚡ **Szybka predykcja** - Model wczytany w pamięci dla natychmiastowych wyników

## 🏗️ Architektura / Architecture

```
ProcureAI/
├── backend/          # Flask API + ML Model
│   ├── app/          # Aplikacja Flask
│   ├── models/       # Wytrenowany model ML
│   ├── data/         # Dane treningowe
│   └── requirements.txt
├── frontend/         # React + Vite
│   ├── src/          # Komponenty React
│   └── package.json
└── README.md
```

## 🚀 Instalacja / Installation

### Wymagania / Requirements

- Python 3.8+
- Node.js 16+
- npm lub yarn

### Backend Setup

```bash
# Przejdź do katalogu backend
cd backend

# Utwórz wirtualne środowisko
python -m venv venv

# Aktywuj środowisko
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Zainstaluj zależności
pip install -r requirements.txt

# Skonfiguruj zmienne środowiskowe
cp .env.example .env
# Edytuj .env i ustaw SECRET_KEY oraz inne zmienne

# Uruchom serwer
python run.py
```

Backend będzie dostępny pod adresem: `http://localhost:5000`

### Frontend Setup

```bash
# Przejdź do katalogu frontend
cd frontend

# Zainstaluj zależności
npm install

# Skonfiguruj zmienne środowiskowe
cp .env.example .env
# Edytuj .env i ustaw VITE_API_BASE jeśli backend działa na innym porcie

# Uruchom serwer deweloperski
npm run dev
```

Frontend będzie dostępny pod adresem: `http://localhost:5173`

### Build dla produkcji / Production Build

```bash
# Backend - użyj gunicorn lub podobnego serwera WSGI
gunicorn -w 4 -b 0.0.0.0:5000 app_flask:app

# Frontend
cd frontend
npm run build
# Pliki będą w folderze dist/
```

## 📖 Użycie / Usage

### API Endpoints

#### POST `/api/predict`

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
```json
{
  "success": true,
  "result": {
    "predictions": [
      {
        "cpv_code": "72000000",
        "probability": 0.85,
        "rank": 1
      },
      ...
    ],
    "top_prediction": {
      "cpv_code": "72000000",
      "probability": 0.85
    }
  }
}
```

#### GET `/api/model-info`

Zwraca informacje o modelu.

**Response:**
```json
{
  "model_name": "CPVClassifier",
  "version": "1.0",
  "algorithm": "Random Forest",
  "categories": 15,
  "features": 40
}
```

### Przykład użycia w Python / Python Example

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

### Przykład użycia w JavaScript / JavaScript Example

```javascript
const response = await fetch('http://localhost:5000/api/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
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

## 🔧 Konfiguracja / Configuration

### Zmienne środowiskowe Backend

Zobacz `backend/.env.example`:

- `SECRET_KEY` - Klucz sekretny Flask (wymagany w produkcji)
- `FLASK_DEBUG` - Tryb debugowania (True/False)
- `HOST` - Host serwera (domyślnie: 0.0.0.0)
- `PORT` - Port serwera (domyślnie: 5000)
- `CORS_ORIGINS` - Dozwolone źródła CORS (oddzielone przecinkami)

### Zmienne środowiskowe Frontend

Zobacz `frontend/.env.example`:

- `VITE_API_BASE` - URL backend API (domyślnie: http://localhost:5000/api)
- `VITE_ENV` - Środowisko (development/production)

## 🧪 Model Machine Learning

- **Algorytm:** Random Forest Classifier
- **Kategorie CPV:** 15
- **Cechy:** 40
- **Dane treningowe:** 1000 rekordów (syntetyczne)
- **Wersja modelu:** 1.0

Model został wytrenowany na danych syntetycznych i może być dostosowany do rzeczywistych danych z systemów zamówień publicznych.

## 📁 Struktura projektu / Project Structure

```
backend/
├── app/
│   ├── __init__.py          # Factory aplikacji Flask
│   ├── api/
│   │   └── routes.py        # Endpointy API
│   ├── main/
│   │   └── routes.py        # Route'y główne
│   ├── models/
│   │   └── model_loader.py  # Ładowanie modelu ML
│   └── services/
│       └── predictor.py     # Serwis predykcji
├── models/
│   ├── model.pkl            # Wytrenowany model
│   └── metrics.txt          # Metryki modelu
├── data/
│   └── ted_sample.csv       # Przykładowe dane
├── config.py                # Konfiguracja
├── app_flask.py             # Główna aplikacja Flask
└── run.py                   # Entry point

frontend/
├── src/
│   ├── App.jsx              # Główny komponent
│   ├── main.jsx             # Entry point React
│   └── styles.css           # Style
├── public/
│   └── cpv.json             # Dane kodów CPV
├── index.html
└── vite.config.js
```

## 🤝 Wsparcie / Contributing

Zobacz [CONTRIBUTING.md](CONTRIBUTING.md) aby dowiedzieć się, jak możesz przyczynić się do rozwoju projektu.

## 📝 Licencja / License

Ten projekt jest dostępny na licencji MIT. Zobacz [LICENSE](LICENSE) aby uzyskać więcej informacji.

## 👥 Autorzy / Authors

ProcureAI Team

## 🙏 Podziękowania / Acknowledgments

- Flask i React za świetne frameworki
- scikit-learn za narzędzia ML
- Wszystkim kontrybutorom projektu

## 📞 Kontakt / Contact

W razie pytań lub problemów, utwórz [issue](https://github.com/yourusername/ProcureAI/issues) w repozytorium.

---

<div align="center">
Made with ❤️ by ProcureAI Team
</div>

