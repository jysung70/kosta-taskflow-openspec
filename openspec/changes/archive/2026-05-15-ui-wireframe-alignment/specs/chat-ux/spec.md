## ADDED Requirements

### Requirement: 채팅 폴링 인디케이터
채팅 헤더에 `● 5초마다 새로고침` 인디케이터가 표시되어야 한다(SHALL).

#### Scenario: 폴링 인디케이터 표시
- **WHEN** 채팅 화면 로드
- **THEN** 헤더 우측에 초록 점 + "5초마다 새로고침" 텍스트 표시

---

### Requirement: 채팅 Empty State
메시지가 없을 때 아이콘과 안내 문구를 표시해야 한다(SHALL).

#### Scenario: 빈 채팅 Empty State
- **WHEN** 팀의 메시지가 0건
- **THEN** 말풍선 아이콘 + "아직 대화가 없습니다" + "첫 메시지를 보내 팀원과 대화를 시작하세요" 표시
