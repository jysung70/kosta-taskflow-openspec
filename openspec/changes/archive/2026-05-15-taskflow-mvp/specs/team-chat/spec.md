## ADDED Requirements

### Requirement: 메시지 전송
시스템은 팀 소속 멤버가 텍스트 메시지를 전송할 수 있어야 한다(SHALL). 메시지는 최대 1000자(MUST). 빈 메시지는 거부(MUST).

#### Scenario: 정상 메시지 전송
- **WHEN** POST /api/teams/1/messages {"content": "안녕하세요"} (팀 멤버 로그인 상태)
- **THEN** HTTP 201, {"id": 1, "content": "안녕하세요", "user_id": 1, "team_id": 1, "created_at": "2026-05-15T10:00:00Z"}

#### Scenario: 1000자 초과 메시지
- **WHEN** content가 1001자인 메시지 POST
- **THEN** HTTP 422, {"code": "MSG_TOO_LONG", "msg": "메시지는 1000자 이내여야 합니다"}

#### Scenario: 빈 메시지
- **WHEN** content가 빈 문자열인 메시지 POST
- **THEN** HTTP 422, 유효성 검사 오류

---

### Requirement: 메시지 목록 조회 (폴링)
시스템은 `since` 파라미터(ISO 8601) 이후의 메시지만 반환해야 한다(SHALL). since 없으면 최근 50개 반환(MUST). 클라이언트는 5초마다 폴링해야 한다.

#### Scenario: since 없이 초기 조회
- **WHEN** GET /api/teams/1/messages (팀 멤버 로그인 상태)
- **THEN** HTTP 200, 최근 50개 메시지 배열, 각 항목 {"id", "content", "user_id", "created_at", "sender_email"}

#### Scenario: since 이후 메시지 조회 (폴링)
- **WHEN** GET /api/teams/1/messages?since=2026-05-15T10:00:00Z
- **THEN** HTTP 200, 해당 시각 이후 신규 메시지만 반환 (없으면 [])

#### Scenario: 비소속 팀 메시지 조회
- **WHEN** 소속되지 않은 팀의 메시지 GET
- **THEN** HTTP 403, {"code": "FORBIDDEN", "msg": "해당 팀에 접근 권한이 없습니다"}

---

### Requirement: 메시지 단건 조회
시스템은 팀 소속 멤버가 특정 메시지를 조회할 수 있어야 한다(SHALL).

#### Scenario: 정상 단건 조회
- **WHEN** GET /api/messages/1 (팀 멤버 로그인 상태)
- **THEN** HTTP 200, {"id": 1, "content": "안녕하세요", "user_id": 1, "created_at": "2026-05-15T10:00:00Z"}

---

### Requirement: 메시지 삭제
시스템은 메시지 발신자 본인만 삭제할 수 있어야 한다(SHALL).

#### Scenario: 본인 메시지 삭제
- **WHEN** DELETE /api/messages/1 (발신자 본인 로그인 상태)
- **THEN** HTTP 200, {"msg": "삭제되었습니다"}

#### Scenario: 타인 메시지 삭제 시도
- **WHEN** 본인이 아닌 메시지에 DELETE /api/messages/1
- **THEN** HTTP 403, {"code": "FORBIDDEN", "msg": "본인 메시지만 삭제할 수 있습니다"}
