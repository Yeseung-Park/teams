# Test Plan for Backend

**Unit**: backend
**작성일**: 2026-02-09

---

## Unit Overview
- **Unit**: backend
- **Total Test Cases**: 25개
- **Layers**: AuthService, MenuService, OrderService, TableService, UploadService

---

## AuthService Tests

### AuthService.login_table()
- **TC-AUTH-001**: 유효한 자격증명으로 테이블 로그인
  - Given: 유효한 store_identifier, table_number, password
  - When: login_table() 호출
  - Then: JWT 토큰 반환
  - Status: ⬜ Not Started

- **TC-AUTH-002**: 잘못된 비밀번호로 테이블 로그인 실패
  - Given: 유효한 store_identifier, table_number, 잘못된 password
  - When: login_table() 호출
  - Then: HTTPException(401) 발생
  - Status: ⬜ Not Started

### AuthService.login_admin()
- **TC-AUTH-003**: 유효한 자격증명으로 관리자 로그인
  - Given: 유효한 store_identifier, username, password
  - When: login_admin() 호출
  - Then: JWT 토큰 반환 (is_admin=True)
  - Status: ⬜ Not Started

### AuthService.verify_token()
- **TC-AUTH-004**: 유효한 토큰 검증
  - Given: 유효한 JWT 토큰
  - When: verify_token() 호출
  - Then: TokenPayload 반환
  - Status: ⬜ Not Started

- **TC-AUTH-005**: 만료된 토큰 검증 실패
  - Given: 만료된 JWT 토큰
  - When: verify_token() 호출
  - Then: HTTPException(401) 발생
  - Status: ⬜ Not Started

---

## MenuService Tests

### MenuService.get_menus()
- **TC-MENU-001**: 메뉴 목록 조회
  - Given: 메뉴가 등록된 매장
  - When: get_menus() 호출
  - Then: 카테고리별 메뉴 목록 반환
  - Status: ⬜ Not Started

### MenuService.create_menu()
- **TC-MENU-002**: 유효한 데이터로 메뉴 등록
  - Given: 유효한 메뉴 데이터
  - When: create_menu() 호출
  - Then: 생성된 메뉴 반환
  - Status: ⬜ Not Started

- **TC-MENU-003**: 가격 0 이하로 메뉴 등록 실패
  - Given: price <= 0인 메뉴 데이터
  - When: create_menu() 호출
  - Then: HTTPException(400) 발생
  - Status: ⬜ Not Started

### MenuService.update_menu()
- **TC-MENU-004**: 메뉴 수정
  - Given: 존재하는 메뉴
  - When: update_menu() 호출
  - Then: 수정된 메뉴 반환
  - Status: ⬜ Not Started

### MenuService.delete_menu()
- **TC-MENU-005**: 메뉴 삭제 (soft delete)
  - Given: 존재하는 메뉴
  - When: delete_menu() 호출
  - Then: is_available=False로 변경
  - Status: ⬜ Not Started

---

## OrderService Tests

### OrderService.create_order()
- **TC-ORDER-001**: 유효한 주문 생성
  - Given: 유효한 메뉴 항목들
  - When: create_order() 호출
  - Then: 주문 번호와 함께 주문 반환
  - Status: ⬜ Not Started

- **TC-ORDER-002**: 비활성 메뉴로 주문 실패
  - Given: is_available=False인 메뉴 포함
  - When: create_order() 호출
  - Then: HTTPException(400) 발생
  - Status: ⬜ Not Started

- **TC-ORDER-003**: 빈 주문 항목으로 주문 실패
  - Given: 빈 items 리스트
  - When: create_order() 호출
  - Then: HTTPException(400) 발생
  - Status: ⬜ Not Started

### OrderService.get_orders_by_session()
- **TC-ORDER-004**: 세션별 주문 조회
  - Given: 주문이 있는 세션
  - When: get_orders_by_session() 호출
  - Then: 해당 세션의 주문 목록 반환
  - Status: ⬜ Not Started

### OrderService.update_order_status()
- **TC-ORDER-005**: 주문 상태 변경 (pending → preparing)
  - Given: pending 상태의 주문
  - When: update_order_status(status='preparing') 호출
  - Then: preparing 상태로 변경
  - Status: ⬜ Not Started

- **TC-ORDER-006**: 잘못된 상태 전이 실패 (completed → pending)
  - Given: completed 상태의 주문
  - When: update_order_status(status='pending') 호출
  - Then: HTTPException(400) 발생
  - Status: ⬜ Not Started

### OrderService.delete_order()
- **TC-ORDER-007**: 주문 삭제
  - Given: 존재하는 주문
  - When: delete_order() 호출
  - Then: 주문 삭제됨
  - Status: ⬜ Not Started

---

## TableService Tests

### TableService.ensure_session()
- **TC-TABLE-001**: 새 세션 생성
  - Given: 활성 세션이 없는 테이블
  - When: ensure_session() 호출
  - Then: 새 세션 생성 및 session_id 반환
  - Status: ⬜ Not Started

- **TC-TABLE-002**: 기존 세션 반환
  - Given: 활성 세션이 있는 테이블
  - When: ensure_session() 호출
  - Then: 기존 session_id 반환
  - Status: ⬜ Not Started

### TableService.complete_table()
- **TC-TABLE-003**: 테이블 이용 완료
  - Given: 활성 세션이 있는 테이블
  - When: complete_table() 호출
  - Then: 세션 종료, current_session_id=NULL
  - Status: ⬜ Not Started

- **TC-TABLE-004**: 활성 세션 없이 이용 완료 실패
  - Given: 활성 세션이 없는 테이블
  - When: complete_table() 호출
  - Then: HTTPException(400) 발생
  - Status: ⬜ Not Started

### TableService.get_table_history()
- **TC-TABLE-005**: 과거 주문 내역 조회
  - Given: 종료된 세션의 주문 내역
  - When: get_table_history() 호출
  - Then: 과거 주문 목록 반환
  - Status: ⬜ Not Started

---

## UploadService Tests

### UploadService.upload_image()
- **TC-UPLOAD-001**: 유효한 이미지 업로드
  - Given: JPEG 이미지 파일
  - When: upload_image() 호출
  - Then: S3 URL 반환
  - Status: ⬜ Not Started

- **TC-UPLOAD-002**: 잘못된 파일 형식 업로드 실패
  - Given: PDF 파일
  - When: upload_image() 호출
  - Then: HTTPException(400) 발생
  - Status: ⬜ Not Started

---

## Requirements Coverage

| Story ID | Test Cases | Status |
|----------|------------|--------|
| AUTH-C-001~003 | TC-AUTH-001~005 | ⬜ Pending |
| MENU-C-001~003 | TC-MENU-001 | ⬜ Pending |
| MENUMGT-A-001~006 | TC-MENU-002~005 | ⬜ Pending |
| ORDER-C-001~004 | TC-ORDER-001~004 | ⬜ Pending |
| ORDMGT-A-001~005 | TC-ORDER-005~007 | ⬜ Pending |
| TBLMGT-A-001~005 | TC-TABLE-001~005 | ⬜ Pending |
| MENUMGT-A-003 | TC-UPLOAD-001~002 | ⬜ Pending |
