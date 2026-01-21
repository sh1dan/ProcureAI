"""
Routes dla głównego interfejsu webowego
"""

from app.main import bp
from flask import render_template

@bp.route('/')
def index():
    """Główna strona aplikacji."""
    return render_template('index.html')

