## ADDED Requirements

### Requirement: 태스크 상태 변경 (PATCH 전용 엔드포인트)
시스템은 `PATCH /api/tasks/{id}/status`로 태스크 상태만 변경하는 전용 엔드포인트를 제공해야 한다(SHALL). 칸반 드래그 앤 드롭은 이 엔드포인트를 사용해야 한다(MUST).

#### Scenario: PATCH로 상태 변경
- **WHEN** PATCH /api/tasks/1/status {"status": "DOING"}
- **THEN** HTTP 200, {"id": 1, "status": "DOING"}

#### Scenario: 유효하지 않은 상태값
- **WHEN** PATCH /api/tasks/1/status {"status": "INVALID"}
- **THEN** HTTP 422, 유효성 검사 오류

## MODIFIED Requirements

### Requirement: 태스크 생성
시스템은 팀 소속 멤버가 태스크를 생성할 수 있어야 한다(SHALL). `assignee_id` 필드를 선택적으로 받아야 한다(MUST). 초기 상태는 항상 TODO(MUST).

#### Scenario: 정상 생성 (assignee 포함)
- **WHEN** POST /api/teams/1/tasks {"title": "로그인 화면 구현", "assignee_id": 1}
- **THEN** HTTP 201, {"id": 1, "title": "로그인 화면 구현", "status": "TODO", "creator_id": 1, "assignee_id": 1, "team_id": 1}

#### Scenario: 정상 생성 (assignee 없음)
- **WHEN** POST /api/teams/1/tasks {"title": "로그인 화면 구현"}
- **THEN** HTTP 201, assignee_id = null

#### Scenario: 비소속 팀에 태스크 생성
- **WHEN** 소속되지 않은 팀에 POST /api/teams/99/tasks
- **THEN** HTTP 403, {"code": "FORBIDDEN", "msg": "해당 팀에 접근 권한이 없습니다"}
