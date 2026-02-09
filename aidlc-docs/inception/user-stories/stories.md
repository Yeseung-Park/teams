# User Stories

**프로젝트**: 테이블오더 서비스
**작성일**: 2026-02-09
**분류 방식**: Feature 기반
**세분화 수준**: Fine

---

## 1. 인증 (Authentication)

### 고객 인증

#### AUTH-C-001: 테이블 초기 설정
**As a** 테이블 고객  
**I want** 태블릿에서 매장/테이블 정보를 초기 설정할 수 있다  
**So that** 이후 자동 로그인이 가능하다

**Acceptance Criteria:**
- Given 초기 설정되지 않은 태블릿
- When 매장 식별자, 테이블 번호, 비밀번호 입력
- Then 정보가 로컬에 저장되고 로그인 완료
- And 16시간 세션 생성

#### AUTH-C-002: 자동 로그인
**As a** 테이블 고객  
**I want** 태블릿 접속 시 자동으로 로그인된다  
**So that** 별도 입력 없이 바로 메뉴를 볼 수 있다

**Acceptance Criteria:**
- Given 초기 설정 완료된 태블릿
- When 앱/페이지 접속
- Then 저장된 정보로 자동 로그인
- And 메뉴 화면으로 이동

#### AUTH-C-003: 세션 만료 시 재로그인
**As a** 테이블 고객  
**I want** 세션 만료 시 자동으로 재로그인된다  
**So that** 서비스 이용이 중단되지 않는다

**Acceptance Criteria:**
- Given 16시간 세션 만료
- When 다음 요청 발생
- Then 저장된 정보로 자동 재로그인
- And 요청 정상 처리

### 관리자 인증

#### AUTH-A-001: 관리자 로그인
**As a** 매장 관리자  
**I want** 매장 식별자와 계정으로 로그인할 수 있다  
**So that** 관리자 기능에 접근할 수 있다

**Acceptance Criteria:**
- Given 관리자 로그인 페이지
- When 매장 식별자, 사용자명, 비밀번호 입력
- Then 인증 성공 시 대시보드로 이동
- And 16시간 세션 생성

#### AUTH-A-002: 관리자 세션 유지
**As a** 매장 관리자  
**I want** 브라우저 새로고침 후에도 로그인 상태가 유지된다  
**So that** 반복 로그인 없이 업무를 볼 수 있다

**Acceptance Criteria:**
- Given 로그인된 관리자
- When 브라우저 새로고침
- Then 로그인 상태 유지
- And 현재 페이지 유지

#### AUTH-A-003: 관리자 자동 로그아웃
**As a** 매장 관리자  
**I want** 16시간 후 자동 로그아웃된다  
**So that** 보안이 유지된다

**Acceptance Criteria:**
- Given 16시간 경과한 세션
- When 다음 요청 발생
- Then 로그인 페이지로 리다이렉트
- And 세션 정보 삭제

---

## 2. 메뉴 (Menu)

#### MENU-C-001: 메뉴 목록 조회
**As a** 테이블 고객  
**I want** 전체 메뉴 목록을 볼 수 있다  
**So that** 주문할 메뉴를 선택할 수 있다

**Acceptance Criteria:**
- Given 로그인된 고객
- When 메뉴 화면 접속
- Then 카테고리별 메뉴 목록 표시
- And 메뉴명, 가격, 이미지 표시

#### MENU-C-002: 카테고리별 메뉴 필터링
**As a** 테이블 고객  
**I want** 카테고리를 선택하여 메뉴를 필터링할 수 있다  
**So that** 원하는 종류의 메뉴를 빠르게 찾을 수 있다

**Acceptance Criteria:**
- Given 메뉴 목록 화면
- When 특정 카테고리 선택
- Then 해당 카테고리 메뉴만 표시
- And 다른 카테고리로 빠르게 전환 가능

#### MENU-C-003: 메뉴 상세 정보 조회
**As a** 테이블 고객  
**I want** 메뉴의 상세 정보를 볼 수 있다  
**So that** 주문 전 메뉴 정보를 확인할 수 있다

**Acceptance Criteria:**
- Given 메뉴 목록 화면
- When 특정 메뉴 선택
- Then 메뉴명, 가격, 설명, 이미지 표시
- And 장바구니 추가 버튼 표시

---

## 3. 장바구니 (Cart)

#### CART-C-001: 메뉴 장바구니 추가
**As a** 테이블 고객  
**I want** 메뉴를 장바구니에 추가할 수 있다  
**So that** 여러 메뉴를 모아서 주문할 수 있다

**Acceptance Criteria:**
- Given 메뉴 상세 화면
- When 장바구니 추가 버튼 클릭
- Then 해당 메뉴가 장바구니에 추가
- And 장바구니 아이콘에 수량 표시

#### CART-C-002: 장바구니 수량 증가
**As a** 테이블 고객  
**I want** 장바구니 항목의 수량을 증가시킬 수 있다  
**So that** 같은 메뉴를 여러 개 주문할 수 있다

**Acceptance Criteria:**
- Given 장바구니에 메뉴 존재
- When 수량 증가 버튼 클릭
- Then 해당 메뉴 수량 +1
- And 총 금액 재계산

#### CART-C-003: 장바구니 수량 감소
**As a** 테이블 고객  
**I want** 장바구니 항목의 수량을 감소시킬 수 있다  
**So that** 주문 수량을 조절할 수 있다

**Acceptance Criteria:**
- Given 장바구니에 수량 2 이상인 메뉴 존재
- When 수량 감소 버튼 클릭
- Then 해당 메뉴 수량 -1
- And 총 금액 재계산

#### CART-C-004: 장바구니 항목 삭제
**As a** 테이블 고객  
**I want** 장바구니에서 메뉴를 삭제할 수 있다  
**So that** 원하지 않는 메뉴를 제거할 수 있다

**Acceptance Criteria:**
- Given 장바구니에 메뉴 존재
- When 삭제 버튼 클릭
- Then 해당 메뉴 장바구니에서 제거
- And 총 금액 재계산

#### CART-C-005: 장바구니 비우기
**As a** 테이블 고객  
**I want** 장바구니를 한번에 비울 수 있다  
**So that** 처음부터 다시 선택할 수 있다

**Acceptance Criteria:**
- Given 장바구니에 메뉴 존재
- When 전체 삭제 버튼 클릭
- Then 모든 메뉴 제거
- And 총 금액 0원 표시

---

## 4. 주문 (Order)

#### ORDER-C-001: 주문 생성
**As a** 테이블 고객  
**I want** 장바구니의 메뉴를 주문할 수 있다  
**So that** 음식을 받을 수 있다

**Acceptance Criteria:**
- Given 장바구니에 메뉴 존재
- When 주문하기 버튼 클릭
- Then 주문 확인 화면 표시
- And 주문 확정 버튼 표시

#### ORDER-C-002: 주문 확정
**As a** 테이블 고객  
**I want** 주문을 최종 확정할 수 있다  
**So that** 주문이 주방에 전달된다

**Acceptance Criteria:**
- Given 주문 확인 화면
- When 주문 확정 버튼 클릭
- Then 주문 번호 표시
- And 장바구니 비워짐
- And 메뉴 화면으로 이동

#### ORDER-C-003: 주문 내역 조회
**As a** 테이블 고객  
**I want** 현재 세션의 주문 내역을 볼 수 있다  
**So that** 주문한 메뉴와 금액을 확인할 수 있다

**Acceptance Criteria:**
- Given 로그인된 고객
- When 주문 내역 화면 접속
- Then 현재 세션 주문 목록 표시
- And 주문별 메뉴, 수량, 금액 표시

#### ORDER-C-004: 주문 상태 확인
**As a** 테이블 고객  
**I want** 주문의 현재 상태를 확인할 수 있다  
**So that** 음식 준비 상황을 알 수 있다

**Acceptance Criteria:**
- Given 주문 내역 화면
- When 주문 목록 조회
- Then 각 주문의 상태 표시 (대기중/준비중/완료)
- And 상태별 시각적 구분

---

## 5. 주문 관리 (Order Management)

#### ORDMGT-A-001: 실시간 주문 수신
**As a** 매장 관리자  
**I want** 신규 주문을 실시간으로 받을 수 있다  
**So that** 즉시 주문을 확인하고 처리할 수 있다

**Acceptance Criteria:**
- Given 관리자 대시보드
- When 고객이 주문 생성
- Then 2초 이내 대시보드에 표시
- And 신규 주문 시각적 강조

#### ORDMGT-A-002: 테이블별 주문 현황 조회
**As a** 매장 관리자  
**I want** 테이블별로 주문 현황을 볼 수 있다  
**So that** 각 테이블 상황을 파악할 수 있다

**Acceptance Criteria:**
- Given 관리자 대시보드
- When 대시보드 조회
- Then 테이블별 카드 형태로 표시
- And 각 테이블 총 주문액 표시

#### ORDMGT-A-003: 주문 상세 조회
**As a** 매장 관리자  
**I want** 특정 주문의 상세 내역을 볼 수 있다  
**So that** 주문 메뉴를 정확히 확인할 수 있다

**Acceptance Criteria:**
- Given 테이블 카드
- When 주문 카드 클릭
- Then 전체 메뉴 목록 표시
- And 수량, 금액 상세 표시

#### ORDMGT-A-004: 주문 상태 변경
**As a** 매장 관리자  
**I want** 주문 상태를 변경할 수 있다  
**So that** 주문 처리 진행 상황을 관리할 수 있다

**Acceptance Criteria:**
- Given 주문 상세 화면
- When 상태 변경 버튼 클릭
- Then 대기중 → 준비중 → 완료 순서로 변경
- And 변경 즉시 반영

#### ORDMGT-A-005: 주문 삭제
**As a** 매장 관리자  
**I want** 특정 주문을 삭제할 수 있다  
**So that** 잘못된 주문을 정정할 수 있다

**Acceptance Criteria:**
- Given 주문 상세 화면
- When 삭제 버튼 클릭
- Then 확인 팝업 표시
- And 확인 시 주문 삭제
- And 테이블 총 주문액 재계산

---

## 6. 테이블 관리 (Table Management)

#### TBLMGT-A-001: 테이블 세션 시작
**As a** 매장 관리자  
**I want** 테이블 세션이 첫 주문 시 자동 시작된다  
**So that** 고객별 주문을 추적할 수 있다

**Acceptance Criteria:**
- Given 세션 없는 테이블
- When 첫 주문 생성
- Then 새 세션 자동 생성
- And 세션 ID로 주문 그룹화

#### TBLMGT-A-002: 테이블 이용 완료
**As a** 매장 관리자  
**I want** 테이블 이용 완료 처리를 할 수 있다  
**So that** 새 고객을 받을 준비를 할 수 있다

**Acceptance Criteria:**
- Given 주문이 있는 테이블
- When 이용 완료 버튼 클릭
- Then 확인 팝업 표시
- And 확인 시 세션 종료
- And 주문 내역 이력으로 이동

#### TBLMGT-A-003: 테이블 초기화
**As a** 매장 관리자  
**I want** 이용 완료 시 테이블이 초기화된다  
**So that** 새 고객이 이전 주문을 보지 않는다

**Acceptance Criteria:**
- Given 이용 완료 처리된 테이블
- When 처리 완료
- Then 현재 주문 목록 비워짐
- And 총 주문액 0원으로 리셋

#### TBLMGT-A-004: 과거 주문 내역 조회
**As a** 매장 관리자  
**I want** 테이블의 과거 주문 내역을 볼 수 있다  
**So that** 이전 매출을 확인할 수 있다

**Acceptance Criteria:**
- Given 테이블 관리 화면
- When 과거 내역 버튼 클릭
- Then 과거 주문 목록 표시 (시간 역순)
- And 날짜 필터링 가능

#### TBLMGT-A-005: 과거 내역 상세 조회
**As a** 매장 관리자  
**I want** 과거 주문의 상세 내역을 볼 수 있다  
**So that** 정확한 주문 정보를 확인할 수 있다

**Acceptance Criteria:**
- Given 과거 주문 목록
- When 특정 주문 선택
- Then 주문 번호, 시각, 메뉴 목록, 총 금액 표시
- And 이용 완료 시각 표시

---

## 7. 메뉴 관리 (Menu Management)

#### MENUMGT-A-001: 메뉴 목록 조회
**As a** 매장 관리자  
**I want** 등록된 메뉴 목록을 볼 수 있다  
**So that** 현재 메뉴 현황을 파악할 수 있다

**Acceptance Criteria:**
- Given 메뉴 관리 화면
- When 화면 접속
- Then 카테고리별 메뉴 목록 표시
- And 메뉴명, 가격, 상태 표시

#### MENUMGT-A-002: 메뉴 등록
**As a** 매장 관리자  
**I want** 새 메뉴를 등록할 수 있다  
**So that** 판매 메뉴를 추가할 수 있다

**Acceptance Criteria:**
- Given 메뉴 관리 화면
- When 메뉴 추가 버튼 클릭
- Then 메뉴 등록 폼 표시
- And 메뉴명, 가격, 설명, 카테고리, 이미지 입력 가능

#### MENUMGT-A-003: 메뉴 이미지 업로드
**As a** 매장 관리자  
**I want** 메뉴 이미지를 업로드할 수 있다  
**So that** 고객에게 메뉴 사진을 보여줄 수 있다

**Acceptance Criteria:**
- Given 메뉴 등록/수정 폼
- When 이미지 파일 선택
- Then 이미지 미리보기 표시
- And 저장 시 S3에 업로드

#### MENUMGT-A-004: 메뉴 수정
**As a** 매장 관리자  
**I want** 기존 메뉴 정보를 수정할 수 있다  
**So that** 가격이나 설명을 변경할 수 있다

**Acceptance Criteria:**
- Given 메뉴 목록
- When 특정 메뉴 수정 버튼 클릭
- Then 수정 폼에 기존 정보 표시
- And 변경 후 저장 가능

#### MENUMGT-A-005: 메뉴 삭제
**As a** 매장 관리자  
**I want** 메뉴를 삭제할 수 있다  
**So that** 판매 중단 메뉴를 제거할 수 있다

**Acceptance Criteria:**
- Given 메뉴 목록
- When 삭제 버튼 클릭
- Then 확인 팝업 표시
- And 확인 시 메뉴 삭제

#### MENUMGT-A-006: 메뉴 순서 조정
**As a** 매장 관리자  
**I want** 메뉴 노출 순서를 조정할 수 있다  
**So that** 원하는 순서로 메뉴를 배치할 수 있다

**Acceptance Criteria:**
- Given 메뉴 목록
- When 드래그 앤 드롭 또는 순서 버튼 사용
- Then 메뉴 순서 변경
- And 변경 즉시 저장

---

## 8. 에러 처리 (Error Handling)

### 고객 에러

#### ERR-C-001: 로그인 실패 처리
**As a** 테이블 고객  
**I want** 로그인 실패 시 에러 메시지를 볼 수 있다  
**So that** 문제를 파악하고 재시도할 수 있다

**Acceptance Criteria:**
- Given 로그인 시도
- When 인증 실패
- Then 에러 메시지 표시
- And 재입력 가능

#### ERR-C-002: 주문 실패 처리
**As a** 테이블 고객  
**I want** 주문 실패 시 에러 메시지를 볼 수 있다  
**So that** 장바구니를 유지하고 재시도할 수 있다

**Acceptance Criteria:**
- Given 주문 확정 시도
- When 서버 오류 발생
- Then 에러 메시지 표시
- And 장바구니 유지
- And 재시도 가능

#### ERR-C-003: 네트워크 오류 처리
**As a** 테이블 고객  
**I want** 네트워크 오류 시 안내 메시지를 볼 수 있다  
**So that** 연결 상태를 확인할 수 있다

**Acceptance Criteria:**
- Given 네트워크 요청
- When 연결 실패
- Then 네트워크 오류 메시지 표시
- And 재시도 버튼 표시

### 관리자 에러

#### ERR-A-001: 로그인 실패 처리
**As a** 매장 관리자  
**I want** 로그인 실패 시 에러 메시지를 볼 수 있다  
**So that** 올바른 정보로 재시도할 수 있다

**Acceptance Criteria:**
- Given 관리자 로그인 시도
- When 인증 실패
- Then 에러 메시지 표시
- And 재입력 가능

#### ERR-A-002: 주문 처리 실패
**As a** 매장 관리자  
**I want** 주문 상태 변경 실패 시 알림을 받을 수 있다  
**So that** 재시도하거나 문제를 해결할 수 있다

**Acceptance Criteria:**
- Given 주문 상태 변경 시도
- When 서버 오류 발생
- Then 에러 알림 표시
- And 재시도 가능

#### ERR-A-003: SSE 연결 끊김 처리
**As a** 매장 관리자  
**I want** 실시간 연결 끊김 시 알림을 받을 수 있다  
**So that** 연결 상태를 확인하고 복구할 수 있다

**Acceptance Criteria:**
- Given SSE 연결 중
- When 연결 끊김
- Then 연결 상태 알림 표시
- And 자동 재연결 시도
- And 수동 새로고침 버튼 표시

---

## Story Summary

| Category | Count |
|----------|-------|
| 인증 (Authentication) | 6 |
| 메뉴 (Menu) | 3 |
| 장바구니 (Cart) | 5 |
| 주문 (Order) | 4 |
| 주문 관리 (Order Management) | 5 |
| 테이블 관리 (Table Management) | 5 |
| 메뉴 관리 (Menu Management) | 6 |
| 에러 처리 (Error Handling) | 6 |
| **Total** | **40** |

---

## INVEST Compliance

모든 스토리는 INVEST 기준을 충족합니다:

- **Independent**: 각 스토리는 독립적으로 구현 가능
- **Negotiable**: 구현 세부사항은 협상 가능
- **Valuable**: 각 스토리는 사용자에게 명확한 가치 제공
- **Estimable**: 스토리 크기 추정 가능
- **Small**: Fine 수준으로 세분화되어 적절한 크기
- **Testable**: Given/When/Then 형식의 acceptance criteria로 테스트 가능
