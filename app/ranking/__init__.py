from flask import Blueprint

ranking_bp = Blueprint('ranking', __name__)

from app.ranking import routes, models, services
