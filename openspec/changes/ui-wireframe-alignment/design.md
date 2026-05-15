## Context

TaskFlow MVP v1이 배포된 상태. 스토리보드 v2(42슬라이드)를 기준으로 UI/UX 정렬 작업. 기존 4개 HTML 파일과 app.js를 수정하며, BE는 DB 스키마 2개 컬럼 추가 + 엔드포인트 1개 추가가 필요하다. Neon PostgreSQL에 이미 데이터가 존재하므로 마이그레이션 전략이 중요하다.

## Goals / Non-Goals

**Goals:**
- 스토리보드 v2의 모든 화면 상태(정상/빈/에러)를 HTML에 반영
- `tasks.assignee_id`, `users.team_id` 컬럼 추가 (nullable — 기존 데이터 영향 없음)
- `PATCH /api/tasks/{id}/status` 분리 엔드포인트 추가
- 768px 이하 모바일 칸반 1컬럼 CSS 반응형

**Non-Goals:**
- 실제 터치 스와이프 제스처 (CSS 탭 전환만)
- 멤버 탭 실제 기능 (UI 버튼만, 멤버 목록 API는 기존 것 활용)
- assignee 선택 드롭다운의 전체 멤버 목록 API 연동 (기본값 @me만)

## Decisions

### 1. DB 마이그레이션 — nullable 컬럼 추가

**결정**: `tasks.assignee_id`, `users.team_id` 모두 nullable로 추가. SQLAlchemy `create_all`은 이미 존재하는 테이블을 건드리지 않으므로 Alembic 없이 직접 ALTER TABLE 실행.

**방법**: 앱 기동 시 `ALTER TABLE IF NOT EXISTS` (PostgreSQL) / `ALTER TABLE` 예외 무시 (SQLite) 방식으로 startup_event에서 처리.

**이유**: Alembic 도입은 이번 범위 초과. nullable 추가는 기존 데이터 손상 없음.

---

### 2. PATCH /tasks/{id}/status 분리

**결정**: 기존 `PUT /api/tasks/{id}` (title+status 복합)는 유지하고, `PATCH /api/tasks/{id}/status`를 추가로 신설. 칸반 드래그는 PATCH만 사용.

**이유**: 스토리보드 결정 #3 (PUT 중복 분리). REST 의미론 정확성. 기존 PUT 클라이언트 코드와 하위 호환.

---

### 3. 팀 컨텍스트 네비게이션 — URL 파라미터 유지

**결정**: 현재 `/kanban?team=N`, `/chat?team=N` URL 구조 유지. 탭 클릭 시 해당 URL로 이동. 단일 SPA 전환 없음.

**이유**: FastAPI StaticFiles 구조에서 클라이언트 라우터 없이 가장 단순. 각 페이지가 독립 HTML 파일이므로 탭 클릭 = 링크 이동.

---

### 4. users.team_id — 1인 1팀 정책

**결정**: `users.team_id` nullable 컬럼 추가. 팀 생성/합류 시 UPDATE. 로그인 응답에 포함. FE에서 NULL이면 `/teams`, 값이 있으면 `/kanban?team={id}`로 분기.

**이유**: 스토리보드 결정 #1. 현재 team_members 다대다 관계는 유지(팀 멤버 검증용), team_id는 "기본 팀" 개념으로만 사용.

---

### 5. 모바일 반응형 — Tailwind breakpoint

**결정**: Tailwind `md:` (768px) 기준으로 칸반 컬럼을 `flex-col` → 탭 기반 표시. CSS visibility 토글로 구현 (DOM 유지, display 전환).

**이유**: Tailwind CDN 사용 중이므로 별도 빌드 불필요. DOM 유지로 JS 상태 보존.

## Risks / Trade-offs

- **ALTER TABLE 실패 시** → 앱 기동은 계속됨 (예외 무시), assignee_id 컬럼 없이도 API 동작 (SQLAlchemy 모델만 있으면 쿼리 시 에러)  → Mitigation: startup 로그로 확인
- **기존 PUT /tasks/{id} 와 PATCH 공존** → 혼란 가능 → Mitigation: PATCH를 드래그에만 사용, 문서화
- **팀 생성 화면 UX 변경** → 현재 `/teams` 페이지 대폭 변경 → 기존 URL 유지로 영향 최소화

## Migration Plan

1. `models.py` 수정 (assignee_id, team_id 컬럼 추가)
2. `main.py` startup_event에 ALTER TABLE 추가
3. BE 라우터 수정 (PATCH /status, 로그인 응답, 팀 생성/합류)
4. FE HTML 5개 파일 수정
5. `vercel deploy --prod` 로 배포
6. Neon에서 `SELECT * FROM users LIMIT 1` 으로 컬럼 추가 확인

## Open Questions

- (없음)
