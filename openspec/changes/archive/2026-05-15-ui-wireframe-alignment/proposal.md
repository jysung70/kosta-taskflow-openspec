## Why

TaskFlow MVP 스토리보드 v2(42슬라이드)와 현재 구현 사이에 UI/UX 및 데이터 모델 차이가 존재한다. 스토리보드에 명시된 탭 네비게이션, 카드 표시 형식, assignee 기능, 모바일 반응형, Empty state 등이 미적용된 상태이며, 이를 스토리보드 기준으로 정렬한다.

## What Changes

**프론트엔드 (FE)**
- 헤더 탭 네비게이션: 칸반·채팅·멤버 탭 추가 (팀 컨텍스트 내 이동)
- 로그인/회원가입: 비밀번호 8자 이상 검증, 로딩 상태(`처리 중...`), 인라인 에러 표시
- 팀 생성 성공 화면: 초대코드 복사 버튼 + `칸반 시작하기 →` 버튼
- 칸반 컬럼 헤더: 태스크 카운트 표시 (`TODO · 3`), 컬럼 색상 (노란/파란/초록)
- 칸반 카드: `#id · @assignee` 표시
- 칸반 필터 탭: 전체 / @me / 미할당
- 칸반 인라인 태스크 생성: 담당자(@me) 드롭다운 + Enter 저장
- 칸반 Empty state: 아이콘 + "카드 없음" + "+ 첫 태스크 만들기" 안내
- 채팅 헤더: `● 5초마다 새로고침` 인디케이터
- 채팅 Empty state: 말풍선 아이콘 + "아직 대화가 없습니다" 안내
- 모바일 반응형 (768px): 칸반 1컬럼 + 탭 인디케이터 스와이프
- 로그인 성공 시 `users.team_id` 확인 → NULL이면 팀 선택, 있으면 칸반으로 직접 이동

**백엔드 (BE)**
- `tasks.assignee_id` 컬럼 추가 (nullable, FK users.id)
- `PATCH /api/tasks/{id}/status` 엔드포인트 추가 (상태 변경 전용)
- `users.team_id` 컬럼 추가 (nullable) + 로그인 응답에 포함
- 팀 생성/합류 시 `users.team_id` 자동 업데이트

## Capabilities

### New Capabilities
- `tab-navigation`: 팀 컨텍스트 내 칸반·채팅·멤버 탭 네비게이션
- `kanban-ux`: 칸반 카드 assignee 표시, 필터, 인라인 생성, Empty state
- `chat-ux`: 채팅 Empty state, 폴링 인디케이터
- `mobile-responsive`: 768px 이하 칸반 1컬럼 + 탭 스와이프
- `auth-ux`: 로딩 상태, 인라인 에러, 8자 검증, team_id 분기

### Modified Capabilities
- `user-auth`: 로그인 응답에 `team_id` 추가, 비밀번호 8자 이상 검증
- `team-management`: 팀 생성 후 성공 화면(초대코드 복사), `users.team_id` 자동 업데이트
- `kanban-board`: `assignee_id` 필드 추가, `PATCH /tasks/{id}/status` 분리

## Impact

- **BE**: `models.py` (Task.assignee_id, User.team_id 추가), `routers/tasks.py` (PATCH /status 추가), `routers/auth.py` (로그인 응답 team_id 포함), `routers/teams.py` (팀 생성/합류 시 team_id 업데이트)
- **FE**: `static/index.html`, `static/signup.html`, `static/teams.html`, `static/kanban.html`, `static/chat.html`, `static/app.js` 전체 수정
- **DB**: Neon/SQLite 스키마 마이그레이션 (ALTER TABLE 또는 `create_all` 재실행)
- **Out of Scope**: 모바일 실제 스와이프 제스처(터치 이벤트) — CSS/탭 UI만 적용
