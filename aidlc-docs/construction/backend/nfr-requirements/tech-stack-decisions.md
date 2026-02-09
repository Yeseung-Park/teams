# Tech Stack Decisions - Backend

**Unit**: backend
**작성일**: 2026-02-09

---

## Core Stack

| Category | Technology | Version | Rationale |
|----------|------------|---------|-----------|
| Language | Python | 3.11+ | 빠른 개발, 풍부한 라이브러리 |
| Framework | FastAPI | 0.100+ | 비동기 지원, 자동 문서화, 타입 힌트 |
| ORM | SQLAlchemy | 2.0+ | 성숙한 ORM, 비동기 지원 |
| Database | MySQL | 8.0+ | 관계형 DB, ACID 보장, 널리 사용 |

---

## Dependencies

### Core Dependencies
| Package | Purpose |
|---------|---------|
| fastapi | 웹 프레임워크 |
| uvicorn | ASGI 서버 |
| sqlalchemy | ORM |
| aiomysql | MySQL 비동기 드라이버 |
| pydantic | 데이터 검증 |
| pydantic-settings | 환경 설정 관리 |

### Authentication
| Package | Purpose |
|---------|---------|
| python-jose | JWT 토큰 생성/검증 |
| passlib[bcrypt] | 비밀번호 해싱 |

### AWS Integration
| Package | Purpose |
|---------|---------|
| boto3 | AWS SDK (S3 업로드) |

### Utilities
| Package | Purpose |
|---------|---------|
| python-multipart | 파일 업로드 처리 |
| python-dotenv | 환경 변수 로드 |

---

## Development Dependencies

| Package | Purpose |
|---------|---------|
| pytest | 테스트 프레임워크 |
| pytest-asyncio | 비동기 테스트 |
| httpx | 테스트용 HTTP 클라이언트 |

---

## Infrastructure

| Component | Service | Rationale |
|-----------|---------|-----------|
| Compute | AWS EC2 | 단일 인스턴스 (MVP) |
| Database | AWS RDS MySQL | 관리형 DB, 자동 백업 |
| Storage | AWS S3 | 이미지 저장, 확장성 |

---

## Configuration

### Environment Variables
```
# Database
DATABASE_URL=mysql+aiomysql://user:pass@host:3306/dbname

# JWT
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=16

# AWS
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_S3_BUCKET=your-bucket
AWS_REGION=ap-northeast-2

# App
DEBUG=false
CORS_ORIGINS=https://your-domain.com
```

---

## Decision Rationale

### FastAPI 선택 이유
1. 비동기 지원 (SSE에 필수)
2. 자동 OpenAPI 문서 생성
3. Pydantic 통합 (타입 안전성)
4. 높은 성능

### SQLAlchemy 2.0 선택 이유
1. 비동기 지원 (asyncio)
2. 타입 힌트 지원
3. 성숙한 생태계

### MySQL 선택 이유
1. 요구사항에서 지정
2. 관계형 데이터 모델에 적합
3. AWS RDS 지원
