from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-123')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///educv.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

from datetime import timedelta
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

@app.before_request
def make_session_permanent():
    session.permanent = True

db = SQLAlchemy(app)

# Register Blueprints
from routes.main import main_bp
from routes.ai import ai_bp
app.register_blueprint(main_bp)
app.register_blueprint(ai_bp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
