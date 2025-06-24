#!/usr/bin/env python3
"""
관리자 계정 재설정
"""

from app.infrastructure.database.sqlite_connection import SQLiteConnection
from app.domain.models.user import User

def reset_admin():
    print("🔄 관리자 계정을 재설정합니다...")
    
    db = SQLiteConnection()
    
    try:
        # 기존 admin 삭제
        db.execute_non_query("DELETE FROM users WHERE username = 'admin'")
        print("   기존 admin 계정 삭제됨")
        
        # 새 패스워드 해시 생성
        password_hash = User.hash_password('admin123')
        print(f"   새 패스워드 해시 생성: {password_hash[:30]}...")
        
        # 새 admin 생성
        db.execute_non_query("""
            INSERT INTO users (username, email, password_hash, is_active)
            VALUES (?, ?, ?, ?)
        """, ('admin', 'admin@example.com', password_hash, 1))
        
        print("✅ 새 관리자 계정이 생성되었습니다.")
        
        # 검증 테스트
        users = db.execute_query("SELECT * FROM users WHERE username = 'admin'")
        if users:
            user_data = users[0]
            test_user = User(
                id=user_data['id'],
                username=user_data['username'],
                email=user_data['email'],
                password_hash=user_data['password_hash'],
                is_active=user_data['is_active']
            )
            
            if test_user.check_password('admin123'):
                print("✅ 패스워드 검증 성공!")
                print("\n🎉 로그인 정보:")
                print("   사용자명: admin")
                print("   비밀번호: admin123")
            else:
                print("❌ 패스워드 검증 실패")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    reset_admin()