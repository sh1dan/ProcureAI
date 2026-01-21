"""
Konfiguracja aplikacji ProcureAI CPV Predictor
Model: CPVClassifier v1.0
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Flask configuration
class Config:
    """Podstawowa konfiguracja."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Model paths
    MODEL_PATH = BASE_DIR / 'models' / 'model.pkl'
    METRICS_PATH = BASE_DIR / 'models' / 'metrics.txt'
    
    # Data paths
    DATA_PATH = BASE_DIR / 'data' / 'ted_sample.csv'
    
    # Model info
    MODEL_NAME = 'CPVClassifier'
    MODEL_VERSION = '1.0'
    MODEL_ALGORITHM = 'Random Forest'

class DevelopmentConfig(Config):
    """Konfiguracja deweloperska."""
    DEBUG = True

class ProductionConfig(Config):
    """Konfiguracja produkcyjna."""
    DEBUG = False

# Wybór konfiguracji na podstawie zmiennej środowiskowej
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

