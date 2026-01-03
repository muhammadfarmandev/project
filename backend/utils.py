# Utility functions for password hashing and file handling

import bcrypt
import os
from werkzeug.utils import secure_filename

# Upload folder path (relative to project root)
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')

# Allowed file extensions for evidence
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}


def hash_password(password):
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def check_password(password, hashed):
    """Check if password matches hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_file(file):
    """Save uploaded file to uploads folder"""
    if file and allowed_file(file.filename):
        # Make filename safe
        filename = secure_filename(file.filename)
        
        # Make sure uploads folder exists
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        
        # Generate unique filename to avoid conflicts
        import uuid
        unique_filename = str(uuid.uuid4()) + '_' + filename
        
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(filepath)
        
        return unique_filename
    return None


def delete_file(filename):
    """Delete file from uploads folder"""
    if filename:
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
    return False

