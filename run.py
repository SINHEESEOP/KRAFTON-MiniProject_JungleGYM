from app import create_app
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

load_dotenv()

app = create_app()

jwt = JWTManager(app)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
