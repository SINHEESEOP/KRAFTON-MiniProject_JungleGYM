from app import create_app
from dotenv import load_dotenv
from flask import redirect, url_for
from flask_jwt_extended import JWTManager

load_dotenv()

app = create_app()

jwt = JWTManager(app)

@jwt.unauthorized_loader
def custom_unauthorized_response(_err):
    return redirect(url_for('auth.login'))

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
