# TDD Code Generation Plan for Backend

**Unit**: backend
**작성일**: 2026-02-09
**Workspace Root**: /Users/yonge/teams
**Project Type**: Greenfield

---

## Plan Step 0: Project Setup & Contract Skeleton
- [x] 0.1 프로젝트 구조 생성
- [x] 0.2 requirements.txt 생성
- [x] 0.3 Database Models 생성
- [x] 0.4 Pydantic Schemas 생성
- [x] 0.5 Core 설정 (config, database, dependencies)
- [x] 0.6 Service Skeletons 생성 (NotImplementedError)
- [x] 0.7 Router Skeletons 생성
- [x] 0.8 Main app 생성

---

## Plan Step 1: AuthService (TDD)

### 1.1 AuthService.login_table()
- [x] RED: TC-AUTH-001 테스트 작성
- [x] GREEN: 최소 구현
- [x] RED: TC-AUTH-002 테스트 작성
- [x] GREEN: 에러 처리 추가
- [x] REFACTOR: 코드 정리
- [x] VERIFY: 모든 테스트 통과

### 1.2 AuthService.login_admin()
- [x] RED: TC-AUTH-003 테스트 작성
- [x] GREEN: 최소 구현
- [x] REFACTOR: 공통 로직 추출
- [x] VERIFY: 모든 테스트 통과

### 1.3 AuthService.verify_token()
- [x] RED: TC-AUTH-004 테스트 작성
- [x] GREEN: 최소 구현
- [x] RED: TC-AUTH-005 테스트 작성
- [x] GREEN: 만료 처리 추가
- [x] VERIFY: 모든 테스트 통과

---

## Plan Step 2: MenuService (TDD)

### 2.1 MenuService.get_menus()
- [x] RED: TC-MENU-001 테스트 작성
- [x] GREEN: 최소 구현
- [x] VERIFY: 테스트 통과

### 2.2 MenuService.create_menu()
- [x] RED: TC-MENU-002 테스트 작성
- [x] GREEN: 최소 구현
- [x] RED: TC-MENU-003 테스트 작성
- [x] GREEN: 검증 로직 추가
- [x] VERIFY: 모든 테스트 통과

### 2.3 MenuService.update_menu()
- [x] RED: TC-MENU-004 테스트 작성
- [x] GREEN: 최소 구현
- [x] VERIFY: 테스트 통과

### 2.4 MenuService.delete_menu()
- [x] RED: TC-MENU-005 테스트 작성
- [x] GREEN: soft delete 구현
- [x] VERIFY: 테스트 통과

---

## Plan Step 3: OrderService (TDD)

### 3.1 OrderService.create_order()
- [x] RED: TC-ORDER-001 테스트 작성
- [x] GREEN: 최소 구현
- [x] RED: TC-ORDER-002 테스트 작성
- [x] GREEN: 메뉴 검증 추가
- [x] RED: TC-ORDER-003 테스트 작성
- [x] GREEN: 빈 주문 검증 추가
- [x] REFACTOR: 주문 번호 생성 로직 분리
- [x] VERIFY: 모든 테스트 통과

### 3.2 OrderService.get_orders_by_session()
- [x] RED: TC-ORDER-004 테스트 작성
- [x] GREEN: 최소 구현
- [x] VERIFY: 테스트 통과

### 3.3 OrderService.update_order_status()
- [x] RED: TC-ORDER-005 테스트 작성
- [x] GREEN: 최소 구현
- [x] RED: TC-ORDER-006 테스트 작성
- [x] GREEN: 상태 전이 검증 추가
- [x] VERIFY: 모든 테스트 통과

### 3.4 OrderService.delete_order()
- [x] RED: TC-ORDER-007 테스트 작성
- [x] GREEN: 최소 구현
- [x] VERIFY: 테스트 통과

---

## Plan Step 4: TableService (TDD)

### 4.1 TableService.ensure_session()
- [x] RED: TC-TABLE-001 테스트 작성
- [x] GREEN: 새 세션 생성 구현
- [x] RED: TC-TABLE-002 테스트 작성
- [x] GREEN: 기존 세션 반환 구현
- [x] VERIFY: 모든 테스트 통과

### 4.2 TableService.complete_table()
- [x] RED: TC-TABLE-003 테스트 작성
- [x] GREEN: 최소 구현
- [x] RED: TC-TABLE-004 테스트 작성
- [x] GREEN: 에러 처리 추가
- [x] VERIFY: 모든 테스트 통과

### 4.3 TableService.get_table_history()
- [x] RED: TC-TABLE-005 테스트 작성
- [x] GREEN: 최소 구현
- [x] VERIFY: 테스트 통과

---

## Plan Step 5: UploadService (TDD)

### 5.1 UploadService.upload_image()
- [x] RED: TC-UPLOAD-001 테스트 작성 (mock S3)
- [x] GREEN: 최소 구현
- [x] RED: TC-UPLOAD-002 테스트 작성
- [x] GREEN: 파일 검증 추가
- [x] VERIFY: 모든 테스트 통과

---

## Plan Step 6: SSEService
- [x] SSEService 구현 (연결 관리, 브로드캐스트)
- [x] OrderService에 SSE 이벤트 연동

---

## Plan Step 7: API Routers
- [x] Customer Auth Router
- [x] Customer Menu Router
- [x] Customer Order Router
- [x] Admin Auth Router
- [x] Admin Order Router (SSE 포함)
- [x] Admin Table Router
- [x] Admin Menu Router
- [x] Admin Upload Router

---

## Plan Step 8: Integration & Final
- [x] Main app에 모든 라우터 등록
- [x] CORS 설정
- [x] Health check 엔드포인트
- [x] README.md 생성

---

## Code Location

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
│   ├── test_auth.py
│   ├── test_menu.py
│   ├── test_order.py
│   ├── test_table.py
│   └── test_upload.py
├── requirements.txt
└── README.md
```
