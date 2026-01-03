# Main Flask application for NSOS
# Police Station Management System

from flask import Flask, send_from_directory
from flask_cors import CORS
from config import SECRET_KEY, UPLOAD_FOLDER
from routes import routes
import os

# Create Flask app
app = Flask(__name__, static_folder='../frontend', static_url_path='')

# Configure app
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Session configuration for cookies
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours in seconds
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_PATH'] = '/'  # Make sure cookie is available for all paths

# Enable CORS for API calls (needed if frontend is on different origin)
# Since Flask serves static files, same origin, but keeping for flexibility
CORS(app, supports_credentials=True)

# Register routes
app.register_blueprint(routes)

# Create uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Serve static files from frontend
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory(app.static_folder, path)


# Serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded evidence files"""
    return send_from_directory(UPLOAD_FOLDER, filename)


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return {'error': 'Not found'}, 404


@app.errorhandler(500)
def internal_error(error):
    return {'error': 'Internal server error'}, 500


if __name__ == '__main__':
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)

