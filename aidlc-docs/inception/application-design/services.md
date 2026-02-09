# Services Design

**프로젝트**: 테이블오더 서비스
**작성일**: 2026-02-09
**아키텍처**: Simple Structure (기능별 모듈 분리)

---

## Backend Service Layer

### AuthService
**책임**: 인증 비즈니스 로직

**주요 기능**:
- 테이블 인증 (store_id + table_number + password)
- 관리자 인증 (store_id + username + password)
- JWT 토큰 생성/검증
- 세션 생성/갱신

**의존성**: Database Models, JWT Library, bcrypt

---

### MenuService
**책임**: 메뉴 비즈니스 로직

**주요 기능**:
- 메뉴 CRUD 처리
- 카테고리별 메뉴 조회
- 메뉴 순서 관리
- 메뉴 가용성 검증

**의존성**: Database Models

---

### OrderService
**책임**: 주문 비즈니스 로직

**주요 기능**:
- 주문 생성 (메뉴 검증, 금액 계산)
- 주문 상태 전이 (대기중 → 준비중 → 완료)
- 주문 삭제 및 금액 재계산
- 세션별 주문 조회

**의존성**: Database Models, SSEService

---

### TableService
**책임**: 테이블/세션 비즈니스 로직

**주요 기능**:
- 테이블 세션 시작 (첫 주문 시)
- 이용 완료 처리 (세션 종료, 이력 이동)
- 과거 주문 내역 조회

**의존성**: Database Models, OrderService

---

### SSEService
**책임**: 실시간 이벤트 관리

**주요 기능**:
- 클라이언트 연결 관리
- 주문 이벤트 브로드캐스트
- 연결 상태 모니터링

**의존성**: asyncio, FastAPI StreamingResponse

---

### UploadService
**책임**: 파일 업로드 처리

**주요 기능**:
- S3 이미지 업로드
- 파일 검증 (타입, 크기)
- URL 생성

**의존성**: boto3 (AWS SDK)

---

## Service Interaction Flow

### 주문 생성 플로우
```
Customer → OrderService.create_order()
  → MenuService.validate_menus()
  → TableService.ensure_session()
  → Database.save()
  → SSEService.broadcast_new_order()
```

### 이용 완료 플로우
```
Admin → TableService.complete_table()
  → OrderService.archive_orders()
  → Database.update_session()
  → SSEService.broadcast_table_reset()
```

---

## Frontend Service Layer

### ApiService
**책임**: HTTP 통신 추상화

**구현**: Axios 인스턴스
- Base URL 설정
- 인터셉터 (토큰 주입, 에러 처리)
- 요청/응답 변환

### SSEService
**책임**: 실시간 연결 관리

**구현**: EventSource API
- 연결 수립/해제
- 재연결 로직
- 이벤트 핸들링
