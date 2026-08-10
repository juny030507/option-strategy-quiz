# 최종 제출 체크리스트

## 텍스트 검증

- [x] Python 3.10.4에서 전체 67개 테스트 통과
- [x] 원격 문서 브랜치를 새 clone에서 동일하게 검증
- [x] `python3 main.py`의 5번 정상 종료 통과
- [x] README 상대 링크 확인
- [x] `state.json` JSON 문법, 10문제·최고 점수 0/0·누적 0/0 확인
- [x] GitHub Actions의 PR·`main` push 실행 성공 확인
- [x] PR #13을 merge commit `fca0e08`로 `main`에 병합
- [x] `main` 브랜치 보호 규칙 API 재조회 확인
- [x] `git diff --check` 통과

## README 실행 결과 이미지

현재 브랜치의 실제 프로그램·테스트 출력에서 개인정보를 제거해 만든
기능별 이미지다. `README.md`에 모두 첨부했다.

- [x] 메인 메뉴
- [x] 사용자 퀴즈 추가와 퀴즈 목록
- [x] 퀴즈 풀이와 최고 점수 갱신
- [x] 최고 점수와 누적 통계
- [x] Python·Git 환경
- [x] 전체 67개 테스트와 Ruff 통과
- [x] 최고 점수 기능 브랜치와 커밋 그래프

## 사용자 직접 캡처할 실제 화면

최종 제출 전에 사용자가 실제 Terminal·VS Code·GitHub 화면에서 직접
캡처한다. README 이미지를 보완하거나 필요하면 교체한다.

- [ ] 메인 메뉴
- [ ] `0`을 이용한 메뉴 복귀
- [ ] 사용자 퀴즈 추가와 퀴즈 목록
- [ ] 퀴즈 완료 후 최고 점수와 누적 점수 화면
- [ ] 프로젝트 루트의 `state.json`
- [ ] 전체 67개 테스트 통과 터미널
- [ ] `git log --oneline --graph --decorate --all` 그래프
- [ ] GitHub PR #1부터 최종 PR까지의 목록
- [ ] GitHub Actions `Python 3.10 unit tests` 성공 화면
- [ ] `main` 브랜치 보호 설정 화면

## 최종 수동 검토

- [ ] README의 사용법과 JSON 예시 재확인
- [ ] 코드를 파일별로 직접 설명하는 전체 리뷰·스터디
- [ ] 캡처 파일에 개인정보·절대경로·토큰이 노출되지 않았는지 확인
