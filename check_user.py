#!/usr/bin/env python3
"""
사용자 데이터 확인 스크립트
"""

from app.infrastructure.database.sqlite_connection import SQLiteConnection
from app.domain.models.user import User

def check_users():
    print("🔍 데이터베이스 사용자 확인 중...")
    
    db = SQLiteConnection()
    
    try:
        # 모든 사용자 조회
        users = db.execute_query("SELECT * FROM users")
        
        print(f"📊 총 사용자 수: {len(users)}")
        
        for user in users:
            print(f"\n👤 사용자 정보:")
            print(f"   ID: {user['id']}")
            print(f"   사용자명: {user['username']}")
            print(f"   이메일: {user['email']}")
            print(f"   활성화: {user['is_active']}")
            print(f"   패스워드 해시: {user['password_hash'][:50]}...")
            
            # 패스워드 확인 테스트
            test_user = User(
                id=user['id'],
                username=user['username'],
                email=user['email'],
                password_hash=user['password_hash'],
                is_active=user['is_active']
            )
            
            # admin123 패스워드 테스트
            password_valid = test_user.check_password('admin123')
            print(f"   admin123 패스워드 검증: {'✅ 성공' if password_valid else '❌ 실패'}")
        
        if len(users) == 0:
            print("\n❌ 사용자가 없습니다. 다시 데이터베이스를 초기화하세요.")
            return False
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False
    
    return True

def recreate_admin():
    """관리자 계정 재생성"""
    print("\n🔄 관리자 계정을 재생성합니다...")
    
    db = SQLiteConnection()
    
    try:
        # 기존 admin 삭제
        db.execute_non_query("DELETE FROM users WHERE username = 'admin'")
        
        # 새 admin 생성
        password_hash = User.hash_password('admin123')
        db.execute_non_query("""
            INSERT INTO users (username, email, password_hash, is_active)
            VALUES (?, ?, ?, ?)
        """, ('admin', 'admin@example.com', password_hash, 1))
        
        print("✅ 관리자 계정이 재생성되었습니다.")
        
        # 확인
        return check_users()
        
    except Exception as e:
        print(f"❌ 계정 재생성 실패: {e}")
        return False

if __name__ == "__main__":
    if not check_users():
        recreate_admin()