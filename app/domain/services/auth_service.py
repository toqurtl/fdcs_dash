from app.domain.models.user import User

class AuthService:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def authenticate_user(self, username, password):
        user = self.get_user_by_username(username)
        if user and user.check_password(password):
            return user
        return None
    
    def get_user_by_username(self, username):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, username, email, password_hash, is_active, created_at 
                FROM users WHERE username = ?
            """, (username,))
            row = cursor.fetchone()
            
            if row:
                return User(
                    id=row[0],
                    username=row[1], 
                    email=row[2],
                    password_hash=row[3],
                    is_active=bool(row[4]),
                    created_at=row[5]
                )
            return None
    
    def get_user_by_id(self, user_id):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, username, email, password_hash, is_active, created_at 
                FROM users WHERE id = ?
            """, (user_id,))
            row = cursor.fetchone()
            
            if row:
                return User(
                    id=row[0],
                    username=row[1],
                    email=row[2], 
                    password_hash=row[3],
                    is_active=bool(row[4]),
                    created_at=row[5]
                )
            return None
    
    def create_user(self, username, email, password):
        password_hash = User.hash_password(password)
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, email, password_hash) 
                VALUES (?, ?, ?)
            """, (username, email, password_hash))
            conn.commit()
            
            user_id = cursor.lastrowid
            return self.get_user_by_id(user_id)