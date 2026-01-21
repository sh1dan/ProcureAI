"""
ProcureAI CPV Predictor - Flask Application Package
Model: CPVClassifier v1.0
"""

from flask import Flask
from config import config
from flask_cors import CORS

def create_app(config_name='default'):
    """Factory function do tworzenia aplikacji Flask."""
    from pathlib import Path
    
    BASE_DIR = Path(__file__).parent.parent
    
    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / 'templates'),
        static_folder=str(BASE_DIR / 'static')
    )
    app.config.from_object(config[config_name])
    CORS(app)
    
    # Register blueprints
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app

