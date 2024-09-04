
from flask import render_template
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.ranking.services import get_all_rankings, get_level
from app.ranking.__init__ import ranking_bp


@ranking_bp.route('/', methods=['GET'])
@jwt_required(locations=['cookies'])
def ranking_page():

    current_user = get_jwt_identity()

    rankings = get_all_rankings()
    level = get_level(current_user)

    print(level)
    return render_template('ranking.html', rankings=rankings, level=level)
