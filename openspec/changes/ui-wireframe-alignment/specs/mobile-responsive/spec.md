## ADDED Requirements

### Requirement: 모바일 칸반 1컬럼 레이아웃
768px 미만 화면에서 칸반 보드는 1컬럼으로 전환되어야 한다(SHALL). 탭 인디케이터로 현재 컬럼 표시(MUST).

#### Scenario: 모바일 칸반 진입
- **WHEN** 뷰포트 너비 < 768px 에서 칸반 화면 로드
- **THEN** TODO/DOING/DONE 탭이 상단에 표시, 선택된 컬럼만 1열로 렌더링

#### Scenario: 모바일 탭 전환
- **WHEN** DOING 탭 클릭
- **THEN** DOING 컬럼 태스크 목록만 표시

#### Scenario: 데스크탑 칸반
- **WHEN** 뷰포트 너비 ≥ 768px
- **THEN** TODO/DOING/DONE 3컬럼 나란히 표시 (기존 동작 유지)
