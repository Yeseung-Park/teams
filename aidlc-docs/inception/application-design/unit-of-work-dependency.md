# Unit of Work Dependencies

**프로젝트**: 테이블오더 서비스
**작성일**: 2026-02-09

---

## Dependency Matrix

| Unit | Depends On | Communication |
|------|------------|---------------|
| backend | MySQL, S3 | Database, AWS SDK |
| frontend | backend | REST API, SSE |

---

## Detailed Dependencies

### backend
| Dependency | Type | Purpose |
|------------|------|---------|
| MySQL | External | 데이터 저장 |
| AWS S3 | External | 이미지 저장 |
| - | - | 다른 유닛 의존성 없음 |

### frontend
| Dependency | Type | Purpose |
|------------|------|---------|
| backend | Internal | REST API 호출 |
| backend | Internal | SSE 연결 (관리자) |

---

## Communication Patterns

```
┌──────────────┐     REST API      ┌──────────────┐
│   frontend   │ ───────────────── │   backend    │
│  (Vue.js)    │                   │  (FastAPI)   │
│              │ ◄──── SSE ─────── │              │
└──────────────┘                   └──────────────┘
                                          │
                                          │
                          ┌───────────────┼───────────────┐
                          │               │               │
                          ▼               ▼               ▼
                    ┌──────────┐   ┌──────────┐   ┌──────────┐
                    │  MySQL   │   │   S3     │   │  (JWT)   │
                    │ Database │   │  Bucket  │   │  Tokens  │
                    └──────────┘   └──────────┘   └──────────┘
```

---

## Build/Deploy Order

1. **backend** - 먼저 배포 (API 서버)
2. **frontend** - 이후 배포 (backend URL 설정 필요)

---

## Integration Points

### API Endpoints
- Base URL: `http://localhost:8000/api/v1` (dev)
- Customer: `/customer/*`
- Admin: `/admin/*`

### SSE Endpoint
- URL: `/api/v1/admin/orders/stream`
- 관리자 인증 필요
