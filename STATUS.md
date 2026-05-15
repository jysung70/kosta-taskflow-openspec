# TaskFlow MVP — 시스템 현황

> 기준일: 2026-05-15

---

## 배포 정보

| 항목 | 값 |
|------|-----|
| 프로덕션 URL | https://taskflow-openspec-six.vercel.app |
| GitHub | https://github.com/jysung70/kosta-taskflow-openspec |
| 플랫폼 | Vercel (FastAPI Python 3.12) |
| DB | Neon Serverless PostgreSQL (`neon-gray-flower`) |
| 로컬 실행 | `uvicorn main:app --reload --port 8000` |

---

## 기술 스택

| 레이어 | 기술 |
|--------|------|
| Backend | FastAPI + SQLAlchemy (Python 3.14) |
| Frontend | Vanilla JS + Tailwind CSS (CDN) |
| DB (로컬) | SQLite (`taskflow.db`) |
| DB (배포) | Neon PostgreSQL (Vercel Marketplace) |
| 인증 | JWT (24h) + bcrypt (python-jose, bcrypt) |
| 배포 | Vercel Functions (`@vercel/python`) |

---

## 구현된 기능

### 인증
- 회원가입 (이메일/비밀번호 8자 이상, 중복 체크)
- 로그인 (JWT 발급, team_id 포함 응답)
- 로그인 성공 시 team_id 분기 (없으면 팀선택, 있으면 칸반 직행)
- 로그아웃 (클라이언트 토큰 삭제, stateless)

### 팀 관리
- 팀 생성 (초대코드 `ABCD-1234` 자동발급, 성공 화면 + 복사 버튼)
- 초대코드로 팀 합류 → `/kanban?team=N` 자동 이동
- 멤버 목록 조회
- 팀 생성/합류 시 `users.team_id` 자동 업데이트

### 칸반 보드
- TODO / DOING / DONE 3컬럼
- 컬럼 헤더 색상 + 태스크 카운트 (`TODO · 3`)
- 카드에 `#id · @assignee` 표시
- 필터 탭 (전체 / @me / 미할당)
- 인라인 태스크 생성 (+ 클릭 → 담당자 @me 기본값)
- 드래그앤드롭 상태 이동 → `PATCH /api/tasks/{id}/status`
- Empty state (📋 아이콘 + 안내 문구)
- 모바일 반응형 (768px 이하 → 1컬럼 + 탭 전환)

### 채팅
- 팀 단위 텍스트 채팅 (1000자 제한)
- 5초 폴링 (`since` 마이크로초 정밀도)
- 말풍선 UI (내 메시지: teal 오른쪽, 상대: 흰색 왼쪽)
- `● 5초마다 새로고침` 헤더 인디케이터
- Empty state (💬 아이콘 + "아직 대화가 없습니다")
- 클라이언트 ID 기반 중복 제거 (`seenIds Set`)

### 공통 UI
- 탭 네비게이션 (칸반 | 채팅 | 멤버)
- 버튼 로딩 상태 ("처리 중...")
- 인라인 에러 표시 (필드 하단)
- teal (#0d9488) 브랜드 컬러 일관 적용

---

## API 엔드포인트 (18개 + 1개 추가)

### Auth (4개)
| Method | Path | 설명 |
|--------|------|------|
| POST | `/api/auth/signup` | 회원가입 → JWT + user(team_id) |
| POST | `/api/auth/login` | 로그인 → JWT + user(team_id) |
| GET | `/api/auth/me` | 내 정보 |
| POST | `/api/auth/logout` | 로그아웃 (200 반환) |

### Team (4개)
| Method | Path | 설명 |
|--------|------|------|
| POST | `/api/teams` | 팀 생성 + users.team_id 업데이트 |
| GET | `/api/teams` | 내 팀 목록 |
| POST | `/api/teams/join` | 초대코드로 합류 + users.team_id 업데이트 |
| GET | `/api/teams/{id}/members` | 멤버 목록 |

### Task (6개 + PATCH 1개)
| Method | Path | 설명 |
|--------|------|------|
| POST | `/api/teams/{id}/tasks` | 태스크 생성 (assignee_id 옵션) |
| GET | `/api/teams/{id}/tasks` | 팀 태스크 목록 |
| GET | `/api/tasks/{id}` | 태스크 단건 |
| PUT | `/api/tasks/{id}` | 태스크 수정 (title/status 복합) |
| PATCH | `/api/tasks/{id}/status` | 상태만 변경 (드래그용) |
| DELETE | `/api/tasks/{id}` | 태스크 삭제 |

### Chat (4개)
| Method | Path | 설명 |
|--------|------|------|
| POST | `/api/teams/{id}/messages` | 메시지 전송 |
| GET | `/api/teams/{id}/messages?since=` | 메시지 목록 (폴링) |
| GET | `/api/messages/{id}` | 메시지 단건 |
| DELETE | `/api/messages/{id}` | 메시지 삭제 (본인만) |

---

## DB 스키마

```
users
  id, email(unique), password_hash, created_at, team_id(FK→teams, nullable)

teams
  id, name, invite_code(unique), owner_id(FK→users)

team_members  ← 다대다 중간 테이블
  user_id(FK→users), team_id(FK→teams)

tasks
  id, team_id(FK→teams), title, status(TODO/DOING/DONE),
  creator_id(FK→users), assignee_id(FK→users, nullable)

messages
  id, team_id(FK→teams), user_id(FK→users), content, created_at
```

---

## 파일 구조

```
D:\taskflow-openspec\
├── main.py              FastAPI 앱 + StaticFiles + ALTER TABLE 마이그레이션
├── database.py          SQLAlchemy 엔진 (SQLite/Neon 분기)
├── models.py            ORM 모델 5종
├── auth.py              JWT 발급/검증, bcrypt
├── routers/
│   ├── auth.py          인증 4 API
│   ├── teams.py         팀 4 API
│   ├── tasks.py         태스크 6+1 API
│   └── messages.py      채팅 4 API
├── static/
│   ├── app.js           공통 유틸 (JWT, API호출, 탭네비, 로딩)
│   ├── index.html       로그인
│   ├── signup.html      회원가입
│   ├── teams.html       팀 선택/생성
│   ├── kanban.html      칸반 보드
│   └── chat.html        채팅
├── requirements.txt
├── vercel.json          Vercel Functions 설정
├── .env.example         환경변수 예시
└── openspec/
    ├── specs/           메인 스펙 10종 (현재 기준)
    ├── changes/archive/ 완료된 변경 이력 2건
    └── docs/            기획 PDF + 스토리보드 이미지
```

---

## OpenSpec 변경 이력

| 날짜 | 변경명 | 내용 | 태스크 |
|------|--------|------|--------|
| 2026-05-15 | `taskflow-mvp` | MVP 전체 구현 + Vercel/Neon 배포 | 47/47 ✅ |
| 2026-05-15 | `ui-wireframe-alignment` | 스토리보드 v2 와이어프레임 정렬 | 33/33 ✅ |

---

## 메인 스펙 (openspec/specs/)

| Capability | 주요 내용 |
|-----------|----------|
| `user-auth` | 회원가입/로그인/JWT/로그아웃, team_id 응답 포함 |
| `team-management` | 팀 생성(성공화면), 합류, 멤버, team_id 업데이트 |
| `kanban-board` | 태스크 CRUD, assignee_id, PATCH /status |
| `team-chat` | 채팅 송수신, 5초 폴링, 마이크로초 since |
| `deployment` | 로컬 SQLite, Vercel, Neon 연동 |
| `tab-navigation` | 칸반/채팅/멤버 탭 |
| `kanban-ux` | 카드 표시, 필터, 인라인 생성, Empty state |
| `chat-ux` | 폴링 인디케이터, Empty state |
| `mobile-responsive` | 768px 이하 1컬럼 + 탭 전환 |
| `auth-ux` | 로딩 상태, 8자 검증, team_id 분기 |

---

## 알려진 사항

| 항목 | 내용 |
|------|------|
| Python 버전 | 3.14 사용 → passlib 비호환, bcrypt 직접 사용으로 해결 |
| 채팅 중복 | 마이크로초 정밀도 + seenIds로 완전 해결 |
| Out of Scope | 알림, 파일첨부, 전문검색, 권한세분화, 다국어, WebSocket, 자동테스트 |
| 모바일 스와이프 | CSS 탭 전환만 구현 (터치 제스처 미구현) |
