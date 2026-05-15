# deployment Specification

## Purpose

로컬 SQLite 기반 개발 환경 기동, Vercel 배포, Neon PostgreSQL 연동, 정적 파일 서빙 등 배포 및 실행 환경 요구사항을 정의한다.

## Requirements

### Requirement: 로컬 개발 환경 기동
시스템은 `DATABASE_URL` 환경변수 없이 로컬 SQLite로 즉시 기동되어야 한다(SHALL). `uvicorn main:app --reload` 한 명령으로 FE+BE 동시 서빙(MUST).

#### Scenario: 로컬 기동
- **WHEN** DATABASE_URL 없이 `uvicorn main:app --reload` 실행
- **THEN** http://localhost:8000 에서 FE 화면 접근 가능, ./taskflow.db 자동 생성

#### Scenario: 로컬 API 동작
- **WHEN** http://localhost:8000/api/auth/signup 호출
- **THEN** SQLite에 사용자 저장, JWT 반환

---

### Requirement: Vercel 배포
시스템은 `vercel deploy` 한 명령으로 배포되어야 한다(SHALL). 배포 완료까지 5분 이내(MUST).

#### Scenario: 정상 Vercel 배포
- **WHEN** `vercel deploy` 실행 (DATABASE_URL 환경변수 설정됨)
- **THEN** 5분 이내 배포 URL 발급, FastAPI 앱이 Vercel Functions로 동작

#### Scenario: DATABASE_URL 미설정 시 배포
- **WHEN** DATABASE_URL 없이 Vercel 배포
- **THEN** 앱 기동 오류 또는 SQLite 대체 동작 (명시적 오류 메시지 출력)

---

### Requirement: Neon PostgreSQL 연동
시스템은 `DATABASE_URL` 환경변수(Neon Pooled 연결 문자열)로 PostgreSQL에 자동 연결해야 한다(SHALL). 테이블 자동 생성(MUST).

#### Scenario: Neon 연결 성공
- **WHEN** DATABASE_URL=postgresql+psycopg2://... 환경변수로 앱 기동
- **THEN** Neon DB에 4개 테이블 자동 생성, API 정상 동작

#### Scenario: 연결 실패
- **WHEN** 잘못된 DATABASE_URL로 앱 기동
- **THEN** 기동 시 명확한 연결 오류 메시지 출력

---

### Requirement: 정적 파일 서빙
시스템은 FastAPI StaticFiles로 FE 파일을 서빙해야 한다(SHALL). `/api/` 경로는 API 라우터, 나머지는 FE 파일(MUST).

#### Scenario: 루트 경로 접근
- **WHEN** GET http://localhost:8000/
- **THEN** index.html (로그인 화면) 반환

#### Scenario: API 경로 분리
- **WHEN** GET http://localhost:8000/api/auth/me
- **THEN** FE 파일이 아닌 API 응답 반환
