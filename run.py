from app import create_app
from dotenv import load_dotenv
from flask import redirect
from flask_jwt_extended import JWTManager, unset_jwt_cookies

load_dotenv()

app = create_app()

jwt = JWTManager(app)

@jwt.unauthorized_loader
def custom_unauthorized_response(_err):
    return redirect('/auth/login')

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    response = redirect('/auth/login')
    unset_jwt_cookies(response)
    return response

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
