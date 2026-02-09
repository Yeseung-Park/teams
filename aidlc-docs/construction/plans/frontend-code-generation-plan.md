# Frontend Code Generation Plan

**Unit**: frontend
**Type**: Service (Vue.js 3 SPA)
**방식**: Standard (일반)
**작성일**: 2026-02-09

---

## Unit Context

### 기본 정보
- **Tech Stack**: Vue.js 3, Pinia, Vite, Axios
- **Workspace Root**: /Users/yonge/teams
- **Code Location**: frontend/

### Stories (40개)
- Customer Section (18): AUTH-C-001~003, MENU-C-001~003, CART-C-001~005, ORDER-C-001~004, ERR-C-001~003
- Admin Section (22): AUTH-A-001~003, ORDMGT-A-001~005, TBLMGT-A-001~005, MENUMGT-A-001~006, ERR-A-001~003

### Dependencies
- Backend API: http://localhost:8000/api/v1/

---

## Code Generation Plan

### Step 0: Project Setup
- [x] Vite + Vue 3 프로젝트 초기화
- [x] package.json 의존성 설정
- [x] vite.config.js 설정
- [x] 디렉토리 구조 생성

### Step 1: Core Services
- [x] src/services/api.js - Axios 인스턴스, 인터셉터
- [x] src/services/sse.js - SSE 연결 관리

### Step 2: Pinia Stores
- [x] src/stores/auth.js - 인증 상태 관리
- [x] src/stores/cart.js - 장바구니 상태 관리
- [x] src/stores/menu.js - 메뉴 상태 관리
- [x] src/stores/order.js - 주문 상태 관리

### Step 3: Router Setup
- [x] src/router/index.js - Vue Router 설정
- [x] Customer routes: /, /menu, /cart, /orders
- [x] Admin routes: /admin/login, /admin/dashboard, /admin/menus, /admin/tables

### Step 4: Customer Views
- [x] src/views/customer/LoginView.vue
- [x] src/views/customer/MenuView.vue
- [x] src/views/customer/CartView.vue
- [x] src/views/customer/OrdersView.vue

### Step 5: Admin Views
- [x] src/views/admin/LoginView.vue
- [x] src/views/admin/DashboardView.vue
- [x] src/views/admin/MenuManagement.vue
- [x] src/views/admin/TableManagement.vue

### Step 6: Shared Components
- [x] (Views에 통합됨)

### Step 7: App Entry
- [x] src/App.vue
- [x] src/main.js
- [x] index.html

### Step 8: Styles & Assets
- [x] (Views에 scoped style로 통합됨)

### Step 9: Documentation
- [x] README.md

---

## Story Coverage

| Step | Stories Covered |
|------|-----------------|
| Step 1 | 공통 (API 통신) |
| Step 2 | AUTH-C/A, CART-C, ORDER-C |
| Step 3 | 라우팅 |
| Step 4 | AUTH-C-001~003, MENU-C-001~003, CART-C-001~005, ORDER-C-001~004 |
| Step 5 | AUTH-A-001~003, ORDMGT-A-001~005, TBLMGT-A-001~005, MENUMGT-A-001~006 |
| Step 6 | UI 컴포넌트 |
| Step 7 | 앱 진입점 |
| Step 8 | 스타일링 |
| Step 9 | 문서화 |

---

## 예상 산출물

```
frontend/
├── src/
│   ├── views/
│   │   ├── customer/
│   │   │   ├── LoginView.vue
│   │   │   ├── MenuView.vue
│   │   │   ├── CartView.vue
│   │   │   └── OrdersView.vue
│   │   └── admin/
│   │       ├── LoginView.vue
│   │       ├── DashboardView.vue
│   │       ├── MenuManagement.vue
│   │       └── TableManagement.vue
│   ├── components/
│   │   ├── common/
│   │   └── customer/
│   │   └── admin/
│   ├── stores/
│   │   ├── auth.js
│   │   ├── cart.js
│   │   ├── menu.js
│   │   └── order.js
│   ├── services/
│   │   ├── api.js
│   │   └── sse.js
│   ├── router/
│   │   └── index.js
│   ├── assets/
│   │   └── main.css
│   ├── App.vue
│   └── main.js
├── public/
├── index.html
├── package.json
├── vite.config.js
└── README.md
```
