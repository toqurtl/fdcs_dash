import sqlite3
import os
from contextlib import contextmanager

class SQLiteConnection:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'ecommerce_dashboard.db')
    
    @contextmanager
    def get_connection(self):
        connection = None
        try:
            connection = sqlite3.connect(self.db_path)
            connection.row_factory = sqlite3.Row
            yield connection
        except Exception as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection:
                connection.close()
    
    def execute_query(self, query, params=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
    
    def execute_non_query(self, query, params=None, multiple=False):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if multiple and params:
                cursor.executemany(query, params)
            elif params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.rowcount
    
    def init_database(self):
        """데이터베이스 초기화 및 테이블 생성"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 사용자 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 비즈니스 카테고리 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS business_categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    order_num INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 비즈니스 콘텐츠 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS business_contents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    route TEXT NOT NULL,
                    icon TEXT,
                    order_num INTEGER DEFAULT 0,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES business_categories(id)
                )
            ''')
            
            # 고객 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    city TEXT,
                    registration_date DATE DEFAULT CURRENT_DATE
                )
            ''')
            
            # 상품 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
                    stock_quantity INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 주문 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price DECIMAL(10,2) NOT NULL,
                    total_amount DECIMAL(10,2) NOT NULL,
                    order_date DATE DEFAULT CURRENT_DATE,
                    status TEXT DEFAULT 'pending',
                    FOREIGN KEY (customer_id) REFERENCES customers(id),
                    FOREIGN KEY (product_id) REFERENCES products(id)
                )
            ''')
            
            conn.commit()
    
    def insert_sample_data(self):
        """샘플 데이터 삽입"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 기존 데이터 확인
            cursor.execute("SELECT COUNT(*) as count FROM users")
            if cursor.fetchone()['count'] > 0:
                return  # 이미 데이터가 있으면 건너뛰기
            
            # 사용자 데이터
            cursor.execute("""
                INSERT INTO users (username, email, password_hash) 
                VALUES ('admin', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6lUYBWMnNG')
            """)
            
            # 비즈니스 카테고리
            cursor.execute("""
                INSERT INTO business_categories (name, description, order_num) 
                VALUES ('전자상거래', '온라인 쇼핑몰 관리', 1)
            """)
            
            # 비즈니스 콘텐츠
            contents = [
                ('매출 분석', 'sales_analysis', 'fas fa-chart-line', 1),
                ('고객 현황', 'customer_status', 'fas fa-users', 2),
                ('상품 관리', 'product_management', 'fas fa-box', 3)
            ]
            
            for name, route, icon, order_num in contents:
                cursor.execute("""
                    INSERT INTO business_contents (category_id, name, route, icon, order_num)
                    VALUES (1, ?, ?, ?, ?)
                """, (name, route, icon, order_num))
            
            # 데이터 분석 카테고리 추가
            cursor.execute("""
                INSERT INTO business_categories (name, description, order_num) 
                VALUES ('데이터 분석', '대용량 데이터 조회 및 분석', 2)
            """)
            
            # 데이터 분석 콘텐츠
            cursor.execute("""
                INSERT INTO business_contents (category_id, name, route, icon, order_num)
                VALUES (2, '데이터 조회', 'data_table', 'fas fa-table', 1)
            """)
            
            # 고객 데이터
            customers = [
                ('김철수', 'kim@example.com', '010-1234-5678', '서울', '2024-01-15'),
                ('이영희', 'lee@example.com', '010-2345-6789', '부산', '2024-02-20'),
                ('박민수', 'park@example.com', '010-3456-7890', '대구', '2024-03-10'),
                ('최수진', 'choi@example.com', '010-4567-8901', '인천', '2024-04-05'),
                ('정준호', 'jung@example.com', '010-5678-9012', '광주', '2024-05-12')
            ]
            
            for customer in customers:
                cursor.execute("""
                    INSERT INTO customers (name, email, phone, city, registration_date)
                    VALUES (?, ?, ?, ?, ?)
                """, customer)
            
            # 상품 데이터
            products = [
                ('노트북', '전자제품', 1200000, 15),
                ('스마트폰', '전자제품', 800000, 25),
                ('태블릿', '전자제품', 600000, 10),
                ('무선이어폰', '액세서리', 150000, 50),
                ('키보드', '액세서리', 80000, 30),
                ('마우스', '액세서리', 50000, 40)
            ]
            
            for product in products:
                cursor.execute("""
                    INSERT INTO products (name, category, price, stock_quantity)
                    VALUES (?, ?, ?, ?)
                """, product)
            
            # 주문 데이터 (최근 6개월)
            orders = [
                (1, 1, 1, 1200000, 1200000, '2024-01-20', 'completed'),
                (2, 2, 2, 800000, 1600000, '2024-02-25', 'completed'),
                (3, 4, 1, 150000, 150000, '2024-03-15', 'completed'),
                (1, 3, 1, 600000, 600000, '2024-03-22', 'completed'),
                (4, 1, 1, 1200000, 1200000, '2024-04-10', 'completed'),
                (5, 5, 2, 80000, 160000, '2024-04-18', 'completed'),
                (2, 6, 3, 50000, 150000, '2024-05-05', 'completed'),
                (3, 2, 1, 800000, 800000, '2024-05-20', 'completed'),
                (4, 4, 2, 150000, 300000, '2024-06-01', 'pending'),
                (5, 1, 1, 1200000, 1200000, '2024-06-15', 'pending')
            ]
            
            for order in orders:
                cursor.execute("""
                    INSERT INTO orders (customer_id, product_id, quantity, unit_price, total_amount, order_date, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, order)
            
            conn.commit()