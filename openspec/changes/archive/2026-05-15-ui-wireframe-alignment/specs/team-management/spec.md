## MODIFIED Requirements

### Requirement: 팀 생성
시스템은 로그인된 사용자가 팀을 생성하고 고유 초대코드를 자동 발급해야 한다(SHALL). 생성 후 성공 화면에 초대코드 복사 버튼과 "칸반 시작하기" 버튼을 표시해야 한다(MUST). 팀 생성 시 `users.team_id`를 해당 팀 id로 업데이트해야 한다(MUST).

#### Scenario: 정상 팀 생성 후 성공 화면
- **WHEN** POST /api/teams {"name": "개발팀"} 성공
- **THEN** 성공 화면 표시: 팀 이름, 초대코드(복사 버튼), "칸반 시작하기 →" 버튼

#### Scenario: 팀 이름 누락
- **WHEN** name 없이 POST /api/teams
- **THEN** HTTP 422, 유효성 검사 오류

---

### Requirement: 초대코드로 팀 합류
시스템은 유효한 초대코드로 팀에 합류할 수 있어야 한다(SHALL). 합류 시 `users.team_id`를 해당 팀 id로 업데이트해야 한다(MUST).

#### Scenario: 정상 합류 후 칸반 이동
- **WHEN** POST /api/teams/join {"invite_code": "ABCD-1234"} 성공
- **THEN** HTTP 200, {"id": 1, "name": "개발팀"}, FE에서 /kanban?team=1로 이동

#### Scenario: 잘못된 초대코드
- **WHEN** 존재하지 않는 초대코드로 POST /api/teams/join
- **THEN** HTTP 404, {"code": "INVALID_INVITE_CODE", "msg": "유효하지 않은 초대코드입니다"}

#### Scenario: 이미 소속된 팀
- **WHEN** 이미 합류한 팀의 초대코드로 POST /api/teams/join
- **THEN** HTTP 409, {"code": "ALREADY_MEMBER", "msg": "이미 소속된 팀입니다"}
