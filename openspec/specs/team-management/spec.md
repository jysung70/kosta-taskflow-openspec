# team-management Specification

## Purpose

팀 생성, 초대코드 발급, 팀 합류, 팀 목록 조회, 멤버 목록 조회 등 팀 관리 기능을 제공한다.

## Requirements

### Requirement: 팀 생성
시스템은 로그인된 사용자가 팀을 생성하고 고유 초대코드(ABCD-1234 형식, 영문대문자4자-숫자4자)를 자동 발급해야 한다(SHALL). 생성자가 owner가 된다(MUST).

#### Scenario: 정상 팀 생성
- **WHEN** POST /api/teams {"name": "개발팀"} (로그인 상태)
- **THEN** HTTP 201, {"id": 1, "name": "개발팀", "invite_code": "ABCD-1234", "owner_id": 1}

#### Scenario: 팀 이름 누락
- **WHEN** name 없이 POST /api/teams
- **THEN** HTTP 422, 유효성 검사 오류

---

### Requirement: 내 팀 목록 조회
시스템은 현재 사용자가 속한 모든 팀 목록을 반환해야 한다(SHALL).

#### Scenario: 정상 목록 조회
- **WHEN** GET /api/teams (로그인 상태)
- **THEN** HTTP 200, [{"id": 1, "name": "개발팀", "invite_code": "ABCD-1234"}]

#### Scenario: 소속 팀 없음
- **WHEN** 아직 팀에 속하지 않은 사용자가 GET /api/teams
- **THEN** HTTP 200, []

---

### Requirement: 초대코드로 팀 합류
시스템은 유효한 초대코드로 팀에 합류할 수 있어야 한다(SHALL). 이미 소속된 팀은 중복 합류 불가(MUST).

#### Scenario: 정상 합류
- **WHEN** POST /api/teams/join {"invite_code": "ABCD-1234"} (로그인 상태)
- **THEN** HTTP 200, {"id": 1, "name": "개발팀"}

#### Scenario: 잘못된 초대코드
- **WHEN** 존재하지 않는 초대코드로 POST /api/teams/join
- **THEN** HTTP 404, {"code": "INVALID_INVITE_CODE", "msg": "유효하지 않은 초대코드입니다"}

#### Scenario: 이미 소속된 팀
- **WHEN** 이미 합류한 팀의 초대코드로 POST /api/teams/join
- **THEN** HTTP 409, {"code": "ALREADY_MEMBER", "msg": "이미 소속된 팀입니다"}

---

### Requirement: 팀 멤버 목록 조회
시스템은 해당 팀 소속 멤버만 멤버 목록을 조회할 수 있어야 한다(SHALL).

#### Scenario: 정상 조회
- **WHEN** GET /api/teams/1/members (해당 팀 멤버인 로그인 상태)
- **THEN** HTTP 200, [{"id": 1, "email": "user@example.com"}]

#### Scenario: 비소속 팀 조회
- **WHEN** 소속되지 않은 팀의 멤버 조회
- **THEN** HTTP 403, {"code": "FORBIDDEN", "msg": "해당 팀에 접근 권한이 없습니다"}
