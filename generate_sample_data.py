#!/usr/bin/env python3
"""
대용량 샘플 데이터 생성 스크립트
- 고객 데이터 1000명
- 주문 데이터 5000건  
- 상품 데이터 100개
"""

import random
import sqlite3
from datetime import datetime, timedelta
from app.infrastructure.database.sqlite_connection import SQLiteConnection

# 샘플 데이터 생성용 데이터
KOREAN_LAST_NAMES = ['김', '이', '박', '최', '정', '강', '조', '윤', '장', '임', '한', '오', '서', '신', '권', '황', '안', '송', '류', '전']
KOREAN_FIRST_NAMES = ['민수', '수진', '영호', '은정', '현우', '지영', '태형', '소영', '동현', '미영', '준영', '혜진', '상훈', '나영', '재현', '다은', '성민', '수빈', '진우', '예은']

CITIES = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주']

PRODUCT_CATEGORIES = ['전자제품', '의류', '도서', '가구', '식품', '스포츠', '뷰티', '완구', '자동차용품', '문구']

PRODUCT_NAMES = {
    '전자제품': ['노트북', '스마트폰', '태블릿', '스마트워치', '이어폰', '키보드', '마우스', '모니터', '스피커', '웹캠'],
    '의류': ['티셔츠', '청바지', '원피스', '자켓', '스니커즈', '부츠', '셔츠', '스웨터', '코트', '가디건'],
    '도서': ['소설', '에세이', '자기계발서', '요리책', '여행가이드', '전문서적', '만화', '잡지', '사전', '교재'],
    '가구': ['의자', '책상', '침대', '소파', '옷장', '서랍', '테이블', '선반', '조명', '거울'],
    '식품': ['쌀', '라면', '과자', '음료', '커피', '차', '견과류', '육류', '채소', '과일'],
    '스포츠': ['운동화', '헬스기구', '골프용품', '수영용품', '등산용품', '자전거', '요가매트', '축구공', '농구공', '배드민턴'],
    '뷰티': ['스킨케어', '메이크업', '향수', '헤어케어', '바디케어', '네일', '클렌징', '마스크', '선크림', '립밤'],
    '완구': ['레고', '인형', '퍼즐', '보드게임', '로봇', '자동차', '블록', '악기', '공예키트', '교육완구'],
    '자동차용품': ['타이어', '오일', '방향제', '매트', '커버', '액세서리', '네비게이션', '블랙박스', '충전기', '청소용품'],
    '문구': ['펜', '노트', '스티커', '테이프', '가위', '풀', '자', '지우개', '형광펜', '파일']
}

ORDER_STATUSES = ['pending', 'processing', 'shipped', 'delivered', 'cancelled', 'returned']

def generate_customers(db, count=1000):
    """고객 데이터 생성"""
    print(f"👥 {count}명의 고객 데이터 생성 중...")
    
    customers = []
    for i in range(count):
        last_name = random.choice(KOREAN_LAST_NAMES)
        first_name = random.choice(KOREAN_FIRST_NAMES)
        name = f"{last_name}{first_name}"
        
        # 이메일과 전화번호 중복 방지를 위한 인덱스 추가
        email = f"{name.lower()}{i+1}@example.com"
        phone = f"010-{random.randint(1000,9999)}-{random.randint(1000,9999)}"
        city = random.choice(CITIES)
        
        # 가입일 (최근 2년 내)
        start_date = datetime.now() - timedelta(days=730)
        random_days = random.randint(0, 730)
        registration_date = start_date + timedelta(days=random_days)
        
        customers.append((name, email, phone, city, registration_date.strftime('%Y-%m-%d')))
    
    # 기존 고객 데이터 삭제 후 새로 삽입
    db.execute_non_query("DELETE FROM customers WHERE id > 5")  # 원래 5명은 유지
    
    db.execute_non_query("""
        INSERT INTO customers (name, email, phone, city, registration_date)
        VALUES (?, ?, ?, ?, ?)
    """, customers, multiple=True)
    
    print(f"✅ {count}명의 고객 데이터 생성 완료")

def generate_products(db, count=100):
    """상품 데이터 생성"""
    print(f"📦 {count}개의 상품 데이터 생성 중...")
    
    products = []
    for i in range(count):
        category = random.choice(PRODUCT_CATEGORIES)
        base_name = random.choice(PRODUCT_NAMES[category])
        name = f"{base_name} {random.choice(['프리미엄', '스탠다드', '베이직', '프로', '라이트'])}"
        
        # 카테고리별 가격 범위 설정
        price_ranges = {
            '전자제품': (50000, 2000000),
            '의류': (10000, 300000),
            '도서': (5000, 50000),
            '가구': (30000, 1000000),
            '식품': (1000, 100000),
            '스포츠': (10000, 500000),
            '뷰티': (5000, 200000),
            '완구': (5000, 150000),
            '자동차용품': (10000, 300000),
            '문구': (500, 50000)
        }
        
        min_price, max_price = price_ranges[category]
        price = random.randint(min_price, max_price)
        stock_quantity = random.randint(0, 200)
        
        products.append((name, category, price, stock_quantity))
    
    # 기존 상품 데이터 삭제 후 새로 삽입  
    db.execute_non_query("DELETE FROM products WHERE id > 6")  # 원래 6개는 유지
    
    db.execute_non_query("""
        INSERT INTO products (name, category, price, stock_quantity)
        VALUES (?, ?, ?, ?)
    """, products, multiple=True)
    
    print(f"✅ {count}개의 상품 데이터 생성 완료")

def generate_orders(db, count=5000):
    """주문 데이터 생성"""
    print(f"🛒 {count}건의 주문 데이터 생성 중...")
    
    # 고객과 상품 ID 범위 확인
    customers = db.execute_query("SELECT id FROM customers")
    products = db.execute_query("SELECT id, price FROM products")
    
    customer_ids = [c['id'] for c in customers]
    product_data = [(p['id'], p['price']) for p in products]
    
    orders = []
    for i in range(count):
        customer_id = random.choice(customer_ids)
        product_id, unit_price = random.choice(product_data)
        quantity = random.randint(1, 5)
        total_amount = unit_price * quantity
        
        # 주문일 (최근 1년 내)
        start_date = datetime.now() - timedelta(days=365)
        random_days = random.randint(0, 365)
        order_date = start_date + timedelta(days=random_days)
        
        status = random.choice(ORDER_STATUSES)
        
        orders.append((
            customer_id, product_id, quantity, unit_price, 
            total_amount, order_date.strftime('%Y-%m-%d'), status
        ))
    
    # 기존 주문 데이터 삭제 후 새로 삽입
    db.execute_non_query("DELETE FROM orders WHERE id > 10")  # 원래 10개는 유지
    
    db.execute_non_query("""
        INSERT INTO orders (customer_id, product_id, quantity, unit_price, total_amount, order_date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, orders, multiple=True)
    
    print(f"✅ {count}건의 주문 데이터 생성 완료")

def main():
    print("🗄️ 대용량 샘플 데이터 생성을 시작합니다...")
    
    db = SQLiteConnection()
    
    # SQLite 연결 클래스에 bulk insert 메서드 추가
    def execute_bulk_insert(self, query, data_list):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, data_list)
            conn.commit()
            return cursor.rowcount
    
    # 임시로 메서드 추가
    import types
    db.execute_non_query_bulk = types.MethodType(
        lambda self, query, data_list: execute_bulk_insert(self, query, data_list), 
        db
    )
    
    try:
        # 1000명의 고객 생성
        generate_customers(db, 1000)
        
        # 100개의 상품 생성
        generate_products(db, 100)
        
        # 5000건의 주문 생성
        generate_orders(db, 5000)
        
        # 통계 출력
        stats = {
            'customers': db.execute_query("SELECT COUNT(*) as count FROM customers")[0]['count'],
            'products': db.execute_query("SELECT COUNT(*) as count FROM products")[0]['count'],
            'orders': db.execute_query("SELECT COUNT(*) as count FROM orders")[0]['count']
        }
        
        print("\n📊 데이터 생성 완료!")
        print(f"   👥 총 고객: {stats['customers']}명")
        print(f"   📦 총 상품: {stats['products']}개")
        print(f"   🛒 총 주문: {stats['orders']}건")
        print("\n🎉 대용량 샘플 데이터 생성이 완료되었습니다!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

# SQLiteConnection 클래스 확장
def extend_sqlite_connection():
    """SQLite 연결 클래스에 bulk insert 기능 추가"""
    original_init = SQLiteConnection.__init__
    
    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
    
    def execute_non_query_bulk(self, query, data_list):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, data_list)
            conn.commit()
            return cursor.rowcount
    
    SQLiteConnection.__init__ = new_init
    SQLiteConnection.execute_non_query_bulk = execute_non_query_bulk

if __name__ == "__main__":
    extend_sqlite_connection()
    main()