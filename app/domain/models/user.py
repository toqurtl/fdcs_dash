from flask_login import UserMixin
from datetime import datetime
import bcrypt

class User(UserMixin):
    def __init__(self, id=None, username=None, email=None, password_hash=None, 
                 is_active=True, created_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self._is_active = is_active
        self.created_at = created_at or datetime.now()
    
    def check_password(self, password):
        if not self.password_hash:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def get_id(self):
        return str(self.id)
    
    @property
    def is_active(self):
        return self._is_active
    
    def is_authenticated(self):
        return True
    
    def is_anonymous(self):
        return False