## ADDED Requirements

### Requirement: 회원가입
시스템은 이메일과 비밀번호를 받아 사용자를 생성하고 JWT를 발급해야 한다(SHALL). 비밀번호는 bcrypt로 해시 저장해야 한다(MUST). 중복 이메일은 거부해야 한다(MUST).

#### Scenario: 정상 가입
- **WHEN** POST /api/auth/signup {"email": "user@example.com", "password": "pass1234"}
- **THEN** HTTP 201, {"token": "<JWT>", "user": {"id": 1, "email": "user@example.com"}}

#### Scenario: 중복 이메일 가입
- **WHEN** 이미 존재하는 이메일로 POST /api/auth/signup
- **THEN** HTTP 409, {"code": "EMAIL_EXISTS", "msg": "이미 사용 중인 이메일입니다"}

#### Scenario: 비밀번호 누락
- **WHEN** password 필드 없이 POST /api/auth/signup
- **THEN** HTTP 422, 유효성 검사 오류 응답

---

### Requirement: 로그인
시스템은 이메일·비밀번호 검증 후 JWT(24h 만료, 갱신 없음)를 발급해야 한다(SHALL).

#### Scenario: 정상 로그인
- **WHEN** POST /api/auth/login {"email": "user@example.com", "password": "pass1234"}
- **THEN** HTTP 200, {"token": "<JWT>", "user": {"id": 1, "email": "user@example.com"}}

#### Scenario: 잘못된 비밀번호
- **WHEN** 올바르지 않은 비밀번호로 POST /api/auth/login
- **THEN** HTTP 401, {"code": "INVALID_CREDENTIALS", "msg": "이메일 또는 비밀번호가 올바르지 않습니다"}

---

### Requirement: 내 정보 조회
시스템은 유효한 JWT로 현재 로그인 사용자 정보를 반환해야 한다(SHALL).

#### Scenario: 정상 조회
- **WHEN** GET /api/auth/me (Authorization: Bearer <유효한 JWT>)
- **THEN** HTTP 200, {"id": 1, "email": "user@example.com"}

#### Scenario: 만료된 JWT
- **WHEN** GET /api/auth/me (Authorization: Bearer <만료된 JWT>)
- **THEN** HTTP 401, {"code": "TOKEN_EXPIRED", "msg": "로그인이 만료되었습니다"}

---

### Requirement: 로그아웃
시스템은 로그아웃 요청을 수락해야 한다(SHALL). 서버 측 토큰 무효화는 하지 않는다(클라이언트가 localStorage에서 제거).

#### Scenario: 정상 로그아웃
- **WHEN** POST /api/auth/logout (Authorization: Bearer <유효한 JWT>)
- **THEN** HTTP 200, {"msg": "로그아웃 되었습니다"}
