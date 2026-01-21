"""
API Routes dla predykcji CPV
"""

from app.api import bp
from flask import request, jsonify
from app.services.predictor import CPVPredictor
from app.models.model_loader import ModelLoader

# Globalna instancja predyktora
predictor = None

def init_predictor():
    """Inicjalizuje predyktor przy starcie aplikacji."""
    global predictor
    if predictor is None:
        model_data = ModelLoader.load()
        if model_data:
            predictor = CPVPredictor(model_data)
    return predictor

@bp.route('/predict', methods=['POST'])
def api_predict():
    """API endpoint do predykcji."""
    global predictor
    
    if predictor is None:
        predictor = init_predictor()
    
    if predictor is None:
        return jsonify({'error': 'Model nie został wczytany'}), 500
    
    try:
        data = request.get_json()
        
        # Walidacja danych
        required_fields = ['VALUE_EURO', 'CAE_NAME', 'NUTS', 'TYPE_OF_CONTRACT']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Brakuje pola: {field}'}), 400
        
        # Predykcja
        result = predictor.predict(data)
        
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/model-info', methods=['GET'])
def api_model_info():
    """API endpoint z informacjami o modelu."""
    global predictor
    
    if predictor is None:
        predictor = init_predictor()
    
    if predictor is None:
        return jsonify({'error': 'Model nie został wczytany'}), 500
    
    return jsonify(predictor.get_model_info())

