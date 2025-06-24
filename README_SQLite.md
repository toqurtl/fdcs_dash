# 🛒 전자상거래 대시보드 - SQLite3 예제

SQLite3로 구현된 전자상거래 대시보드 시스템입니다. 실제 데이터와 연동되어 동작하는 완전한 예제입니다.

## 🚀 빠른 시작

### 1. 데이터베이스 초기화
```bash
cd dashboard_project
python init_database.py
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 서버 실행
```bash
python run.py
```

### 4. 브라우저 접속
```
http://localhost:5000
```

## 🔐 로그인 정보
- **사용자명**: `admin`
- **비밀번호**: `admin123`

## 📊 예제 데이터

### 업무 영역: 전자상거래
1. **매출 분석** (`sales_analysis`)
   - 월별 매출액 및 주문 건수 라인 차트
   - 실제 주문 데이터에서 집계

2. **고객 현황** (`customer_status`)  
   - 지역별 고객 분포 (도넛 차트)
   - 월별 신규 고객 (막대 차트)

3. **상품 관리** (`product_management`)
   - 상품별 판매량과 수익 테이블
   - 재고 현황 포함

### 샘플 데이터
- **고객**: 5명 (서울, 부산, 대구, 인천, 광주)
- **상품**: 6개 (노트북, 스마트폰, 태블릿, 무선이어폰, 키보드, 마우스)
- **주문**: 10건 (2024년 1월~6월)

## 🗄️ 데이터베이스 구조

### 주요 테이블
```sql
-- 사용자
users (id, username, email, password_hash, is_active, created_at)

-- 비즈니스 구조
business_categories (id, name, description, order_num, created_at)
business_contents (id, category_id, name, route, icon, order_num, is_active, created_at)

-- 전자상거래 데이터
customers (id, name, email, phone, city, registration_date)
products (id, name, category, price, stock_quantity, created_at)
orders (id, customer_id, product_id, quantity, unit_price, total_amount, order_date, status)
```

## 💡 학습 포인트

### 1. 실제 데이터 연동
- SQLite3로 실제 데이터 조회
- 집계 쿼리 (SUM, COUNT, GROUP BY)
- JOIN을 활용한 복합 데이터 조회

### 2. 동적 차트 렌더링
- Chart.js 라이브러리 활용
- 다양한 차트 타입 (라인, 막대, 도넛)
- 실시간 데이터 업데이트

### 3. MVC + DDD 아키텍처
- Domain Layer: 비즈니스 로직 분리
- Infrastructure Layer: 데이터 접근 추상화
- Presentation Layer: 컨트롤러와 뷰 분리

### 4. 보안 구현
- Flask-Login 세션 관리
- bcrypt 패스워드 해싱
- CSRF 보안 토큰

## 🔧 커스터마이징

### 새로운 차트 추가
1. `DashboardService`에 새 메서드 추가
2. `dashboard.js`에 렌더링 로직 추가
3. 데이터베이스에 새 콘텐츠 등록

### 데이터 추가
```python
from app.infrastructure.database.sqlite_connection import SQLiteConnection

db = SQLiteConnection()
db.execute_non_query("""
    INSERT INTO orders (customer_id, product_id, quantity, unit_price, total_amount, order_date)
    VALUES (?, ?, ?, ?, ?, ?)
""", (customer_id, product_id, quantity, price, total, date))
```

## 📈 확장 아이디어

1. **실시간 대시보드**: WebSocket으로 실시간 업데이트
2. **필터링**: 날짜 범위, 카테고리별 필터
3. **드릴다운**: 차트 클릭 시 상세 데이터 표시
4. **PDF 내보내기**: 리포트 생성 기능
5. **REST API**: 모바일 앱 연동용 API

## 🎯 이 예제로 배울 수 있는 것

- SQLite3를 활용한 경량 데이터베이스 설계
- Flask-Login 인증 시스템 구현
- AdminLTE를 활용한 반응형 대시보드 UI
- Chart.js를 활용한 데이터 시각화
- Clean Architecture 원칙 적용
- 실제 비즈니스 로직과 데이터 연동

완전히 동작하는 전자상거래 대시보드로 실습해보세요! 🎉