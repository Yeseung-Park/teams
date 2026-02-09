# Application Components

**프로젝트**: 테이블오더 서비스
**작성일**: 2026-02-09

---

## Backend Components

### 1. Auth Module
**책임**: 인증 및 세션 관리
- 테이블 로그인/자동 로그인
- 관리자 로그인
- JWT 토큰 발급/검증
- 세션 관리 (16시간)

### 2. Menu Module
**책임**: 메뉴 및 카테고리 관리
- 메뉴 CRUD
- 카테고리 관리
- 메뉴 순서 조정
- 이미지 URL 관리

### 3. Cart Module
**책임**: 장바구니 관리 (클라이언트 측)
- 프론트엔드에서 LocalStorage로 관리
- 백엔드 컴포넌트 없음

### 4. Order Module
**책임**: 주문 생성 및 조회
- 주문 생성
- 주문 내역 조회
- 주문 상태 관리
- 주문 삭제

### 5. Table Module
**책임**: 테이블 및 세션 관리
- 테이블 세션 시작/종료
- 이용 완료 처리
- 과거 주문 내역 조회

### 6. SSE Module
**책임**: 실시간 주문 스트리밍
- Server-Sent Events 연결 관리
- 주문 이벤트 브로드캐스트

### 7. Upload Module
**책임**: 파일 업로드
- S3 이미지 업로드
- 이미지 URL 반환

---

## Frontend Components (Vue.js - 단일 프로젝트)

### Customer Section (/customer/*)

#### 1. CustomerAuth
**책임**: 고객 인증 UI
- 초기 설정 폼
- 자동 로그인 처리

#### 2. MenuView
**책임**: 메뉴 표시
- 카테고리별 메뉴 목록
- 메뉴 상세 모달

#### 3. CartView
**책임**: 장바구니 UI
- 장바구니 목록
- 수량 조절
- 총 금액 표시

#### 4. OrderView
**책임**: 주문 UI
- 주문 확인/확정
- 주문 내역 조회

### Admin Section (/admin/*)

#### 5. AdminAuth
**책임**: 관리자 인증 UI
- 로그인 폼

#### 6. DashboardView
**책임**: 주문 대시보드
- 테이블별 주문 현황 (그리드)
- 실시간 업데이트 (SSE)
- 주문 상태 변경

#### 7. TableManagement
**책임**: 테이블 관리 UI
- 이용 완료 처리
- 과거 내역 조회

#### 8. MenuManagement
**책임**: 메뉴 관리 UI
- 메뉴 CRUD 폼
- 이미지 업로드
- 순서 조정

---

## Shared Components

### Frontend Shared
- **ApiClient**: Axios 기반 API 호출
- **AuthStore**: Pinia 인증 상태 관리
- **CartStore**: Pinia 장바구니 상태 관리
- **OrderStore**: Pinia 주문 상태 관리
- **SSEClient**: SSE 연결 관리

### Backend Shared
- **Database Models**: SQLAlchemy 모델
- **Schemas**: Pydantic 스키마
- **Dependencies**: FastAPI 의존성 (인증 등)
- **Config**: 환경 설정
