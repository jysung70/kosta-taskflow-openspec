## 1. BE — DB 스키마 변경

- [x] 1.1 models.py — Task에 assignee_id 컬럼 추가 (nullable, FK users.id)
- [x] 1.2 models.py — User에 team_id 컬럼 추가 (nullable, FK teams.id)
- [x] 1.3 main.py — startup_event에 ALTER TABLE 추가 (tasks.assignee_id, users.team_id)

## 2. BE — 라우터 수정

- [x] 2.1 routers/tasks.py — PATCH /api/tasks/{id}/status 엔드포인트 추가
- [x] 2.2 routers/tasks.py — CreateTaskRequest에 assignee_id 옵션 필드 추가
- [x] 2.3 routers/auth.py — 로그인/회원가입 응답에 user.team_id 포함
- [x] 2.4 routers/teams.py — 팀 생성 시 users.team_id 업데이트
- [x] 2.5 routers/teams.py — 팀 합류 시 users.team_id 업데이트

## 3. FE — 공통 (app.js, 헤더)

- [x] 3.1 static/app.js — saveAuth()에 team_id 저장, getUser()에 team_id 포함
- [x] 3.2 static/app.js — 로그인 성공 후 team_id 분기 함수 추가 (null→/teams, 값→/kanban?team=N)
- [x] 3.3 공통 헤더 HTML 스니펫 — 탭 네비게이션 (칸반|채팅|멤버) 포함

## 4. FE — 로그인/회원가입 화면

- [x] 4.1 static/index.html — 로그인 버튼 로딩 상태 ("처리 중...") 추가
- [x] 4.2 static/index.html — 로그인 성공 후 team_id 분기 적용
- [x] 4.3 static/signup.html — 비밀번호 8자 이상 클라이언트 검증 추가
- [x] 4.4 static/signup.html — 가입하기 버튼 로딩 상태 추가
- [x] 4.5 static/signup.html — 인라인 에러 표시 (필드 하단)

## 5. FE — 팀 선택 화면

- [x] 5.1 static/teams.html — 팀 생성 성공 화면 추가 (초대코드 복사 버튼 + "칸반 시작하기 →")
- [x] 5.2 static/teams.html — 팀 합류 성공 후 /kanban?team=N 자동 이동

## 6. FE — 칸반 화면

- [x] 6.1 static/kanban.html — 헤더 탭 네비게이션 (칸반 활성 | 채팅 | 멤버)
- [x] 6.2 static/kanban.html — 컬럼 헤더 색상 + 카운트 표시 (TODO·N 형식)
- [x] 6.3 static/kanban.html — 카드에 #id · @assignee 표시
- [x] 6.4 static/kanban.html — 필터 탭 (전체/@me/미할당) UI 및 JS 로직
- [x] 6.5 static/kanban.html — 인라인 태스크 생성 폼 (담당자 @me 기본값)
- [x] 6.6 static/kanban.html — 드래그 드롭 → PATCH /api/tasks/{id}/status 사용
- [x] 6.7 static/kanban.html — Empty state (아이콘 + "카드 없음" + 안내 문구)
- [x] 6.8 static/kanban.html — 모바일 반응형 (768px 이하 1컬럼 + 탭 전환)

## 7. FE — 채팅 화면

- [x] 7.1 static/chat.html — 헤더 탭 네비게이션 (칸반 | 채팅 활성 | 멤버)
- [x] 7.2 static/chat.html — 헤더에 "● 5초마다 새로고침" 인디케이터 추가
- [x] 7.3 static/chat.html — Empty state (말풍선 아이콘 + "아직 대화가 없습니다")

## 8. 배포 및 검증

- [ ] 8.1 vercel deploy --prod 실행
- [ ] 8.2 Neon에서 tasks.assignee_id, users.team_id 컬럼 추가 확인
- [ ] 8.3 브라우저에서 전체 플로우 수동 확인 (회원가입→팀생성→칸반→채팅)
- [ ] 8.4 모바일 뷰포트 (768px 이하) 칸반 1컬럼 확인
