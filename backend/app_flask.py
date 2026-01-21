"""
ProcureAI CPV Predictor - Flask Web Application
Model: CPVClassifier (Random Forest Classifier)
Interfejs do predykcji kodów CPV dla ofert przetargowych
"""

from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
from pathlib import Path
import os
from flask_cors import CORS

app = Flask(__name__)

# CORS configuration for production
cors_origins = os.getenv('CORS_ORIGINS', '*').split(',')
CORS(app, origins=cors_origins, supports_credentials=True)

# Ścieżki
BASE_DIR = Path(__file__).parent
MODEL_PATH = BASE_DIR / 'models' / 'model.pkl'

# Globalna zmienna dla modelu (wczytywana raz przy starcie)
model_data = None

def load_model():
    """Wczytuje wytrenowany model."""
    global model_data
    if model_data is None:
        try:
            with open(MODEL_PATH, 'rb') as f:
                data = pickle.load(f)
            
            model_data = {
                'model': data['model'],
                'label_encoder': data['label_encoder'],
                'scaler': data['scaler'],
                'cae_names': data['cae_names'],
                'nuts_codes': data['nuts_codes'],
                'contract_types': data['contract_types']
            }
            print("✅ Model wczytany pomyślnie!")
        except Exception as e:
            print(f"❌ Błąd podczas wczytywania modelu: {e}")
            model_data = None
    return model_data

def prepare_features(offer_data, scaler, cae_names, nuts_codes, contract_types):
    """Przygotowuje cechy dla oferty."""
    # Mapowanie do indeksów
    cae_map = {name: i for i, name in enumerate(cae_names)}
    nuts_map = {code: i for i, code in enumerate(nuts_codes)}
    contract_map = {ct: i for i, ct in enumerate(contract_types)}
    
    # Cecha numeryczna: VALUE_EURO
    value = float(offer_data['VALUE_EURO'])
    
    # Cechy kategoryczne: one-hot encoding
    cae_idx = cae_map.get(offer_data['CAE_NAME'], 0)
    nuts_idx = nuts_map.get(offer_data['NUTS'], 0)
    contract_idx = contract_map.get(offer_data['TYPE_OF_CONTRACT'], 0)
    
    # Tworzenie wektora cech
    features = [value]
    
    # One-hot encoding dla CAE_NAME
    cae_onehot = [0] * len(cae_names)
    if cae_idx < len(cae_names):
        cae_onehot[cae_idx] = 1
    features.extend(cae_onehot)
    
    # One-hot encoding dla NUTS
    nuts_onehot = [0] * len(nuts_codes)
    if nuts_idx < len(nuts_codes):
        nuts_onehot[nuts_idx] = 1
    features.extend(nuts_onehot)
    
    # One-hot encoding dla TYPE_OF_CONTRACT
    contract_onehot = [0] * len(contract_types)
    if contract_idx < len(contract_types):
        contract_onehot[contract_idx] = 1
    features.extend(contract_onehot)
    
    X = np.array(features).reshape(1, -1)
    
    # Normalizacja VALUE_EURO
    X[:, 0:1] = scaler.transform(X[:, 0:1])
    
    return X

def predict_cpv(offer_data):
    """Wykonuje predykcję kodu CPV."""
    model = model_data['model']
    label_encoder = model_data['label_encoder']
    scaler = model_data['scaler']
    cae_names = model_data['cae_names']
    nuts_codes = model_data['nuts_codes']
    contract_types = model_data['contract_types']
    
    # Przygotowanie cech
    X = prepare_features(offer_data, scaler, cae_names, nuts_codes, contract_types)
    
    # Predykcja
    y_pred_encoded = model.predict(X)[0]
    y_pred = label_encoder.inverse_transform([y_pred_encoded])[0]
    
    # Prawdopodobieństwa dla wszystkich klas
    probabilities = model.predict_proba(X)[0]
    
    # Top 5 predykcji
    top5_indices = np.argsort(probabilities)[::-1][:5]
    top5 = [
        {
            'cpv': int(label_encoder.inverse_transform([idx])[0]),
            'probability': float(probabilities[idx])
        }
        for idx in top5_indices
    ]
    
    # Poziom pewności (maksymalne prawdopodobieństwo)
    confidence = float(probabilities.max())
    
    return {
        'cpv': int(y_pred),
        'confidence': confidence,
        'top5': top5
    }

@app.route('/')
def index():
    """Prosty endpoint informacyjny dla backendu API."""
    return jsonify({
        'service': 'ProcureAI CPV Predictor API',
        'model': 'CPVClassifier v1.0',
        'endpoints': {
            'predict': '/api/predict',
            'model_info': '/api/model-info'
        }
    })

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint do predykcji."""
    try:
        data = request.get_json()
        
        # Walidacja danych
        required_fields = ['VALUE_EURO', 'CAE_NAME', 'NUTS', 'TYPE_OF_CONTRACT']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Brakuje pola: {field}'}), 400
        
        # Predykcja
        result = predict_cpv(data)
        
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/model-info', methods=['GET'])
def api_model_info():
    """API endpoint z informacjami o modelu."""
    if model_data is None:
        return jsonify({'error': 'Model nie został wczytany'}), 500
    
    cpv_codes = [str(int(c)) for c in model_data['label_encoder'].classes_]
    
    return jsonify({
        'model_name': 'CPVClassifier',
        'algorithm': 'Random Forest',
        'version': '1.0',
        'num_categories': len(cpv_codes),
        'num_features': 40,
        'cpv_codes': cpv_codes,
        'cae_names': model_data['cae_names'],
        'nuts_codes': model_data['nuts_codes'],
        'contract_types': model_data['contract_types']
    })

# Wczytaj model przy imporcie modułu
load_model()

if __name__ == '__main__':
    if model_data is None:
        print("❌ Nie można uruchomić aplikacji - brak modelu!")
    else:
        print("🚀 Uruchamianie ProcureAI CPV Predictor...")
        print("📱 Model: CPVClassifier v1.0")
        print("🌐 Otwórz przeglądarkę: http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)

