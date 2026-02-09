# Business Logic Model - Backend

**Unit**: backend
**작성일**: 2026-02-09

---

## 1. 주문 생성 플로우

```
Input: table_token, order_items[]
Output: Order

1. 토큰에서 store_id, table_id 추출
2. 각 menu_id의 유효성 검증
   - 존재 여부
   - is_available = True
   - 같은 store_id
3. 세션 확인/생성
   - current_session_id 있으면 사용
   - 없으면 새 세션 생성
4. 주문 번호 생성 (YYYYMMDD-XXXX)
5. 주문 항목 생성
   - menu_name, unit_price 스냅샷 저장
   - subtotal = quantity * unit_price
6. total_amount 계산
7. Order 저장
8. SSE 이벤트 브로드캐스트 ('new_order')
9. Order 반환
```

---

## 2. 이용 완료 플로우

```
Input: admin_token, table_id
Output: success

1. 토큰에서 store_id 추출, 관리자 권한 확인
2. 테이블의 current_session_id 확인
   - NULL이면 에러 (이미 완료됨)
3. 세션 종료
   - session_end_time = now()
   - is_active = False
4. 테이블 초기화
   - current_session_id = NULL
5. SSE 이벤트 브로드캐스트 ('table_reset')
6. success 반환
```

---

## 3. 실시간 주문 스트리밍 플로우

```
Input: admin_token
Output: EventStream

1. 토큰에서 store_id 추출, 관리자 권한 확인
2. SSE 연결 생성
3. 연결을 store_id별 연결 풀에 등록
4. 이벤트 대기 루프
   - 이벤트 발생 시 클라이언트에 전송
   - 연결 끊김 시 풀에서 제거
```

---

## 4. 주문 상태 변경 플로우

```
Input: admin_token, order_id, new_status
Output: Order

1. 토큰에서 store_id 추출, 관리자 권한 확인
2. 주문 조회 (store_id 일치 확인)
3. 상태 전이 검증
   - pending → preparing ✓
   - preparing → completed ✓
   - 기타 → 에러
4. 상태 업데이트
5. SSE 이벤트 브로드캐스트 ('order_updated')
6. Order 반환
```

---

## 5. 메뉴 등록 플로우

```
Input: admin_token, menu_data
Output: Menu

1. 토큰에서 store_id 추출, 관리자 권한 확인
2. 입력 검증
   - menu_name 필수
   - price > 0
   - category_id 존재 및 같은 store_id
3. display_order 설정 (카테고리 내 최대값 + 1)
4. Menu 저장
5. Menu 반환
```

---

## 6. 이미지 업로드 플로우

```
Input: admin_token, file
Output: image_url

1. 토큰에서 store_id 추출, 관리자 권한 확인
2. 파일 검증
   - 형식: JPEG, PNG, WebP
   - 크기: ≤ 5MB
3. 파일명 생성 (UUID + 확장자)
4. S3 업로드
   - Bucket: {bucket_name}
   - Key: menus/{store_id}/{filename}
5. URL 생성 및 반환
```

---

## 7. 고객 주문 내역 조회 플로우

```
Input: table_token
Output: Order[]

1. 토큰에서 store_id, table_id 추출
2. 테이블의 current_session_id 확인
   - NULL이면 빈 배열 반환
3. 해당 session_id의 주문 조회
4. 주문 항목 포함하여 반환
5. created_at 역순 정렬
```

---

## 8. 관리자 대시보드 데이터 조회 플로우

```
Input: admin_token
Output: TableOrderSummary[]

1. 토큰에서 store_id 추출, 관리자 권한 확인
2. 활성 세션이 있는 테이블 조회
3. 각 테이블별:
   - 총 주문액 계산
   - 최근 주문 n개 조회
4. 테이블 번호 순 정렬
5. 결과 반환
```
