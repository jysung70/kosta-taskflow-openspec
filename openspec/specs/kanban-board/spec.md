# kanban-board Specification

## Purpose

태스크 생성, 조회, 상태 변경(TODO/DOING/DONE), 제목 수정, 삭제 등 칸반 보드 기능을 제공한다.

## Requirements

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

---

### Requirement: 팀 태스크 목록 조회
시스템은 팀 소속 멤버가 해당 팀의 전체 태스크를 조회할 수 있어야 한다(SHALL).

#### Scenario: 정상 조회
- **WHEN** GET /api/teams/1/tasks (팀 멤버 로그인 상태)
- **THEN** HTTP 200, [{"id": 1, "title": "로그인 화면 구현", "status": "TODO"}, ...]

#### Scenario: 태스크 없음
- **WHEN** 태스크가 없는 팀의 GET /api/teams/1/tasks
- **THEN** HTTP 200, []

---

### Requirement: 태스크 상태 변경
시스템은 팀 소속 멤버가 태스크 상태를 TODO/DOING/DONE 중 하나로 변경할 수 있어야 한다(SHALL). 유효하지 않은 상태값은 거부(MUST).

#### Scenario: 정상 상태 변경
- **WHEN** PUT /api/tasks/1 {"status": "DOING"} (팀 멤버 로그인 상태)
- **THEN** HTTP 200, {"id": 1, "status": "DOING"}

#### Scenario: 유효하지 않은 상태값
- **WHEN** PUT /api/tasks/1 {"status": "INVALID"}
- **THEN** HTTP 422, 유효성 검사 오류

---

### Requirement: 태스크 상태 변경 (PATCH 전용 엔드포인트)
시스템은 `PATCH /api/tasks/{id}/status`로 태스크 상태만 변경하는 전용 엔드포인트를 제공해야 한다(SHALL). 칸반 드래그 앤 드롭은 이 엔드포인트를 사용해야 한다(MUST).

#### Scenario: PATCH로 상태 변경
- **WHEN** PATCH /api/tasks/1/status {"status": "DOING"}
- **THEN** HTTP 200, {"id": 1, "status": "DOING"}

#### Scenario: 유효하지 않은 상태값
- **WHEN** PATCH /api/tasks/1/status {"status": "INVALID"}
- **THEN** HTTP 422, 유효성 검사 오류

---

### Requirement: 태스크 제목 수정
시스템은 팀 소속 멤버가 태스크 제목을 수정할 수 있어야 한다(SHALL).

#### Scenario: 정상 제목 수정
- **WHEN** PUT /api/tasks/1 {"title": "수정된 제목"} (팀 멤버 로그인 상태)
- **THEN** HTTP 200, {"id": 1, "title": "수정된 제목"}

---

### Requirement: 태스크 삭제
시스템은 팀 소속 멤버가 태스크를 삭제할 수 있어야 한다(SHALL).

#### Scenario: 정상 삭제
- **WHEN** DELETE /api/tasks/1 (팀 멤버 로그인 상태)
- **THEN** HTTP 200, {"msg": "삭제되었습니다"}

#### Scenario: 존재하지 않는 태스크 삭제
- **WHEN** DELETE /api/tasks/999
- **THEN** HTTP 404, {"code": "NOT_FOUND", "msg": "태스크를 찾을 수 없습니다"}

---

### Requirement: 태스크 단건 조회
시스템은 팀 소속 멤버가 태스크 단건을 조회할 수 있어야 한다(SHALL).

#### Scenario: 정상 단건 조회
- **WHEN** GET /api/tasks/1 (팀 멤버 로그인 상태)
- **THEN** HTTP 200, {"id": 1, "title": "로그인 화면 구현", "status": "TODO", "creator_id": 1}
