"""
BidInsight CPV Predictor - Flask Web Application (Nowa struktura)
Model: CPVClassifier (Random Forest Classifier)
"""

from app import create_app
from app.models.model_loader import ModelLoader

# Wczytaj model przy starcie
ModelLoader.load()

# Utwórz aplikację
app = create_app()

if __name__ == '__main__':
    if ModelLoader._model_data is None:
        print("❌ Nie można uruchomić aplikacji - brak modelu!")
    else:
        print("🚀 Uruchamianie BidInsight CPV Predictor...")
        print("📱 Model: CPVClassifier v1.0")
        print("🌐 Otwórz przeglądarkę: http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)

