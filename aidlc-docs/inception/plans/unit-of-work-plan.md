# Unit of Work Plan

**프로젝트**: 테이블오더 서비스
**작성일**: 2026-02-09
**상태**: Planning

---

## Planning Checklist

- [x] Step 1: 유닛 분해 계획 생성
- [x] Step 2: 질문 수집
- [x] Step 3: 답변 분석
- [x] Step 4: 계획 승인 완료

## Generation Checklist

- [x] Step 5: unit-of-work.md 생성
- [x] Step 6: unit-of-work-dependency.md 생성
- [x] Step 7: unit-of-work-story-map.md 생성
- [ ] Step 8: 검증 및 완료

---

## Proposed Units

Application Design 결정사항 기반:
- **Backend**: 단일 FastAPI 서버 (Simple Structure)
- **Frontend**: 단일 Vue.js 프로젝트 (라우팅으로 Customer/Admin 분리)

### Unit 1: backend
- **Type**: Service (독립 배포 가능)
- **Tech**: Python, FastAPI, SQLAlchemy, MySQL
- **Modules**: auth, menu, order, table, sse, upload

### Unit 2: frontend
- **Type**: Service (독립 배포 가능)
- **Tech**: Vue.js 3, Pinia, Vite
- **Sections**: customer (/, /cart, /orders), admin (/admin/*)

---

## Clarification Questions

### Question 1: 유닛 분리 방식
제안된 2개 유닛(backend, frontend) 구성이 적합합니까?

A) Yes - 2개 유닛 (backend, frontend)으로 진행
B) No - 3개 유닛으로 분리 (backend, frontend-customer, frontend-admin)
C) Other (please describe after [Answer]: tag below)

[Answer]:A

---

**다음 단계**: 위 질문에 답변 후 알려주세요.
