import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    MARIADB_HOST = os.environ.get('MARIADB_HOST', 'localhost')
    MARIADB_PORT = int(os.environ.get('MARIADB_PORT', 3306))
    MARIADB_USER = os.environ.get('MARIADB_USER', 'root')
    MARIADB_PASSWORD = os.environ.get('MARIADB_PASSWORD', 'password')
    MARIADB_DATABASE = os.environ.get('MARIADB_DATABASE', 'dashboard')
    
    POSTGRESQL_HOST = os.environ.get('POSTGRESQL_HOST', 'localhost')
    POSTGRESQL_PORT = int(os.environ.get('POSTGRESQL_PORT', 5432))
    POSTGRESQL_USER = os.environ.get('POSTGRESQL_USER', 'postgres')
    POSTGRESQL_PASSWORD = os.environ.get('POSTGRESQL_PASSWORD', 'password')
    POSTGRESQL_DATABASE = os.environ.get('POSTGRESQL_DATABASE', 'dashboard')
    
    WTF_CSRF_ENABLED = True