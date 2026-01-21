"""
CPVClassifier Prediction Service
Model: CPVClassifier v1.0
"""

import numpy as np
from pathlib import Path

class CPVPredictor:
    """Serwis do predykcji kodów CPV."""
    
    def __init__(self, model_data):
        """
        Inicjalizacja predyktora.
        
        Parameters:
        -----------
        model_data : dict
            Słownik zawierający model, scaler, label_encoder i listy cech
        """
        self.model = model_data['model']
        self.label_encoder = model_data['label_encoder']
        self.scaler = model_data['scaler']
        self.cae_names = model_data['cae_names']
        self.nuts_codes = model_data['nuts_codes']
        self.contract_types = model_data['contract_types']
        
        # Mapowania dla szybkiego dostępu
        self.cae_map = {name: i for i, name in enumerate(self.cae_names)}
        self.nuts_map = {code: i for i, code in enumerate(self.nuts_codes)}
        self.contract_map = {ct: i for i, ct in enumerate(self.contract_types)}
    
    def prepare_features(self, offer_data):
        """
        Przygotowuje cechy dla oferty.
        
        Parameters:
        -----------
        offer_data : dict
            Dane oferty: VALUE_EURO, CAE_NAME, NUTS, TYPE_OF_CONTRACT
            
        Returns:
        --------
        np.array
            Wektor cech gotowy do predykcji
        """
        # Cecha numeryczna: VALUE_EURO
        value = float(offer_data['VALUE_EURO'])
        
        # Cechy kategoryczne: one-hot encoding
        cae_idx = self.cae_map.get(offer_data['CAE_NAME'], 0)
        nuts_idx = self.nuts_map.get(offer_data['NUTS'], 0)
        contract_idx = self.contract_map.get(offer_data['TYPE_OF_CONTRACT'], 0)
        
        # Tworzenie wektora cech
        features = [value]
        
        # One-hot encoding dla CAE_NAME
        cae_onehot = [0] * len(self.cae_names)
        if cae_idx < len(self.cae_names):
            cae_onehot[cae_idx] = 1
        features.extend(cae_onehot)
        
        # One-hot encoding dla NUTS
        nuts_onehot = [0] * len(self.nuts_codes)
        if nuts_idx < len(self.nuts_codes):
            nuts_onehot[nuts_idx] = 1
        features.extend(nuts_onehot)
        
        # One-hot encoding dla TYPE_OF_CONTRACT
        contract_onehot = [0] * len(self.contract_types)
        if contract_idx < len(self.contract_types):
            contract_onehot[contract_idx] = 1
        features.extend(contract_onehot)
        
        X = np.array(features).reshape(1, -1)
        
        # Normalizacja VALUE_EURO
        X[:, 0:1] = self.scaler.transform(X[:, 0:1])
        
        return X
    
    def predict(self, offer_data, top_n=5):
        """
        Wykonuje predykcję kodu CPV.
        
        Parameters:
        -----------
        offer_data : dict
            Dane oferty
        top_n : int
            Liczba top predykcji do zwrócenia
            
        Returns:
        --------
        dict
            Słownik z predykcją: cpv, confidence, top_n
        """
        # Przygotowanie cech
        X = self.prepare_features(offer_data)
        
        # Predykcja
        y_pred_encoded = self.model.predict(X)[0]
        y_pred = self.label_encoder.inverse_transform([y_pred_encoded])[0]
        
        # Prawdopodobieństwa dla wszystkich klas
        probabilities = self.model.predict_proba(X)[0]
        
        # Top N predykcji
        top_indices = np.argsort(probabilities)[::-1][:top_n]
        top_predictions = [
            {
                'cpv': int(self.label_encoder.inverse_transform([idx])[0]),
                'probability': float(probabilities[idx])
            }
            for idx in top_indices
        ]
        
        # Poziom pewności (maksymalne prawdopodobieństwo)
        confidence = float(probabilities.max())
        
        return {
            'cpv': int(y_pred),
            'confidence': confidence,
            'top5': top_predictions
        }
    
    def get_model_info(self):
        """Zwraca informacje o modelu."""
        cpv_codes = [str(int(c)) for c in self.label_encoder.classes_]
        
        return {
            'model_name': 'CPVClassifier',
            'algorithm': 'Random Forest',
            'version': '1.0',
            'num_categories': len(cpv_codes),
            'num_features': 40,
            'cpv_codes': cpv_codes,
            'cae_names': self.cae_names,
            'nuts_codes': self.nuts_codes,
            'contract_types': self.contract_types
        }

