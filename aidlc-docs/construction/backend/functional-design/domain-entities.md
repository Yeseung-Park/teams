# Domain Entities - Backend

**Unit**: backend
**작성일**: 2026-02-09

---

## Entity Relationship Diagram

```
Store (1) ──────< Table (N)
  │                  │
  │                  └──< TableSession (N)
  │                              │
  │                              └──< Order (N)
  │                                      │
  │                                      └──< OrderItem (N)
  │
  └──────< Category (N)
              │
              └──< Menu (N)
```

---

## Entities

### Store (매장)
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| store_id | Integer | PK, Auto | 매장 고유 ID |
| store_name | String(100) | NOT NULL | 매장명 |
| store_identifier | String(50) | UNIQUE, NOT NULL | 매장 식별자 (로그인용) |
| admin_username | String(50) | NOT NULL | 관리자 사용자명 |
| admin_password_hash | String(255) | NOT NULL | 비밀번호 해시 (bcrypt) |
| created_at | DateTime | NOT NULL | 생성일시 |
| updated_at | DateTime | NOT NULL | 수정일시 |

### Table (테이블)
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| table_id | Integer | PK, Auto | 테이블 고유 ID |
| store_id | Integer | FK(Store), NOT NULL | 매장 ID |
| table_number | Integer | NOT NULL | 테이블 번호 |
| table_password_hash | String(255) | NOT NULL | 테이블 비밀번호 해시 |
| current_session_id | Integer | FK(TableSession), NULL | 현재 세션 ID |
| created_at | DateTime | NOT NULL | 생성일시 |
| updated_at | DateTime | NOT NULL | 수정일시 |

**Unique**: (store_id, table_number)

### TableSession (테이블 세션)
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| session_id | Integer | PK, Auto | 세션 고유 ID |
| table_id | Integer | FK(Table), NOT NULL | 테이블 ID |
| session_start_time | DateTime | NOT NULL | 세션 시작 시각 |
| session_end_time | DateTime | NULL | 세션 종료 시각 |
| is_active | Boolean | NOT NULL, Default=True | 활성 여부 |
| created_at | DateTime | NOT NULL | 생성일시 |
| updated_at | DateTime | NOT NULL | 수정일시 |

### Category (카테고리)
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| category_id | Integer | PK, Auto | 카테고리 고유 ID |
| store_id | Integer | FK(Store), NOT NULL | 매장 ID |
| category_name | String(50) | NOT NULL | 카테고리명 |
| display_order | Integer | NOT NULL, Default=0 | 표시 순서 |
| created_at | DateTime | NOT NULL | 생성일시 |
| updated_at | DateTime | NOT NULL | 수정일시 |

### Menu (메뉴)
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| menu_id | Integer | PK, Auto | 메뉴 고유 ID |
| store_id | Integer | FK(Store), NOT NULL | 매장 ID |
| category_id | Integer | FK(Category), NOT NULL | 카테고리 ID |
| menu_name | String(100) | NOT NULL | 메뉴명 |
| price | Integer | NOT NULL | 가격 (원) |
| description | Text | NULL | 메뉴 설명 |
| image_url | String(500) | NULL | 이미지 URL (S3) |
| display_order | Integer | NOT NULL, Default=0 | 표시 순서 |
| is_available | Boolean | NOT NULL, Default=True | 판매 가능 여부 |
| created_at | DateTime | NOT NULL | 생성일시 |
| updated_at | DateTime | NOT NULL | 수정일시 |

### Order (주문)
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| order_id | Integer | PK, Auto | 주문 고유 ID |
| store_id | Integer | FK(Store), NOT NULL | 매장 ID |
| table_id | Integer | FK(Table), NOT NULL | 테이블 ID |
| session_id | Integer | FK(TableSession), NOT NULL | 세션 ID |
| order_number | String(20) | NOT NULL | 주문 번호 |
| total_amount | Integer | NOT NULL | 총 금액 |
| order_status | Enum | NOT NULL, Default='pending' | 주문 상태 |
| created_at | DateTime | NOT NULL | 생성일시 |
| updated_at | DateTime | NOT NULL | 수정일시 |

**order_status**: 'pending' (대기중), 'preparing' (준비중), 'completed' (완료)

### OrderItem (주문 항목)
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| order_item_id | Integer | PK, Auto | 주문 항목 고유 ID |
| order_id | Integer | FK(Order), NOT NULL | 주문 ID |
| menu_id | Integer | FK(Menu), NOT NULL | 메뉴 ID |
| menu_name | String(100) | NOT NULL | 메뉴명 (스냅샷) |
| quantity | Integer | NOT NULL | 수량 |
| unit_price | Integer | NOT NULL | 단가 (스냅샷) |
| subtotal | Integer | NOT NULL | 소계 |
| created_at | DateTime | NOT NULL | 생성일시 |

---

## Indexes

| Table | Index Name | Columns | Type |
|-------|------------|---------|------|
| Store | idx_store_identifier | store_identifier | UNIQUE |
| Table | idx_table_store_number | store_id, table_number | UNIQUE |
| Order | idx_order_session | session_id | INDEX |
| Order | idx_order_status | order_status | INDEX |
| Menu | idx_menu_category | category_id | INDEX |
