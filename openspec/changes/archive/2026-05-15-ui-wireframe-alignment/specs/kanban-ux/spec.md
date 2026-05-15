## ADDED Requirements

### Requirement: 칸반 컬럼 헤더 카운트 및 색상
각 컬럼 헤더는 태스크 수와 색상 배경을 표시해야 한다(SHALL). TODO=노란, DOING=파란, DONE=초록(MUST).

#### Scenario: 태스크 있는 칸반 컬럼 헤더
- **WHEN** TODO 컬럼에 태스크 3개 존재
- **THEN** 헤더에 `TODO · 3` 형식으로 표시, 노란 배경

#### Scenario: 빈 칸반 컬럼 헤더
- **WHEN** DOING 컬럼에 태스크 없음
- **THEN** 헤더에 `DOING · 0` 표시

---

### Requirement: 칸반 카드 assignee 표시
태스크 카드는 제목과 함께 `#id · @assignee` 형식으로 표시해야 한다(SHALL).

#### Scenario: 카드 정보 표시
- **WHEN** 태스크 id=100, assignee=me 인 카드 렌더링
- **THEN** 카드 하단에 `#100 · @me` 표시

#### Scenario: 미할당 카드
- **WHEN** assignee_id가 null인 카드
- **THEN** `#100 · 미할당` 표시

---

### Requirement: 칸반 필터 탭
칸반 보드 상단에 전체/내 카드/@me/미할당 필터 탭이 있어야 한다(SHALL).

#### Scenario: 전체 필터 (기본값)
- **WHEN** 칸반 화면 진입
- **THEN** `전체` 탭 활성, 모든 태스크 표시

#### Scenario: @me 필터
- **WHEN** `@me` 탭 클릭
- **THEN** assignee_id = 현재 사용자 인 태스크만 표시

#### Scenario: 미할당 필터
- **WHEN** `미할당` 탭 클릭
- **THEN** assignee_id = null 인 태스크만 표시

---

### Requirement: 칸반 인라인 태스크 생성
`+` 버튼 클릭 시 인라인 입력폼이 컬럼 상단에 나타나야 한다(SHALL). Enter로 저장, Esc로 취소(MUST).

#### Scenario: 인라인 태스크 생성
- **WHEN** TODO 컬럼 `+` 클릭 → 제목 입력 → Enter
- **THEN** POST /api/teams/{id}/tasks 호출, 카드가 TODO 컬럼에 즉시 추가

---

### Requirement: 칸반 Empty State
태스크가 없는 컬럼은 아이콘 + 안내 문구를 표시해야 한다(SHALL). TODO 컬럼에만 CTA 표시(MUST).

#### Scenario: TODO Empty State
- **WHEN** TODO 컬럼에 태스크 없음
- **THEN** 클립보드 아이콘 + "카드 없음" + "+ 첫 태스크 만들기" 링크 표시

#### Scenario: DOING/DONE Empty State
- **WHEN** DOING 또는 DONE 컬럼에 태스크 없음
- **THEN** 클립보드 아이콘 + "카드 없음" + "드래그로 이동" 안내 표시
