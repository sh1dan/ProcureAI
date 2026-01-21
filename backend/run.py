"""
Entry point dla aplikacji ProcureAI CPV Predictor
Model: CPVClassifier v1.0
"""

import os
from app_flask import app

if __name__ == '__main__':
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    
    print("🚀 Uruchamianie ProcureAI CPV Predictor...")
    print("📱 Model: CPVClassifier v1.0")
    print(f"🌐 Otwórz przeglądarkę: http://{host}:{port}")
    print(f"🔧 Debug mode: {debug}")
    
    app.run(debug=debug, host=host, port=port)

