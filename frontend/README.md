# Table Order Service - Frontend

테이블오더 서비스 프론트엔드 (Vue.js 3)

## Tech Stack

- Vue.js 3
- Pinia (상태 관리)
- Vue Router
- Axios
- Vite

## Setup

### 1. 의존성 설치

```bash
npm install
```

### 2. 개발 서버 실행

```bash
npm run dev
```

서버가 http://localhost:3000 에서 실행됩니다.

### 3. 프로덕션 빌드

```bash
npm run build
```

## Routes

### Customer
- `/` - 테이블 로그인
- `/menu` - 메뉴 조회
- `/cart` - 장바구니
- `/orders` - 주문 내역

### Admin
- `/admin/login` - 관리자 로그인
- `/admin` - 주문 대시보드
- `/admin/menus` - 메뉴 관리
- `/admin/tables` - 테이블 관리

## Project Structure

```
src/
├── views/
│   ├── customer/       # 고객 화면
│   └── admin/          # 관리자 화면
├── stores/             # Pinia 스토어
├── services/           # API, SSE 서비스
├── router/             # Vue Router
├── App.vue
└── main.js
```

## Environment

Backend API는 Vite proxy를 통해 `/api` 경로로 연결됩니다.
`vite.config.js`에서 proxy 설정을 확인하세요.
