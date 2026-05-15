## Context

TaskFlow MVP는 소규모 팀(3-5인)을 위한 칸반+채팅 일체형 협업 도구다. 신규 프로젝트로 기존 코드베이스 없음. 기술 스택은 기획 문서에서 고정 지정됨: FastAPI(BE) + Vanilla JS + Tailwind(FE) + SQLite(로컬)/Neon(배포). Vercel에서 FE+BE를 단일 앱으로 서빙한다.

## Goals / Non-Goals

**Goals:**
- FastAPI 단일 앱에서 REST API(18개) + 정적 파일(FE) 동시 서빙
- 로컬 SQLite ↔ Neon PostgreSQL 환경변수 하나로 전환
- JWT 인증 미들웨어로 전체 보호된 엔드포인트 일관 처리
- 5초 폴링 채팅으로 WebSocket 없이 실시간성 구현
- Vercel Functions로 FastAPI 배포, `DATABASE_URL` 환경변수 자동 주입

**Non-Goals:**
- WebSocket, 이메일/SMS 알림, 파일 업로드
- 페이지별 권한, 전문 검색, 다국어
- pytest/jest 자동 테스트, Sentry 로그 수집

## Decisions

### 1. 단일 FastAPI 앱 — FE 정적 파일 포함

**결정**: FastAPI `StaticFiles`로 FE HTML/JS/CSS를 `/` 경로에 마운트, API는 `/api/` prefix로 분리.

**이유**: Vercel Functions에서 FE+BE 별도 배포보다 단일 앱이 CORS 설정 불필요하고 배포 단순. 로컬 개발도 서버 하나만 기동.

**대안 고려**: Next.js FE + 별도 BE → 학습 복잡도 증가, Day 2 범위 초과.

---

### 2. SQLAlchemy 환경변수 분기

**결정**: `DATABASE_URL` 환경변수 존재 시 Neon PostgreSQL, 없으면 로컬 `./taskflow.db` SQLite 사용. SQLAlchemy로 양쪽 호환.

**이유**: 로컬 개발은 SQLite로 설치 없이 즉시 기동, 배포는 Neon Pooled URL 자동 주입.

**대안 고려**: Docker PostgreSQL 로컬 → 환경 설정 부담 증가.

---

### 3. JWT localStorage 저장

**결정**: JWT를 브라우저 localStorage에 저장, 모든 API 요청에 `Authorization: Bearer <token>` 헤더 첨부.

**이유**: Assumption에 명시된 전제(JWT localStorage = 검증 안 함). httpOnly Cookie는 Day 2 범위 외.

**리스크**: XSS 취약 → Out of Scope 명시로 수용.

---

### 4. 채팅 5초 폴링

**결정**: `GET /api/teams/{id}/messages?since=<ISO timestamp>` 로 5초마다 신규 메시지만 가져옴.

**이유**: WebSocket은 Vercel Functions의 stateless 특성과 충돌. 폴링으로 동일 UX 근사.

**대안 고려**: SSE → 브라우저 연결 유지로 Vercel 과금 증가.

---

### 5. 프로젝트 구조

```
taskflow/
├── main.py              # FastAPI 앱 진입점, StaticFiles 마운트
├── database.py          # SQLAlchemy 엔진·세션 (SQLite/Neon 분기)
├── models.py            # users, teams, tasks, messages 모델
├── auth.py              # JWT 발급·검증, bcrypt 해시
├── routers/
│   ├── auth.py          # POST /api/auth/*
│   ├── teams.py         # POST/GET /api/teams/*
│   ├── tasks.py         # POST/GET/PUT/DELETE /api/tasks/*
│   └── messages.py      # POST/GET/DELETE /api/teams/{id}/messages
├── static/
│   ├── index.html       # 로그인 화면
│   ├── teams.html       # 팀 선택 화면
│   ├── kanban.html      # 칸반 화면
│   ├── chat.html        # 채팅 화면
│   └── app.js           # 공통 JS (API 호출, JWT 헤더 주입)
├── requirements.txt
└── vercel.json          # Vercel Functions 설정
```

## Risks / Trade-offs

- **Neon Pooled 연결 한도** → Free 플랜 동시 접속 제한, 동시 50명 이내 Assumption으로 수용
- **SQLite → PostgreSQL 타입 차이** → SQLAlchemy String/Integer/DateTime 공통 타입만 사용, ARRAY/JSON 컬럼 금지
- **칸반 드래그 50ms** → 서버 왕복 없이 낙관적 UI 업데이트 후 API 호출로 달성
- **JWT 만료(24h) 갱신 없음** → 만료 시 재로그인 필요, Constraint로 명시 수용

## Migration Plan

1. 로컬: `pip install -r requirements.txt` → `uvicorn main:app --reload`
2. Vercel 배포: `vercel deploy` → Neon Pooled URL을 `DATABASE_URL` 환경변수로 주입
3. 롤백: 이전 Vercel deployment URL로 즉시 전환 가능 (Vercel 대시보드)

## Open Questions

- (없음 — 기획 문서에서 모든 결정 사항 명시 완료)
