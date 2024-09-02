from flask import Flask, render_template
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"  # MongoDB URI 설정
    mongo.init_app(app)

    # 블루프린트 등록
    from app.auth._init_ import auth_bp
    from app.meetings._init_ import meetings_bp
    from app.ranking._init_ import ranking_bp
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

    @app.route('/')
    def index():
        return render_template("index.html")

    return app
