# AdminLTE Dashboard 프로젝트 개발 기록

## 프로젝트 개요
- **목적**: 교육용 AdminLTE + Flask 대시보드 시스템
- **아키텍처**: MVC + DDD (Domain Driven Design) 패턴
- **기술 스택**: Flask, SQLite3, AdminLTE 3.2, Chart.js, jQuery
- **특징**: 폐쇄망 환경 지원 (모든 외부 의존성 로컬화)

## 개발 진행 내용

### 1. 기본 시스템 구축
#### 완료된 작업:
- Flask 애플리케이션 팩토리 패턴 구현
- 사용자 인증 시스템 (Flask-Login)
- MVC + DDD 아키텍처 적용
- SQLite3 데이터베이스 설계
- AdminLTE 3.2 UI 프레임워크 적용

#### 주요 파일:
- `/app/__init__.py`: Flask 애플리케이션 팩토리
- `/app/domain/`: 도메인 로직 및 서비스
- `/app/presentation/`: 컨트롤러 및 라우트
- `/app/infrastructure/`: 데이터베이스 연결
- `/templates/`: Jinja2 템플릿 파일들

### 2. 대용량 데이터 처리 시스템
#### 완료된 작업:
- 5000+ 주문, 1000+ 고객, 100+ 상품 샘플 데이터 생성
- 고성능 페이지네이션 시스템
- 실시간 검색 및 정렬 기능
- AJAX 기반 비동기 데이터 로딩

#### 주요 파일:
- `/generate_sample_data.py`: 대용량 샘플 데이터 생성 스크립트
- `/app/domain/services/table_service.py`: 테이블 데이터 서비스
- `/app/static/js/advanced-table.js`: 고급 테이블 컴포넌트

### 3. 고급 검색 시스템 (최신 추가)
#### 완료된 작업:
- **아코디언 스타일 고급 검색 패널**: 접힘/펼침 가능한 UI
- **복합 조건 검색**: 여러 컬럼 동시 검색 지원
- **다양한 검색 연산자**: 포함, 같음, 초과, 미만, NULL 체크 등
- **AND/OR 논리 연산**: 복잡한 조건 조합 가능
- **동적 필터 관리**: 실시간으로 조건 추가/삭제

#### 검색 기능 세부사항:
- **기본 검색**: 단일 컬럼 LIKE 검색 (기존 방식 유지)
- **고급 검색**: 
  - 다중 컬럼 복합 조건
  - 연산자: contains, equals, not_equals, starts_with, ends_with, greater_than, less_than, is_null, is_not_null
  - 논리 연산자: AND, OR
  - JSON 형태로 백엔드 전송

#### 주요 수정 파일:
- `/app/static/js/advanced-table.js`: 고급 검색 UI 및 로직 추가
- `/app/domain/services/table_service.py`: 복합 검색 쿼리 생성 로직
- `/app/presentation/controllers/api_controller.py`: 고급 검색 파라미터 처리

### 4. 폐쇄망 환경 지원
#### 완료된 작업:
- 모든 외부 CDN 의존성을 로컬로 다운로드
- 폰트 파일 포함 완전한 오프라인 지원
- 로컬 경로로 템플릿 참조 변경

#### 로컬화된 라이브러리:
- `/app/static/vendors/jquery/`: jQuery 3.6.0
- `/app/static/vendors/bootstrap/`: Bootstrap 4.6
- `/app/static/vendors/adminlte/`: AdminLTE 3.2
- `/app/static/vendors/chartjs/`: Chart.js
- `/app/static/vendors/fontawesome/`: Font Awesome
- `/app/static/vendors/fonts/`: Source Sans Pro 폰트 파일들

## 데이터베이스 구조

### 테이블 스키마:
```sql
-- 고객 테이블
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    city TEXT,
    registration_date DATE
);

-- 상품 테이블  
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT,
    price DECIMAL(10,2),
    stock_quantity INTEGER,
    created_at TIMESTAMP
);

-- 주문 테이블
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    order_date DATE,
    status TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

## 실행 방법

### 초기 설정:
```bash
# 데이터베이스 초기화 및 샘플 데이터 생성
python init_database.py
python generate_sample_data.py

# 애플리케이션 실행
python run.py
```

### 접속 정보:
- **URL**: http://localhost:5000
- **로그인**: admin / admin123

## 주요 기능

### 1. 대시보드
- 매출 통계 차트 (Chart.js)
- 방문자 통계
- 실시간 데이터 업데이트

### 2. 데이터 조회 시스템
- **테이블 선택**: 주문 현황, 고객 관리, 상품 목록
- **기본 검색**: 단일 컬럼 검색
- **고급 검색**: 
  - 아코디언 형태 UI
  - 복합 조건 검색
  - 동적 필터 추가/삭제
  - AND/OR 논리 연산
- **페이지네이션**: 대용량 데이터 효율적 처리
- **정렬**: 모든 컬럼 오름차순/내림차순
- **실시간 통계**: 총 데이터 수, 페이지 정보

### 3. 사용자 인증
- 로그인/로그아웃
- 세션 관리
- 권한 기반 라우트 보호

## 기술적 특징

### 1. 아키텍처
- **Clean Architecture**: 도메인 로직과 인프라 분리
- **Repository Pattern**: 데이터 액세스 추상화
- **Service Layer**: 비즈니스 로직 캡슐화

### 2. 성능 최적화
- **페이지네이션**: LIMIT/OFFSET 쿼리
- **인덱싱**: 주요 검색 컬럼 인덱스
- **AJAX**: 비동기 데이터 로딩
- **캐싱**: 정적 파일 최적화

### 3. 보안
- **SQL Injection 방지**: 파라미터화된 쿼리
- **CSRF 보호**: Flask-WTF
- **세션 보안**: Flask-Login

## 개발 환경 명령어

### 데이터베이스 관련:
```bash
# 데이터베이스 재생성
python init_database.py

# 샘플 데이터 추가 생성
python generate_sample_data.py
```

### 개발 서버:
```bash
# 개발 모드 실행
python run.py

# 디버그 모드
export FLASK_ENV=development
python run.py
```

## 향후 확장 계획

### 단기 계획:
- [ ] 데이터 내보내기 기능 (CSV, Excel)
- [ ] 고급 차트 및 리포트
- [ ] 사용자 권한 관리 시스템

### 중기 계획:
- [ ] RESTful API 완성
- [ ] 모바일 반응형 개선
- [ ] 실시간 알림 시스템

### 장기 계획:
- [ ] 다중 테넌트 지원
- [ ] 마이크로서비스 아키텍처 전환
- [ ] 클라우드 배포 지원

## 트러블슈팅

### 일반적인 문제:
1. **템플릿 오류**: 경로 확인 및 templates 폴더 구조 점검
2. **데이터베이스 오류**: init_database.py 재실행
3. **정적 파일 오류**: vendors 폴더 권한 및 경로 확인

### 성능 이슈:
1. **느린 쿼리**: 인덱스 추가 검토
2. **메모리 사용량**: 페이지 크기 조정
3. **응답 시간**: 캐싱 전략 검토

---

**마지막 업데이트**: 2025-06-25  
**개발자**: Claude Code Assistant  
**버전**: 1.2.0 (고급 검색 시스템 추가)