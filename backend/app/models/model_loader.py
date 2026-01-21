"""
Model Loader - wczytuje i zarządza modelem CPVClassifier
"""

import pickle
from pathlib import Path
from flask import current_app

class ModelLoader:
    """Klasa do ładowania modelu."""
    
    _model_data = None
    
    @classmethod
    def load(cls):
        """
        Wczytuje wytrenowany model.
        
        Returns:
        --------
        dict lub None
            Słownik z danymi modelu lub None jeśli błąd
        """
        if cls._model_data is None:
            try:
                # Użyj ścieżki z konfiguracji jeśli dostępna
                try:
                    from flask import has_app_context
                    if has_app_context():
                        model_path = current_app.config.get('MODEL_PATH')
                    else:
                        raise RuntimeError("No app context")
                except (RuntimeError, ImportError):
                    # Fallback dla bezpośredniego użycia
                    BASE_DIR = Path(__file__).parent.parent.parent
                    model_path = BASE_DIR / 'models' / 'model.pkl'
                
                with open(model_path, 'rb') as f:
                    data = pickle.load(f)
                
                cls._model_data = {
                    'model': data['model'],
                    'label_encoder': data['label_encoder'],
                    'scaler': data['scaler'],
                    'cae_names': data['cae_names'],
                    'nuts_codes': data['nuts_codes'],
                    'contract_types': data['contract_types']
                }
                print("✅ Model CPVClassifier wczytany pomyślnie!")
            except Exception as e:
                print(f"❌ Błąd podczas wczytywania modelu: {e}")
                cls._model_data = None
        
        return cls._model_data
    
    @classmethod
    def reload(cls):
        """Przeładowuje model."""
        cls._model_data = None
        return cls.load()

