## 1. 프로젝트 초기 설정

- [x] 1.1 프로젝트 디렉토리 구조 생성 (main.py, database.py, models.py, auth.py, routers/, static/)
- [x] 1.2 requirements.txt 작성 (fastapi, uvicorn, sqlalchemy, python-jose, passlib[bcrypt], psycopg2-binary, python-multipart)
- [x] 1.3 vercel.json 작성 (FastAPI Vercel Functions 설정)
- [x] 1.4 .env.example 작성 (DATABASE_URL 환경변수 예시)

## 2. DB 및 모델 설정

- [x] 2.1 database.py — SQLAlchemy 엔진 설정 (DATABASE_URL 있으면 Neon, 없으면 SQLite)
- [x] 2.2 models.py — users 테이블 모델 (id, email, password_hash, created_at)
- [x] 2.3 models.py — teams 테이블 모델 (id, name, invite_code, owner_id)
- [x] 2.4 models.py — tasks 테이블 모델 (id, team_id, title, status, creator_id)
- [x] 2.5 models.py — messages 테이블 모델 (id, team_id, user_id, content, created_at)
- [x] 2.6 team_members 중간 테이블 (users ↔ teams 다대다 관계)
- [x] 2.7 main.py — 앱 기동 시 테이블 자동 생성 (create_all)

## 3. 인증 (Auth)

- [x] 3.1 auth.py — bcrypt 비밀번호 해시·검증 함수
- [x] 3.2 auth.py — JWT 발급 (24h 만료) 및 검증 함수
- [x] 3.3 auth.py — 현재 사용자 의존성 함수 (get_current_user)
- [x] 3.4 routers/auth.py — POST /api/auth/signup (중복 이메일 409 처리)
- [x] 3.5 routers/auth.py — POST /api/auth/login (잘못된 자격증명 401 처리)
- [x] 3.6 routers/auth.py — GET /api/auth/me
- [x] 3.7 routers/auth.py — POST /api/auth/logout

## 4. 팀 관리 (Team)

- [x] 4.1 routers/teams.py — POST /api/teams (초대코드 ABCD-1234 형식 자동 생성)
- [x] 4.2 routers/teams.py — GET /api/teams (내 팀 목록)
- [x] 4.3 routers/teams.py — POST /api/teams/join (초대코드 검증, 중복 합류 409)
- [x] 4.4 routers/teams.py — GET /api/teams/{id}/members (비소속 403 처리)

## 5. 칸반 태스크 (Task)

- [x] 5.1 routers/tasks.py — POST /api/teams/{id}/tasks (초기 status=TODO)
- [x] 5.2 routers/tasks.py — GET /api/teams/{id}/tasks
- [x] 5.3 routers/tasks.py — GET /api/tasks/{id}
- [x] 5.4 routers/tasks.py — PUT /api/tasks/{id} (status 변경, TODO/DOING/DONE 검증)
- [x] 5.5 routers/tasks.py — PUT /api/tasks/{id} (title 수정)
- [x] 5.6 routers/tasks.py — DELETE /api/tasks/{id}

## 6. 채팅 (Message)

- [x] 6.1 routers/messages.py — POST /api/teams/{id}/messages (1000자 제한, 빈 메시지 거부)
- [x] 6.2 routers/messages.py — GET /api/teams/{id}/messages (since 파라미터, 기본 최근 50개)
- [x] 6.3 routers/messages.py — GET /api/messages/{id}
- [x] 6.4 routers/messages.py — DELETE /api/messages/{id} (본인 메시지만 삭제)

## 7. main.py 통합

- [x] 7.1 FastAPI 앱 생성, CORS 미들웨어 설정 (허용 도메인 명시)
- [x] 7.2 4개 라우터 등록 (/api/auth, /api/teams, /api/tasks, /api 하위)
- [x] 7.3 StaticFiles 마운트 (static/ → /)

## 8. 프론트엔드 — 공통

- [x] 8.1 static/app.js — JWT localStorage 저장·불러오기·삭제 유틸
- [x] 8.2 static/app.js — API 공통 호출 함수 (Authorization 헤더 자동 주입)
- [x] 8.3 static/app.js — 에러 응답 공통 처리

## 9. 프론트엔드 — 화면 4종

- [x] 9.1 static/index.html — 로그인 화면 (로고, 이메일, 비밀번호, 로그인 버튼, 회원가입 링크)
- [x] 9.2 static/signup.html — 회원가입 화면 (이메일, 비밀번호, 가입 버튼)
- [x] 9.3 static/teams.html — 팀 선택 화면 (내 팀 목록, 팀 만들기, 초대코드 합류)
- [x] 9.4 static/kanban.html — 칸반 화면 (TODO/DOING/DONE 3컬럼, 태스크 카드, 드래그 상태 이동, + 버튼)
- [x] 9.5 static/chat.html — 채팅 화면 (메시지 리스트, 5초 폴링, 입력창, 발신자+시각 표시)

## 10. 배포

- [ ] 10.1 Vercel 계정 연결 및 프로젝트 생성
- [ ] 10.2 Neon DB 프로비저닝 및 DATABASE_URL 환경변수 Vercel에 등록
- [ ] 10.3 vercel deploy 실행 및 배포 URL 확인
- [ ] 10.4 배포 환경에서 회원가입→로그인→팀생성→칸반→채팅 전체 플로우 수동 확인
