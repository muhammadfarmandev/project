# Database configuration
# Simple config for SQL Server connection

# Database connection settings
DB_SERVER = 'localhost'
DB_NAME = 'NSOS'
DB_DRIVER = '{ODBC Driver 17 for SQL Server}'  # Change if you have different driver

# Connection string for Windows Authentication
def get_connection_string():
    """Returns connection string for database"""
    return f"""
    DRIVER={DB_DRIVER};
    SERVER={DB_SERVER};
    DATABASE={DB_NAME};
    Trusted_Connection=yes;
    """

# Flask settings
SECRET_KEY = 'nsos-secret-key-2025'  # Change in production
import os
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
MAX_UPLOAD_SIZE = 16 * 1024 * 1024  # 16MB max file size

