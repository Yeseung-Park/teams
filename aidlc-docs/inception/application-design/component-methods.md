# Component Methods

**프로젝트**: 테이블오더 서비스
**작성일**: 2026-02-09

---

## Backend API Endpoints

### Auth Module

| Method | Endpoint | Description | Input | Output |
|--------|----------|-------------|-------|--------|
| POST | /api/v1/customer/auth/login | 테이블 로그인 | store_id, table_number, password | token, session_id |
| POST | /api/v1/admin/auth/login | 관리자 로그인 | store_id, username, password | token |

### Menu Module

| Method | Endpoint | Description | Input | Output |
|--------|----------|-------------|-------|--------|
| GET | /api/v1/customer/menus | 메뉴 목록 조회 | - | menus[] |
| GET | /api/v1/admin/menus | 관리자 메뉴 목록 | - | menus[] |
| POST | /api/v1/admin/menus | 메뉴 등록 | menu_data | menu |
| PUT | /api/v1/admin/menus/{id} | 메뉴 수정 | menu_data | menu |
| DELETE | /api/v1/admin/menus/{id} | 메뉴 삭제 | - | success |
| PATCH | /api/v1/admin/menus/order | 메뉴 순서 변경 | menu_orders[] | success |

### Order Module

| Method | Endpoint | Description | Input | Output |
|--------|----------|-------------|-------|--------|
| POST | /api/v1/customer/orders | 주문 생성 | order_items[] | order |
| GET | /api/v1/customer/orders | 주문 내역 조회 | - | orders[] |
| GET | /api/v1/admin/orders/stream | 실시간 주문 스트림 (SSE) | - | EventStream |
| PATCH | /api/v1/admin/orders/{id}/status | 주문 상태 변경 | status | order |
| DELETE | /api/v1/admin/orders/{id} | 주문 삭제 | - | success |

### Table Module

| Method | Endpoint | Description | Input | Output |
|--------|----------|-------------|-------|--------|
| POST | /api/v1/admin/tables/{id}/complete | 이용 완료 | - | success |
| GET | /api/v1/admin/tables/{id}/history | 과거 내역 조회 | date_filter | orders[] |

### Upload Module

| Method | Endpoint | Description | Input | Output |
|--------|----------|-------------|-------|--------|
| POST | /api/v1/admin/upload/image | 이미지 업로드 | file | image_url |

---

## Frontend Store Methods (Pinia)

### AuthStore

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| login() | 로그인 처리 | credentials | Promise<void> |
| logout() | 로그아웃 | - | void |
| checkAuth() | 인증 상태 확인 | - | boolean |

### CartStore

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| addItem() | 장바구니 추가 | menu | void |
| removeItem() | 장바구니 삭제 | menuId | void |
| updateQuantity() | 수량 변경 | menuId, quantity | void |
| clearCart() | 장바구니 비우기 | - | void |
| getTotal() | 총 금액 계산 | - | number |

### OrderStore

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| createOrder() | 주문 생성 | items | Promise<Order> |
| fetchOrders() | 주문 내역 조회 | - | Promise<Order[]> |
| updateStatus() | 상태 변경 (관리자) | orderId, status | Promise<void> |
| deleteOrder() | 주문 삭제 (관리자) | orderId | Promise<void> |

### SSEClient

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| connect() | SSE 연결 | - | void |
| disconnect() | SSE 연결 해제 | - | void |
| onMessage() | 메시지 핸들러 등록 | callback | void |
