# Unit of Work Definitions

**프로젝트**: 테이블오더 서비스
**작성일**: 2026-02-09

---

## Unit Overview

| Unit | Type | Description |
|------|------|-------------|
| backend | Service | FastAPI 백엔드 API 서버 |
| frontend | Service | Vue.js 프론트엔드 (Customer + Admin) |

---

## Unit 1: backend

### 기본 정보
- **Name**: backend
- **Type**: Service (독립 배포)
- **Tech Stack**: Python 3.11+, FastAPI, SQLAlchemy, MySQL
- **Port**: 8000

### 책임
- REST API 제공 (Customer, Admin)
- 데이터베이스 연동
- 인증/인가 처리
- 실시간 주문 스트리밍 (SSE)
- S3 이미지 업로드

### 모듈 구성
| Module | 책임 |
|--------|------|
| auth | 인증/세션 관리 |
| menu | 메뉴 CRUD |
| order | 주문 생성/관리 |
| table | 테이블/세션 관리 |
| sse | 실시간 이벤트 |
| upload | 파일 업로드 |
| models | 데이터베이스 모델 |
| core | 설정, DB 연결, 의존성 |

### 디렉토리 구조
```
backend/
├── app/
│   ├── auth/
│   │   ├── router.py
│   │   ├── service.py
│   │   └── schemas.py
│   ├── menu/
│   │   ├── router.py
│   │   ├── service.py
│   │   └── schemas.py
│   ├── order/
│   │   ├── router.py
│   │   ├── service.py
│   │   └── schemas.py
│   ├── table/
│   │   ├── router.py
│   │   ├── service.py
│   │   └── schemas.py
│   ├── upload/
│   │   ├── router.py
│   │   └── service.py
│   ├── sse/
│   │   └── service.py
│   ├── models/
│   │   └── models.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── dependencies.py
│   └── main.py
├── tests/
├── requirements.txt
└── README.md
```

---

## Unit 2: frontend

### 기본 정보
- **Name**: frontend
- **Type**: Service (독립 배포)
- **Tech Stack**: Vue.js 3, Pinia, Vite, Axios
- **Port**: 3000 (dev), 80 (prod)

### 책임
- 고객용 UI (메뉴 조회, 장바구니, 주문)
- 관리자용 UI (대시보드, 메뉴 관리, 테이블 관리)
- 상태 관리 (Pinia)
- API 통신
- SSE 연결 (관리자)

### 섹션 구성
| Section | Route | 책임 |
|---------|-------|------|
| Customer | /customer/* | 고객 주문 인터페이스 |
| Admin | /admin/* | 관리자 대시보드 |

### 디렉토리 구조
```
frontend/
├── src/
│   ├── views/
│   │   ├── customer/
│   │   │   ├── LoginView.vue
│   │   │   ├── MenuView.vue
│   │   │   ├── CartView.vue
│   │   │   └── OrderView.vue
│   │   └── admin/
│   │       ├── LoginView.vue
│   │       ├── DashboardView.vue
│   │       ├── MenuManagement.vue
│   │       └── TableManagement.vue
│   ├── components/
│   │   ├── customer/
│   │   └── admin/
│   ├── stores/
│   │   ├── auth.js
│   │   ├── cart.js
│   │   └── order.js
│   ├── services/
│   │   ├── api.js
│   │   └── sse.js
│   ├── router/
│   │   └── index.js
│   ├── App.vue
│   └── main.js
├── public/
├── package.json
├── vite.config.js
└── README.md
```

---

## 배포 구성

### 개발 환경
- backend: `uvicorn app.main:app --reload --port 8000`
- frontend: `npm run dev` (Vite dev server, port 3000)

### 프로덕션 환경
- backend: EC2에서 uvicorn/gunicorn 실행
- frontend: 빌드 후 정적 파일 서빙 (Nginx 또는 S3+CloudFront)
