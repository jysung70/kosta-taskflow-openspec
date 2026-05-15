# auth-ux Specification

## Purpose

로그인·회원가입 화면의 UX 동작(로딩 상태, 유효성 검증, 로그인 후 분기 등)을 정의한다.

## Requirements

### Requirement: 로그인/회원가입 로딩 상태
제출 버튼은 API 호출 중 "처리 중..." 텍스트와 비활성 상태로 변경되어야 한다(SHALL).

#### Scenario: 로그인 처리 중 상태
- **WHEN** 로그인 버튼 클릭 후 API 응답 대기 중
- **THEN** 버튼 텍스트 "처리 중...", disabled 상태

---

### Requirement: 비밀번호 8자 이상 검증
회원가입 시 비밀번호는 8자 이상이어야 한다(SHALL). 클라이언트 측 검증 우선(MUST).

#### Scenario: 비밀번호 8자 미만
- **WHEN** 회원가입 시 비밀번호 3자 입력 후 가입하기 클릭
- **THEN** 비밀번호 필드 아래 "8자 이상 입력해주세요" 에러 표시, API 호출 안 함

---

### Requirement: 로그인 성공 후 팀 분기
로그인 성공 시 `users.team_id` 값에 따라 분기되어야 한다(SHALL).

#### Scenario: 팀 없는 사용자 로그인
- **WHEN** 로그인 성공, 응답의 user.team_id = null
- **THEN** `/teams`로 이동

#### Scenario: 팀 있는 사용자 로그인
- **WHEN** 로그인 성공, 응답의 user.team_id = 5
- **THEN** `/kanban?team=5`로 바로 이동
