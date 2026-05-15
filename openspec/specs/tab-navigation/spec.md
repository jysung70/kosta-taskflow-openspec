# tab-navigation Specification

## Purpose

팀 컨텍스트 화면(칸반·채팅·멤버)에서 헤더 탭 네비게이션을 통해 화면 간 이동을 제공한다.

## Requirements

### Requirement: 팀 컨텍스트 탭 네비게이션
칸반·채팅·멤버 화면에서 헤더에 탭 네비게이션이 표시되어야 한다(SHALL). 현재 활성 탭은 강조 표시(MUST). 탭 클릭 시 해당 URL로 이동(MUST).

#### Scenario: 칸반 화면에서 탭 표시
- **WHEN** `/kanban?team=1` 페이지 로드
- **THEN** 헤더에 `칸반(활성) | 채팅 | 멤버` 탭이 표시됨

#### Scenario: 채팅 탭 클릭
- **WHEN** 칸반 화면에서 `채팅` 탭 클릭
- **THEN** `/chat?team=1`로 이동

#### Scenario: 멤버 탭 클릭
- **WHEN** 채팅 화면에서 `멤버` 탭 클릭
- **THEN** `/members?team=1`로 이동 또는 멤버 목록 표시
