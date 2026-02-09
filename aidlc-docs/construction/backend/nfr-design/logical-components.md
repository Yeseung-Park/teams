# Logical Components - Backend

**Unit**: backend
**작성일**: 2026-02-09

---

## Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Application                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌────────┐│
│  │  Auth   │ │  Menu   │ │  Order  │ │  Table  │ │ Upload ││
│  │ Router  │ │ Router  │ │ Router  │ │ Router  │ │ Router ││
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └───┬────┘│
│       │           │           │           │          │      │
│  ┌────┴────┐ ┌────┴────┐ ┌────┴────┐ ┌────┴────┐ ┌───┴────┐│
│  │  Auth   │ │  Menu   │ │  Order  │ │  Table  │ │ Upload ││
│  │ Service │ │ Service │ │ Service │ │ Service │ │ Service││
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └───┬────┘│
│       │           │           │           │          │      │
│       └───────────┴─────┬─────┴───────────┘          │      │
│                         │                            │      │
│                   ┌─────┴─────┐              ┌───────┴────┐ │
│                   │ Database  │              │  S3 Client │ │
│                   │  Session  │              │            │ │
│                   └─────┬─────┘              └───────┬────┘ │
└─────────────────────────┼────────────────────────────┼──────┘
                          │                            │
                    ┌─────┴─────┐              ┌───────┴────┐
                    │   MySQL   │              │   AWS S3   │
                    │    RDS    │              │   Bucket   │
                    └───────────┘              └────────────┘
```

---

## Core Components

### 1. FastAPI Application
- **역할**: HTTP 요청 처리, 라우팅
- **구성**: Uvicorn ASGI 서버
- **포트**: 8000

### 2. Router Layer
- **역할**: API 엔드포인트 정의, 요청/응답 처리
- **구성**: 모듈별 APIRouter
- **책임**: 입력 검증, 응답 직렬화

### 3. Service Layer
- **역할**: 비즈니스 로직 처리
- **구성**: 모듈별 서비스 함수
- **책임**: 트랜잭션 관리, 비즈니스 규칙 적용

### 4. Database Session
- **역할**: DB 연결 관리
- **구성**: SQLAlchemy AsyncSession
- **책임**: 커넥션 풀링, 트랜잭션

---

## Infrastructure Components

### 1. MySQL Database (RDS)
- **역할**: 데이터 영속화
- **구성**: AWS RDS MySQL 8.0
- **특성**: 
  - 자동 백업 (7일)
  - 단일 AZ (MVP)

### 2. AWS S3 Bucket
- **역할**: 이미지 저장
- **구성**: 퍼블릭 읽기 버킷
- **특성**:
  - 메뉴 이미지 저장
  - CDN 없음 (MVP)

### 3. EC2 Instance
- **역할**: 애플리케이션 호스팅
- **구성**: t3.small 또는 t3.medium
- **특성**:
  - 단일 인스턴스 (MVP)
  - Elastic IP

---

## Cross-Cutting Components

### 1. JWT Authentication
- **역할**: 토큰 기반 인증
- **적용**: 모든 보호된 엔드포인트
- **구현**: FastAPI Depends

### 2. SSE Manager
- **역할**: 실시간 이벤트 브로드캐스트
- **구성**: 인메모리 연결 관리
- **특성**:
  - 매장별 연결 그룹
  - 비동기 큐 기반

### 3. Error Handler
- **역할**: 전역 예외 처리
- **구성**: FastAPI exception_handler
- **특성**: 표준화된 에러 응답

### 4. Logger
- **역할**: 애플리케이션 로깅
- **구성**: Python logging + JSON formatter
- **출력**: stdout (CloudWatch 연동 가능)

---

## Data Flow

### 주문 생성 플로우
```
Client → Router → Service → Database → SSE Manager → Admin Clients
```

### 이미지 업로드 플로우
```
Client → Router → Service → S3 Client → S3 Bucket
                     ↓
                 Database (URL 저장)
```

---

## Scaling Considerations (향후)

### 수평 확장 시
1. SSE 연결 관리 → Redis Pub/Sub
2. 세션 저장 → Redis
3. 로드 밸런서 → ALB + Sticky Session
4. 데이터베이스 → Read Replica
