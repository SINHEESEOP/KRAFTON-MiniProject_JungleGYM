from flask import Flask, redirect, render_template
from flask_pymongo import PyMongo
import os

mongo = PyMongo()


def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = os.getenv("SCHEME_MONGO_URI")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config['JWT_TOKEN_LOCATION'] = ['headers', 'query_string']
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    mongo.init_app(app)

    # 블루프린트 등록
    from app.auth.__init__ import auth_bp
    from app.meetings.__init__ import meetings_bp
    from app.ranking.__init__ import ranking_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(meetings_bp, url_prefix='/meetings')
    app.register_blueprint(ranking_bp, url_prefix='/ranking')
    
    # 에러 핸들링
    @app.errorhandler(404)
    def not_found_error(error):
        return "Page Not Found", 404

    @app.errorhandler(500)
    def internal_error(error):
        return "Internal Server Error", 500

    # 메인 페이지
    @app.route("/")
    def index():
        return redirect("/meetings")

    @app.route('/map')
    def map():
        return render_template("map_test.html")

    return app
