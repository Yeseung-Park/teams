# Component Dependencies

**프로젝트**: 테이블오더 서비스
**작성일**: 2026-02-09

---

## Backend Dependency Matrix

| Component | Depends On |
|-----------|------------|
| AuthService | Models, JWT, bcrypt |
| MenuService | Models |
| OrderService | Models, SSEService, MenuService |
| TableService | Models, OrderService |
| SSEService | asyncio |
| UploadService | boto3 |

---

## Frontend Dependency Matrix

| Component | Depends On |
|-----------|------------|
| AuthStore | ApiService |
| CartStore | LocalStorage |
| OrderStore | ApiService, SSEService |
| MenuView | CartStore |
| CartView | CartStore, OrderStore |
| OrderView | OrderStore |
| DashboardView | OrderStore, SSEService |
| MenuManagement | ApiService |

---

## Data Flow

### Customer Flow
```
MenuView → CartStore → OrderView → OrderStore → Backend API
```

### Admin Flow
```
DashboardView ← SSEService ← Backend SSE
DashboardView → OrderStore → Backend API
```

---

## Communication Patterns

### REST API
- Customer ↔ Backend: 메뉴 조회, 주문 생성/조회
- Admin ↔ Backend: 메뉴 관리, 주문 관리, 테이블 관리

### Server-Sent Events (SSE)
- Backend → Admin: 실시간 주문 알림
- 단방향 통신 (서버 → 클라이언트)

### Local Storage
- Customer: 장바구니 데이터 (CartStore)
- Customer/Admin: 인증 토큰 (AuthStore)

---

## Module Structure

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

frontend/
├── src/
│   ├── views/
│   │   ├── customer/
│   │   │   ├── MenuView.vue
│   │   │   ├── CartView.vue
│   │   │   └── OrderView.vue
│   │   └── admin/
│   │       ├── DashboardView.vue
│   │       ├── MenuManagement.vue
│   │       └── TableManagement.vue
│   ├── stores/
│   │   ├── auth.js
│   │   ├── cart.js
│   │   └── order.js
│   ├── services/
│   │   ├── api.js
│   │   └── sse.js
│   ├── router/
│   │   └── index.js
│   └── main.js
```
