# Contract/Interface Definition for Backend

**Unit**: backend
**작성일**: 2026-02-09

---

## Unit Context
- **Stories**: AUTH-C-001~003, AUTH-A-001~003, MENU-C-001~003, ORDER-C-001~004, ORDMGT-A-001~005, TBLMGT-A-001~005, MENUMGT-A-001~006
- **Dependencies**: MySQL, AWS S3
- **Database Entities**: Store, Table, TableSession, Category, Menu, Order, OrderItem

---

## Business Logic Layer

### AuthService
```python
class AuthService:
    async def login_table(self, store_identifier: str, table_number: int, password: str) -> TokenResponse:
        """테이블 로그인"""
        # Returns: TokenResponse(access_token, token_type)
        # Raises: HTTPException(401) if invalid credentials
        
    async def login_admin(self, store_identifier: str, username: str, password: str) -> TokenResponse:
        """관리자 로그인"""
        # Returns: TokenResponse(access_token, token_type)
        # Raises: HTTPException(401) if invalid credentials
        
    def verify_token(self, token: str) -> TokenPayload:
        """토큰 검증"""
        # Returns: TokenPayload(store_id, table_id, is_admin)
        # Raises: HTTPException(401) if invalid/expired token
```

### MenuService
```python
class MenuService:
    async def get_menus(self, db: AsyncSession, store_id: int) -> list[MenuResponse]:
        """메뉴 목록 조회 (카테고리별)"""
        # Returns: list of menus grouped by category
        
    async def create_menu(self, db: AsyncSession, store_id: int, data: MenuCreate) -> MenuResponse:
        """메뉴 등록"""
        # Returns: created menu
        # Raises: HTTPException(400) if validation fails
        
    async def update_menu(self, db: AsyncSession, store_id: int, menu_id: int, data: MenuUpdate) -> MenuResponse:
        """메뉴 수정"""
        # Raises: HTTPException(404) if not found
        
    async def delete_menu(self, db: AsyncSession, store_id: int, menu_id: int) -> None:
        """메뉴 삭제 (soft delete)"""
        # Raises: HTTPException(404) if not found
        
    async def update_menu_order(self, db: AsyncSession, store_id: int, orders: list[MenuOrderUpdate]) -> None:
        """메뉴 순서 변경"""
```

### OrderService
```python
class OrderService:
    async def create_order(self, db: AsyncSession, store_id: int, table_id: int, items: list[OrderItemCreate]) -> OrderResponse:
        """주문 생성"""
        # Returns: created order with order_number
        # Raises: HTTPException(400) if menu not available
        
    async def get_orders_by_session(self, db: AsyncSession, session_id: int) -> list[OrderResponse]:
        """세션별 주문 조회"""
        
    async def get_active_orders(self, db: AsyncSession, store_id: int) -> list[TableOrderSummary]:
        """활성 주문 조회 (대시보드용)"""
        
    async def update_order_status(self, db: AsyncSession, store_id: int, order_id: int, status: str) -> OrderResponse:
        """주문 상태 변경"""
        # Raises: HTTPException(400) if invalid transition
        
    async def delete_order(self, db: AsyncSession, store_id: int, order_id: int) -> None:
        """주문 삭제"""
        # Raises: HTTPException(404) if not found
```

### TableService
```python
class TableService:
    async def ensure_session(self, db: AsyncSession, table_id: int) -> int:
        """세션 확인/생성"""
        # Returns: session_id
        
    async def complete_table(self, db: AsyncSession, store_id: int, table_id: int) -> None:
        """테이블 이용 완료"""
        # Raises: HTTPException(400) if no active session
        
    async def get_table_history(self, db: AsyncSession, store_id: int, table_id: int, date_from: date | None) -> list[OrderResponse]:
        """과거 주문 내역 조회"""
```

### SSEService
```python
class SSEService:
    def connect(self, store_id: int) -> asyncio.Queue:
        """SSE 연결"""
        # Returns: event queue for this connection
        
    def disconnect(self, store_id: int, queue: asyncio.Queue) -> None:
        """SSE 연결 해제"""
        
    async def broadcast(self, store_id: int, event: str, data: dict) -> None:
        """이벤트 브로드캐스트"""
```

### UploadService
```python
class UploadService:
    async def upload_image(self, store_id: int, file: UploadFile) -> str:
        """이미지 업로드"""
        # Returns: image URL
        # Raises: HTTPException(400) if invalid file type/size
```

---

## API Layer

### Customer Auth
- `POST /api/v1/customer/auth/login` → AuthService.login_table()

### Customer Menu
- `GET /api/v1/customer/menus` → MenuService.get_menus()

### Customer Order
- `POST /api/v1/customer/orders` → OrderService.create_order()
- `GET /api/v1/customer/orders` → OrderService.get_orders_by_session()

### Admin Auth
- `POST /api/v1/admin/auth/login` → AuthService.login_admin()

### Admin Order
- `GET /api/v1/admin/orders/stream` → SSE stream
- `PATCH /api/v1/admin/orders/{order_id}/status` → OrderService.update_order_status()
- `DELETE /api/v1/admin/orders/{order_id}` → OrderService.delete_order()

### Admin Table
- `POST /api/v1/admin/tables/{table_id}/complete` → TableService.complete_table()
- `GET /api/v1/admin/tables/{table_id}/history` → TableService.get_table_history()

### Admin Menu
- `GET /api/v1/admin/menus` → MenuService.get_menus()
- `POST /api/v1/admin/menus` → MenuService.create_menu()
- `PUT /api/v1/admin/menus/{menu_id}` → MenuService.update_menu()
- `DELETE /api/v1/admin/menus/{menu_id}` → MenuService.delete_menu()
- `PATCH /api/v1/admin/menus/order` → MenuService.update_menu_order()

### Admin Upload
- `POST /api/v1/admin/upload/image` → UploadService.upload_image()

---

## Repository Layer (SQLAlchemy ORM 직접 사용)

Simple Structure이므로 별도 Repository 클래스 없이 Service에서 직접 DB 접근.
