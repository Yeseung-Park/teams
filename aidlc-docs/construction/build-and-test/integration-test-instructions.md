# Integration Test Instructions

## Purpose

Backend API와 Frontend 간의 통합 테스트를 수행합니다.

---

## Test Environment Setup

### 1. Backend 서버 실행

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend 서버 실행

```bash
cd frontend
npm run dev
```

### 3. 테스트 데이터 준비

```sql
-- MySQL에서 실행
USE tableorder;

-- 테스트 매장 생성
INSERT INTO stores (store_identifier, name, password_hash) 
VALUES ('test-store', '테스트 매장', '$2b$12$...');  -- bcrypt hash of 'password'

-- 테스트 테이블 생성
INSERT INTO tables (store_id, table_number) VALUES (1, 1), (1, 2), (1, 3);

-- 관리자 계정 생성
INSERT INTO admins (store_id, username, password_hash)
VALUES (1, 'admin', '$2b$12$...');  -- bcrypt hash of 'admin123'

-- 테스트 메뉴 생성
INSERT INTO menus (store_id, name, category, price, is_available)
VALUES 
  (1, '아메리카노', '커피', 4500, true),
  (1, '카페라떼', '커피', 5000, true),
  (1, '치즈케이크', '디저트', 6500, true);
```

---

## Integration Test Scenarios

### Scenario 1: Customer 주문 플로우

**Description**: 고객이 로그인 → 메뉴 조회 → 장바구니 추가 → 주문 생성

**Test Steps**:
1. `http://localhost:3000` 접속
2. 매장 코드: `test-store`, 테이블: `1`, 비밀번호: `password` 입력
3. 로그인 성공 → 메뉴 화면 이동 확인
4. 메뉴 클릭하여 장바구니 추가
5. 장바구니 화면에서 수량 조절
6. "주문하기" 버튼 클릭
7. 주문 내역 화면에서 주문 확인

**Expected Results**:
- 로그인 후 JWT 토큰이 localStorage에 저장됨
- 메뉴 목록이 API에서 정상 로드됨
- 주문 생성 후 주문 내역에 표시됨
- 주문 상태가 "대기중"으로 표시됨

---

### Scenario 2: Admin 주문 관리 플로우

**Description**: 관리자가 로그인 → 실시간 주문 수신 → 상태 변경

**Test Steps**:
1. `http://localhost:3000/admin/login` 접속
2. 매장 코드: `test-store`, 아이디: `admin`, 비밀번호: `admin123` 입력
3. 로그인 성공 → 대시보드 이동 확인
4. SSE 연결 확인 (개발자 도구 Network 탭)
5. 다른 브라우저에서 Customer로 주문 생성
6. 대시보드에 새 주문 실시간 표시 확인
7. 주문 상태를 "준비중" → "완료"로 변경
8. Customer 화면에서 상태 변경 확인

**Expected Results**:
- 관리자 로그인 후 대시보드 표시
- SSE 연결이 유지됨
- 새 주문이 실시간으로 표시됨
- 상태 변경이 즉시 반영됨

---

### Scenario 3: Admin 메뉴 관리 플로우

**Description**: 관리자가 메뉴 CRUD 수행

**Test Steps**:
1. Admin 로그인 후 "메뉴" 탭 클릭
2. "메뉴 추가" 버튼 클릭
3. 메뉴 정보 입력 후 저장
4. 메뉴 목록에 새 메뉴 표시 확인
5. 메뉴 수정 버튼 클릭 → 가격 변경 → 저장
6. 메뉴 삭제 버튼 클릭 → 확인
7. Customer 화면에서 메뉴 변경 확인

**Expected Results**:
- 메뉴 CRUD가 정상 동작
- 변경사항이 Customer 화면에 반영됨

---

### Scenario 4: 테이블 이용 완료 플로우

**Description**: 관리자가 테이블 이용 완료 처리

**Test Steps**:
1. Admin 로그인 후 "테이블" 탭 클릭
2. 이용중인 테이블의 "이용완료" 버튼 클릭
3. 테이블 상태가 "비어있음"으로 변경 확인
4. Customer 세션이 종료되어 재로그인 필요 확인

**Expected Results**:
- 테이블 세션이 종료됨
- Customer 토큰이 무효화됨

---

## API Integration Tests (curl)

### Auth API
```bash
# Customer 로그인
curl -X POST http://localhost:8000/api/v1/auth/customer/login \
  -H "Content-Type: application/json" \
  -d '{"store_identifier":"test-store","table_number":1,"password":"password"}'

# Admin 로그인
curl -X POST http://localhost:8000/api/v1/auth/admin/login \
  -H "Content-Type: application/json" \
  -d '{"store_identifier":"test-store","username":"admin","password":"admin123"}'
```

### Menu API
```bash
# 메뉴 조회 (Customer)
curl -X GET http://localhost:8000/api/v1/customer/menus \
  -H "Authorization: Bearer <token>"
```

### Order API
```bash
# 주문 생성
curl -X POST http://localhost:8000/api/v1/customer/orders \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"items":[{"menu_id":1,"quantity":2}]}'
```

---

## Cleanup

테스트 완료 후:
```sql
-- 테스트 데이터 삭제
DELETE FROM order_items;
DELETE FROM orders;
DELETE FROM table_sessions;
DELETE FROM menus WHERE store_id = 1;
DELETE FROM admins WHERE store_id = 1;
DELETE FROM tables WHERE store_id = 1;
DELETE FROM stores WHERE store_identifier = 'test-store';
```
