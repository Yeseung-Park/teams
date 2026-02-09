# NFR Design Patterns - Backend

**Unit**: backend
**작성일**: 2026-02-09

---

## 1. 인증 패턴 (Authentication)

### JWT Token Pattern
```python
# 토큰 구조
{
    "sub": "table:{table_id}" | "admin:{store_id}",
    "store_id": int,
    "table_id": int | null,  # 테이블 로그인 시
    "is_admin": bool,
    "exp": datetime  # 16시간 후
}
```

### 적용
- 모든 API에 JWT 검증 미들웨어
- 토큰에서 컨텍스트 추출 (store_id, table_id, is_admin)

---

## 2. 에러 처리 패턴 (Error Handling)

### Standardized Error Response
```python
{
    "detail": "에러 메시지",
    "error_code": "ERROR_CODE",
    "timestamp": "ISO8601"
}
```

### HTTP Status Codes
| Code | Usage |
|------|-------|
| 400 | 입력 검증 실패 |
| 401 | 인증 실패/토큰 만료 |
| 403 | 권한 없음 |
| 404 | 리소스 없음 |
| 500 | 서버 내부 오류 |

---

## 3. 데이터베이스 패턴 (Database)

### Connection Pool
```python
# SQLAlchemy async engine
engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600
)
```

### Repository Pattern
- 각 모듈에서 직접 DB 접근 (Simple Structure)
- SQLAlchemy 세션 의존성 주입

### N+1 Prevention
```python
# Eager loading 사용
query = select(Order).options(
    selectinload(Order.items)
)
```

---

## 4. SSE 패턴 (Server-Sent Events)

### Connection Management
```python
# 매장별 연결 관리
connections: dict[int, list[Queue]] = {}

async def broadcast(store_id: int, event: dict):
    for queue in connections.get(store_id, []):
        await queue.put(event)
```

### Event Format
```python
{
    "event": "new_order" | "order_updated" | "order_deleted" | "table_reset",
    "data": { ... }
}
```

### Heartbeat
- 30초마다 ping 이벤트 전송
- 연결 유지 및 끊김 감지

---

## 5. 파일 업로드 패턴 (File Upload)

### S3 Direct Upload
```python
async def upload_to_s3(file: UploadFile) -> str:
    key = f"menus/{store_id}/{uuid4()}{ext}"
    await s3_client.upload_fileobj(file.file, bucket, key)
    return f"https://{bucket}.s3.{region}.amazonaws.com/{key}"
```

### Validation
- Content-Type 검증 (image/jpeg, image/png, image/webp)
- 파일 크기 검증 (≤ 5MB)

---

## 6. 로깅 패턴 (Logging)

### Structured Logging
```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module
        })
```

### Log Levels
- ERROR: 예외, 실패
- WARNING: 비정상 상황
- INFO: 주요 이벤트 (주문 생성, 상태 변경)
- DEBUG: 상세 디버깅 (개발 환경)

---

## 7. 설정 관리 패턴 (Configuration)

### Pydantic Settings
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 16
    aws_s3_bucket: str
    debug: bool = False
    
    class Config:
        env_file = ".env"
```

---

## 8. 의존성 주입 패턴 (Dependency Injection)

### FastAPI Dependencies
```python
# 데이터베이스 세션
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

# 현재 사용자
async def get_current_user(token: str = Depends(oauth2_scheme)):
    return decode_token(token)

# 관리자 전용
async def get_admin_user(user = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(403, "Admin required")
    return user
```
