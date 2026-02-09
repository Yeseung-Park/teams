# Unit of Work Story Map

**프로젝트**: 테이블오더 서비스
**작성일**: 2026-02-09

---

## Story to Unit Mapping

### backend (22 stories)

| Story ID | Story Name | Module |
|----------|------------|--------|
| AUTH-C-001 | 테이블 초기 설정 | auth |
| AUTH-C-002 | 자동 로그인 | auth |
| AUTH-C-003 | 세션 만료 시 재로그인 | auth |
| AUTH-A-001 | 관리자 로그인 | auth |
| AUTH-A-002 | 관리자 세션 유지 | auth |
| AUTH-A-003 | 관리자 자동 로그아웃 | auth |
| MENU-C-001 | 메뉴 목록 조회 | menu |
| MENU-C-002 | 카테고리별 메뉴 필터링 | menu |
| MENU-C-003 | 메뉴 상세 정보 조회 | menu |
| ORDER-C-001 | 주문 생성 | order |
| ORDER-C-002 | 주문 확정 | order |
| ORDER-C-003 | 주문 내역 조회 | order |
| ORDER-C-004 | 주문 상태 확인 | order |
| ORDMGT-A-001 | 실시간 주문 수신 | sse, order |
| ORDMGT-A-002 | 테이블별 주문 현황 조회 | order |
| ORDMGT-A-003 | 주문 상세 조회 | order |
| ORDMGT-A-004 | 주문 상태 변경 | order |
| ORDMGT-A-005 | 주문 삭제 | order |
| TBLMGT-A-001 | 테이블 세션 시작 | table |
| TBLMGT-A-002 | 테이블 이용 완료 | table |
| TBLMGT-A-003 | 테이블 초기화 | table |
| TBLMGT-A-004 | 과거 주문 내역 조회 | table |
| TBLMGT-A-005 | 과거 내역 상세 조회 | table |
| MENUMGT-A-001 | 메뉴 목록 조회 | menu |
| MENUMGT-A-002 | 메뉴 등록 | menu |
| MENUMGT-A-003 | 메뉴 이미지 업로드 | upload |
| MENUMGT-A-004 | 메뉴 수정 | menu |
| MENUMGT-A-005 | 메뉴 삭제 | menu |
| MENUMGT-A-006 | 메뉴 순서 조정 | menu |

### frontend (40 stories - 전체)

| Story ID | Story Name | Section |
|----------|------------|---------|
| AUTH-C-001 | 테이블 초기 설정 | customer |
| AUTH-C-002 | 자동 로그인 | customer |
| AUTH-C-003 | 세션 만료 시 재로그인 | customer |
| AUTH-A-001 | 관리자 로그인 | admin |
| AUTH-A-002 | 관리자 세션 유지 | admin |
| AUTH-A-003 | 관리자 자동 로그아웃 | admin |
| MENU-C-001 | 메뉴 목록 조회 | customer |
| MENU-C-002 | 카테고리별 메뉴 필터링 | customer |
| MENU-C-003 | 메뉴 상세 정보 조회 | customer |
| CART-C-001 | 메뉴 장바구니 추가 | customer |
| CART-C-002 | 장바구니 수량 증가 | customer |
| CART-C-003 | 장바구니 수량 감소 | customer |
| CART-C-004 | 장바구니 항목 삭제 | customer |
| CART-C-005 | 장바구니 비우기 | customer |
| ORDER-C-001 | 주문 생성 | customer |
| ORDER-C-002 | 주문 확정 | customer |
| ORDER-C-003 | 주문 내역 조회 | customer |
| ORDER-C-004 | 주문 상태 확인 | customer |
| ORDMGT-A-001 | 실시간 주문 수신 | admin |
| ORDMGT-A-002 | 테이블별 주문 현황 조회 | admin |
| ORDMGT-A-003 | 주문 상세 조회 | admin |
| ORDMGT-A-004 | 주문 상태 변경 | admin |
| ORDMGT-A-005 | 주문 삭제 | admin |
| TBLMGT-A-001 | 테이블 세션 시작 | admin |
| TBLMGT-A-002 | 테이블 이용 완료 | admin |
| TBLMGT-A-003 | 테이블 초기화 | admin |
| TBLMGT-A-004 | 과거 주문 내역 조회 | admin |
| TBLMGT-A-005 | 과거 내역 상세 조회 | admin |
| MENUMGT-A-001 | 메뉴 목록 조회 | admin |
| MENUMGT-A-002 | 메뉴 등록 | admin |
| MENUMGT-A-003 | 메뉴 이미지 업로드 | admin |
| MENUMGT-A-004 | 메뉴 수정 | admin |
| MENUMGT-A-005 | 메뉴 삭제 | admin |
| MENUMGT-A-006 | 메뉴 순서 조정 | admin |
| ERR-C-001 | 로그인 실패 처리 | customer |
| ERR-C-002 | 주문 실패 처리 | customer |
| ERR-C-003 | 네트워크 오류 처리 | customer |
| ERR-A-001 | 로그인 실패 처리 | admin |
| ERR-A-002 | 주문 처리 실패 | admin |
| ERR-A-003 | SSE 연결 끊김 처리 | admin |

---

## Summary

| Unit | Total Stories | Customer | Admin |
|------|---------------|----------|-------|
| backend | 28 | 10 | 18 |
| frontend | 40 | 18 | 22 |

**Note**: 일부 스토리는 backend와 frontend 모두에서 구현 필요 (API + UI)
