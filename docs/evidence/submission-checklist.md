# 최종 제출 체크리스트

## 텍스트 검증

- [x] Python 3.10.4에서 전체 58개 테스트 통과
- [x] 원격 문서 브랜치를 새 clone에서 동일하게 검증
- [x] `python3 main.py`의 5번 정상 종료 통과
- [x] README 상대 링크 확인
- [x] `state.json` JSON 문법, 10문제·0/0점, SHA-256 확인
- [x] GitHub Actions의 PR·`main` push 실행 성공 확인
- [x] `main` 브랜치 보호 규칙 API 재조회 확인
- [x] `git diff --check` 통과

## 사용자 직접 캡처할 UI 스크린샷

아래 이미지 파일은 생성한 것처럼 기록하지 않았다. 최종 제출 전에
사용자가 실제 화면에서 직접 캡처한다.

- [ ] 메인 메뉴
- [ ] `0`을 이용한 메뉴 복귀
- [ ] 사용자 퀴즈 추가와 퀴즈 목록
- [ ] 누적 점수와 정답률 화면
- [ ] 프로젝트 루트의 `state.json`
- [ ] 전체 58개 테스트 통과 터미널
- [ ] `git log --oneline --graph --decorate --all` 그래프
- [ ] GitHub PR #1부터 최종 PR까지의 목록
- [ ] GitHub Actions `Python 3.10 unit tests` 성공 화면
- [ ] `main` 브랜치 보호 설정 화면

## 최종 수동 검토

- [ ] README의 사용법과 JSON 예시 재확인
- [ ] 코드를 파일별로 직접 설명하는 전체 리뷰·스터디
- [ ] 캡처 파일에 개인정보·절대경로·토큰이 노출되지 않았는지 확인
