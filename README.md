# 🛒 전자상거래 대시보드 시스템

Flask + AdminLTE + SQLite3로 구현된 완전한 대시보드 시스템입니다. 실제 데이터베이스와 연동되어 동적으로 차트와 테이블을 생성하는 학습용 예제입니다.

## 🎯 프로젝트 개요

### 주요 기능
- **로그인 시스템**: Flask-Login + bcrypt 보안 인증
- **실시간 대시보드**: SQLite3 데이터베이스와 연동
- **인터랙티브 차트**: Chart.js를 활용한 다양한 시각화
- **반응형 UI**: AdminLTE 3.2 기반 모바일 지원

### 업무 영역
**전자상거래 관리** - 3개 콘텐츠 영역
1. 📈 **매출 분석**: 월별 매출액과 주문 건수 (라인 차트)
2. 👥 **고객 현황**: 지역별 분포 + 월별 신규 고객 (도넛 + 막대 차트)
3. 📦 **상품 관리**: 상품별 판매량, 재고, 수익 (테이블)

## 🚀 빠른 시작

### 1. 프로젝트 클론 및 이동
```bash
git clone <repository-url>
cd dashboard_project
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 데이터베이스 초기화
```bash
python3 init_database.py
```

### 4. 서버 실행
```bash
python3 run.py
```

### 5. 브라우저 접속
```
http://localhost:5000
```

## 🔐 로그인 정보

- **사용자명**: `admin`
- **비밀번호**: `admin123`

> ⚠️ 로그인이 안되면 `python3 reset_admin.py`로 계정을 재설정하세요.

## 📊 샘플 데이터

### 고객 데이터 (5명)
- 김철수 (서울), 이영희 (부산), 박민수 (대구), 최수진 (인천), 정준호 (광주)

### 상품 데이터 (6개)
- **전자제품**: 노트북(120만원), 스마트폰(80만원), 태블릿(60만원)
- **액세서리**: 무선이어폰(15만원), 키보드(8만원), 마우스(5만원)

### 주문 데이터 (10건)
- 2024년 1월~6월 기간의 실제 주문 내역
- 완료된 주문과 대기 중인 주문 포함

## 🎮 사용 방법

### 1. 로그인
1. 브라우저에서 `http://localhost:5000` 접속
2. admin/admin123으로 로그인

### 2. 대시보드 탐색
1. **메인 대시보드**: 기본 통계 카드와 차트 확인
2. **사이드바 네비게이션**: "전자상거래" 펼치기
3. **콘텐츠 클릭**: 각 메뉴 클릭 시 동적 데이터 로딩

### 3. 각 콘텐츠별 기능
- **매출 분석**: 월별 매출 트렌드와 주문량 분석
- **고객 현황**: 지역별 고객 분포와 신규 고객 추이
- **상품 관리**: 상품별 성과 및 재고 현황

## 🏗️ 프로젝트 구조

```
dashboard_project/
├── app/                          # 메인 애플리케이션
│   ├── config/                   # 설정 파일
│   ├── domain/                   # 도메인 레이어 (DDD)
│   │   ├── models/              # 비즈니스 모델
│   │   └── services/            # 비즈니스 로직
│   ├── infrastructure/          # 인프라 레이어
│   │   ├── database/            # DB 연결 관리
│   │   └── repositories/        # 데이터 접근
│   ├── presentation/            # 프레젠테이션 레이어
│   │   ├── controllers/         # MVC 컨트롤러
│   │   └── forms/               # 폼 정의
│   └── static/                  # 정적 파일
├── templates/                   # Jinja2 템플릿
├── ecommerce_dashboard.db      # SQLite 데이터베이스
├── init_database.py            # DB 초기화 스크립트
├── reset_admin.py              # 관리자 계정 재설정
└── run.py                      # 서버 실행 파일
```

## 🛠️ 기술 스택

### Backend
- **Flask 2.2.5**: 웹 프레임워크
- **SQLite3**: 경량 데이터베이스
- **Flask-Login**: 사용자 인증
- **bcrypt**: 패스워드 해싱

### Frontend
- **AdminLTE 3.2**: 관리자 UI 테마
- **Chart.js**: 데이터 시각화
- **jQuery**: DOM 조작
- **Bootstrap 4**: 반응형 디자인

### Architecture
- **MVC Pattern**: Model-View-Controller 구조
- **DDD**: Domain Driven Design 적용
- **Repository Pattern**: 데이터 접근 추상화

## 🔧 커스터마이징

### 새로운 차트 추가하기

1. **데이터베이스에 콘텐츠 추가**
```sql
INSERT INTO business_contents (category_id, name, route, icon, order_num)
VALUES (1, '새 분석', 'new_analysis', 'fas fa-chart-bar', 4);
```

2. **DashboardService에 메서드 추가**
```python
def _get_new_analysis(self):
    # 데이터 조회 로직
    return {
        'title': '새 분석',
        'type': 'bar',
        'data': {...}
    }
```

3. **라우팅 추가**
```python
elif route == 'new_analysis':
    return self._get_new_analysis()
```

### 새로운 업무 영역 추가하기

1. **카테고리 추가**
```sql
INSERT INTO business_categories (name, description, order_num)
VALUES ('새 업무영역', '새로운 업무 설명', 2);
```

2. **해당 콘텐츠들 추가**
3. **비즈니스 로직 구현**

## 📝 학습 포인트

### 1. Flask 웹 개발
- Blueprint를 활용한 모듈 구조화
- Jinja2 템플릿 시스템
- 정적 파일 관리

### 2. 데이터베이스 설계
- SQLite3 활용법
- 관계형 데이터베이스 설계
- SQL 집계 쿼리 (GROUP BY, JOIN)

### 3. 프론트엔드 개발
- AdminLTE 커스터마이징
- Chart.js 동적 차트 생성
- AJAX를 활용한 SPA 구현

### 4. 보안 구현
- 사용자 인증/인가
- 패스워드 보안 처리
- CSRF 보안

### 5. 소프트웨어 아키텍처
- Clean Architecture 원칙
- 의존성 주입 패턴
- 관심사의 분리

## 🐛 문제 해결

### 로그인이 안될 때
```bash
python3 reset_admin.py
```

### 템플릿을 찾을 수 없을 때
```bash
# 올바른 디렉토리에서 실행하는지 확인
cd dashboard_project
python3 run.py
```

### 데이터가 표시되지 않을 때
```bash
python3 check_user.py  # 사용자 확인
python3 init_database.py  # DB 재초기화
```

## 📚 참고 자료

- [Flask 공식 문서](https://flask.palletsprojects.com/)
- [AdminLTE 문서](https://adminlte.io/docs/3.2/)
- [Chart.js 문서](https://www.chartjs.org/docs/)
- [SQLite 문서](https://www.sqlite.org/docs.html)

## 🎉 확장 아이디어

1. **실시간 대시보드**: WebSocket으로 실시간 업데이트
2. **데이터 필터링**: 날짜 범위, 카테고리별 필터
3. **PDF 리포트**: 차트를 PDF로 내보내기
4. **REST API**: 모바일 앱 연동
5. **다중 사용자**: 권한 관리 시스템
6. **알림 시스템**: 이메일/SMS 알림
7. **데이터 백업**: 자동 백업 시스템

---

**🎯 이 프로젝트는 Flask 웹 개발과 데이터 시각화를 학습하기 위한 완전한 예제입니다.**
**실제 비즈니스 로직과 데이터가 연동된 실습용 대시보드로 활용하세요!** 🚀