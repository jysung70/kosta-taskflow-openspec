## Why

소규모 팀(3-5인)이 칸반 보드와 실시간 채팅을 분리된 도구 없이 한 화면에서 업무 진행을 추적할 수 있는 MVP가 필요하다. 기획 문서(프로그램 정의 + 스토리보드)가 완성된 지금, AI 코딩 어시스턴트가 임의 결정 없이 스펙 그대로 구현할 수 있는 조건이 갖춰졌다.

## What Changes

- **인증**: 회원가입, 로그인, JWT 발급(24h), bcrypt 비밀번호 해시, 로그아웃
- **팀**: 팀 생성, 초대코드(ABCD-1234 형식) 발급, 초대코드로 합류, 멤버 목록 조회
- **칸반**: TODO/DOING/DONE 3컬럼 태스크 보드, 태스크 추가·상태 이동·삭제·제목 수정
- **채팅**: 팀 단위 텍스트 채팅 송수신, 5초 폴링, 발신자·시각 표시
- **배포**: Vercel FE+BE 일체형 배포 + Vercel Storage Neon(PostgreSQL) 연동

## Capabilities

### New Capabilities

- `user-auth`: 회원가입·로그인·JWT 발급·bcrypt 해시·로그아웃 (Auth 4 API)
- `team-management`: 팀 생성·초대코드 발급·합류·멤버 목록 (Team 4 API)
- `kanban-board`: TODO/DOING/DONE 3컬럼 태스크 CRUD + 상태 이동 (Task 6 API)
- `team-chat`: 팀 단위 채팅 송수신·5초 폴링·발신자 표시 (Chat 4 API)
- `deployment`: Vercel 배포·Neon DB 연동·로컬 SQLite 호환 설정

### Modified Capabilities

(없음 — 신규 프로젝트)

## Impact

- **Backend**: FastAPI 앱 신규 생성, SQLAlchemy 모델 4종(users/teams/tasks/messages), API 라우터 18개
- **Frontend**: Vanilla JS + Tailwind 4화면(로그인·팀선택·칸반·채팅), StaticFiles로 BE에서 서빙
- **DB**: 로컬 SQLite ↔ 배포 Neon PostgreSQL 양쪽 호환 (SQLAlchemy URL 환경변수 분기)
- **배포**: Vercel Functions(FastAPI) + Vercel Storage Neon Pooled 연결, `DATABASE_URL` 환경변수 자동 주입
- **Out of Scope**: 아래 7종은 이번 MVP에서 구현하지 않음

## Out of Scope

- [X] **알림** — 이메일/푸시 알림 없음. 채팅 폴링으로 대체
- [X] **파일 첨부** — 이미지/파일 업로드 없음. 텍스트 채팅만
- [X] **검색** — 전문 검색 없음. 단순 SELECT 조회만
- [X] **권한 세분화** — 팀 admin/member 구분만. 페이지별 권한 없음
- [X] **다국어** — 한글 UI만. 다국어 리소스 분리 없음
- [X] **WebSocket** — 실시간 메시지 안 함. 5초 폴링으로 대체
- [X] **테스트 자동화** — pytest/jest 자동 테스트 없음. 수동 동작 확인만
