from flask import render_template
from app.ranking.services import get_all_rankings
from app.ranking.__init__ import ranking_bp

@ranking_bp.route('/', methods=['GET'])
def rankingPage():
    print("되냐?")
    rankings = get_all_rankings()
    return render_template('ranking.html', rankings=rankings)


