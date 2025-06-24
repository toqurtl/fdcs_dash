#!/usr/bin/env python3
"""
전자상거래 대시보드 데이터베이스 초기화 스크립트
"""

from app.infrastructure.database.sqlite_connection import SQLiteConnection

def main():
    print("🗄️  전자상거래 대시보드 데이터베이스를 초기화합니다...")
    
    # SQLite 연결 생성
    db = SQLiteConnection()
    
    try:
        # 데이터베이스 및 테이블 생성
        print("📋 테이블을 생성중입니다...")
        db.init_database()
        print("✅ 테이블 생성 완료")
        
        # 샘플 데이터 삽입
        print("📊 샘플 데이터를 삽입중입니다...")
        db.insert_sample_data()
        print("✅ 샘플 데이터 삽입 완료")
        
        print("\n🎉 데이터베이스 초기화가 완료되었습니다!")
        print("\n📈 생성된 샘플 데이터:")
        print("   • 사용자: admin (비밀번호: admin123)")
        print("   • 고객: 5명")  
        print("   • 상품: 6개 (노트북, 스마트폰, 태블릿, 무선이어폰, 키보드, 마우스)")
        print("   • 주문: 10건 (최근 6개월)")
        print("   • 업무 영역: 전자상거래 (매출분석, 고객현황, 상품관리)")
        
    except Exception as e:
        print(f"❌ 오류가 발생했습니다: {e}")
        return False
        
    return True

if __name__ == "__main__":
    main()