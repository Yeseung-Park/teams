# Business Rules - Backend

**Unit**: backend
**작성일**: 2026-02-09

---

## 1. 인증 규칙 (Authentication)

### BR-AUTH-001: 테이블 로그인
- 매장 식별자 + 테이블 번호 + 비밀번호로 인증
- 인증 성공 시 JWT 토큰 발급 (16시간 유효)
- 비밀번호는 bcrypt로 검증

### BR-AUTH-002: 관리자 로그인
- 매장 식별자 + 사용자명 + 비밀번호로 인증
- 인증 성공 시 JWT 토큰 발급 (16시간 유효)
- 비밀번호는 bcrypt로 검증

### BR-AUTH-003: 토큰 검증
- 모든 API 요청에 JWT 토큰 필수 (로그인 제외)
- 만료된 토큰은 401 Unauthorized 반환
- 토큰에서 store_id, table_id (또는 admin 여부) 추출

---

## 2. 메뉴 규칙 (Menu)

### BR-MENU-001: 메뉴 조회
- is_available = True인 메뉴만 고객에게 표시
- display_order 순으로 정렬
- 카테고리별 그룹화

### BR-MENU-002: 메뉴 등록
- 필수 필드: menu_name, price, category_id
- price > 0 검증
- 이미지는 선택사항

### BR-MENU-003: 메뉴 삭제
- 삭제 시 is_available = False로 soft delete
- 기존 주문 내역 보존을 위해 실제 삭제 안함

### BR-MENU-004: 메뉴 순서 변경
- display_order 값 업데이트
- 같은 카테고리 내에서만 순서 의미 있음

---

## 3. 주문 규칙 (Order)

### BR-ORDER-001: 주문 생성
- 최소 1개 이상의 주문 항목 필수
- 각 메뉴의 is_available = True 검증
- 주문 번호 자동 생성 (YYYYMMDD-XXXX 형식)
- total_amount = SUM(quantity * unit_price)

### BR-ORDER-002: 주문 번호 생성
- 형식: YYYYMMDD-XXXX (예: 20260209-0001)
- 매장별, 일별 순차 번호
- 자정에 리셋

### BR-ORDER-003: 주문 상태 전이
```
pending → preparing → completed
```
- 역방향 전이 불가
- 상태 변경 시 updated_at 갱신

### BR-ORDER-004: 주문 삭제
- 관리자만 삭제 가능
- 삭제 시 테이블 총 주문액 재계산
- 실제 DB 삭제 (soft delete 아님)

### BR-ORDER-005: 주문 항목 스냅샷
- menu_name, unit_price는 주문 시점 값 저장
- 메뉴 가격 변경 시 기존 주문 영향 없음

---

## 4. 테이블/세션 규칙 (Table/Session)

### BR-TABLE-001: 세션 시작
- 첫 주문 생성 시 자동으로 세션 시작
- current_session_id가 NULL이면 새 세션 생성
- is_active = True로 설정

### BR-TABLE-002: 세션 종료 (이용 완료)
- 관리자가 이용 완료 처리 시 세션 종료
- session_end_time = 현재 시각
- is_active = False
- current_session_id = NULL

### BR-TABLE-003: 주문 조회 범위
- 고객: 현재 활성 세션의 주문만 조회
- 관리자: 모든 활성 세션의 주문 조회

### BR-TABLE-004: 과거 내역 조회
- 종료된 세션의 주문 내역 조회
- 날짜 필터링 지원
- 시간 역순 정렬

---

## 5. 실시간 알림 규칙 (SSE)

### BR-SSE-001: 연결 관리
- 관리자 인증 필요
- 매장별 연결 관리
- 연결 끊김 시 자동 정리

### BR-SSE-002: 이벤트 브로드캐스트
- 새 주문 생성 시 'new_order' 이벤트
- 주문 상태 변경 시 'order_updated' 이벤트
- 주문 삭제 시 'order_deleted' 이벤트
- 테이블 이용 완료 시 'table_reset' 이벤트

### BR-SSE-003: 이벤트 지연
- 주문 이벤트는 2초 이내 전달

---

## 6. 파일 업로드 규칙 (Upload)

### BR-UPLOAD-001: 이미지 업로드
- 허용 형식: JPEG, PNG, WebP
- 최대 크기: 5MB
- S3에 저장, URL 반환

### BR-UPLOAD-002: 파일명 생성
- UUID 기반 고유 파일명
- 원본 확장자 유지

---

## 7. 데이터 검증 규칙 (Validation)

### BR-VAL-001: 문자열 길이
- store_name: 최대 100자
- menu_name: 최대 100자
- category_name: 최대 50자

### BR-VAL-002: 숫자 범위
- price: 0 < price ≤ 10,000,000
- quantity: 1 ≤ quantity ≤ 99
- table_number: 1 ≤ table_number ≤ 999

### BR-VAL-003: 필수 필드
- 모든 NOT NULL 필드는 요청 시 필수
- 빈 문자열은 NULL과 동일하게 처리
