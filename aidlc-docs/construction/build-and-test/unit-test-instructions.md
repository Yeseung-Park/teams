# Unit Test Execution

## TDD Artifacts 확인

Backend는 TDD 방식으로 개발되어 테스트가 이미 작성되어 있습니다.
- `aidlc-docs/construction/plans/backend-test-plan.md` 참조
- 총 25개 테스트 케이스 (모두 🟢 Passed)

---

## Backend Unit Tests

### 테스트 실행

```bash
cd backend
source venv/bin/activate

# 전체 테스트 실행
pytest tests/ -v

# 커버리지 포함 실행
pytest tests/ -v --cov=app --cov-report=html
```

### 테스트 파일 구조

```
tests/
├── test_auth.py      # 5 tests (TC-AUTH-001~005)
├── test_menu.py      # 5 tests (TC-MENU-001~005)
├── test_order.py     # 7 tests (TC-ORDER-001~007)
├── test_table.py     # 5 tests (TC-TABLE-001~005)
└── test_upload.py    # 2 tests (TC-UPLOAD-001~002)
```

### 예상 결과

```
========================= test session starts ==========================
tests/test_auth.py::test_login_table_success PASSED
tests/test_auth.py::test_login_table_invalid_password PASSED
tests/test_auth.py::test_login_admin_success PASSED
tests/test_auth.py::test_verify_token_valid PASSED
tests/test_auth.py::test_verify_token_invalid PASSED
tests/test_menu.py::test_get_menus PASSED
tests/test_menu.py::test_create_menu PASSED
tests/test_menu.py::test_update_menu PASSED
tests/test_menu.py::test_delete_menu PASSED
tests/test_menu.py::test_get_menu_not_found PASSED
tests/test_order.py::test_create_order PASSED
tests/test_order.py::test_get_orders_by_session PASSED
tests/test_order.py::test_get_active_orders PASSED
tests/test_order.py::test_update_order_status PASSED
tests/test_order.py::test_delete_order PASSED
tests/test_order.py::test_create_order_empty_items PASSED
tests/test_order.py::test_update_order_invalid_status PASSED
tests/test_table.py::test_ensure_session_new PASSED
tests/test_table.py::test_ensure_session_existing PASSED
tests/test_table.py::test_complete_table PASSED
tests/test_table.py::test_complete_table_no_session PASSED
tests/test_table.py::test_get_table_history PASSED
tests/test_upload.py::test_upload_image_valid PASSED
tests/test_upload.py::test_upload_image_invalid_type PASSED
========================= 24 passed in 2.5s ============================
```

### 요구사항 커버리지

| 요구사항 | 테스트 케이스 | 상태 |
|---------|-------------|------|
| AUTH-C-001~003 | TC-AUTH-001~002 | ✅ |
| AUTH-A-001~003 | TC-AUTH-003~005 | ✅ |
| MENU-C-001~003 | TC-MENU-001 | ✅ |
| MENUMGT-A-001~006 | TC-MENU-002~005 | ✅ |
| ORDER-C-001~004 | TC-ORDER-001~003 | ✅ |
| ORDMGT-A-001~005 | TC-ORDER-004~007 | ✅ |
| TBLMGT-A-001~005 | TC-TABLE-001~005 | ✅ |

---

## Frontend Unit Tests (Optional)

Frontend는 Standard 방식으로 개발되어 별도 테스트가 없습니다.
필요시 Vitest + Vue Test Utils로 테스트 추가 가능합니다.

### 테스트 환경 설정 (선택)

```bash
cd frontend
npm install -D vitest @vue/test-utils jsdom
```

### vitest.config.js (선택)
```javascript
import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  test: {
    environment: 'jsdom'
  }
})
```

---

## 테스트 실패 시 대응

1. 실패한 테스트 확인
2. 에러 메시지 분석
3. 관련 코드 수정
4. 테스트 재실행
5. 모든 테스트 통과 확인
