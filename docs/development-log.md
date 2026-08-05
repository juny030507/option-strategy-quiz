# 개발 과정 기록

## 기록 원칙

- Git 커밋, 브랜치, PR 이력을 개발 과정의 우선 근거로 사용한다.
- 중요한 테스트 결과와 오류 해결 과정만 기록한다.
- 명령 오타 같은 사소한 시행착오는 학습 가치가 있을 때만 요약한다.
- 비밀번호, 토큰, 불필요한 절대 경로 등 개인정보는 기록하지 않는다.
- 모든 단계의 개발 주체는 사용자 직접 수행으로 기록한다.
- 최종 README에는 이 문서를 링크하고 핵심 내용만 요약할 예정이다.

## Git 및 기능 개발 이력

아래 이력은 로컬 `git log --all --graph --decorate --oneline`과 병합
커밋을 기준으로 확인했다.

### PR #1: 메인 메뉴 반복 실행

- 날짜: 2026-08-03
- 브랜치: `feature/menu`
- 핵심 기능: 프로그램 기본 구조와 반복 실행되는 메인 메뉴 구현
- 기능 커밋: `abd9e16`
- 병합 커밋: `f1e2dbc`

### PR #2: 숫자 입력 검증과 안전 종료

- 날짜: 2026-08-03
- 브랜치: `feature/input-validation`
- 핵심 기능: 메뉴 숫자 범위 검증과 입력 중단 시 안전 종료 처리
- 기능 커밋: `3521244`
- 병합 커밋: `4c3b24e`

### PR #3: Quiz 클래스와 테스트

- 날짜: 2026-08-03
- 브랜치: `feature/quiz-model`
- 핵심 기능: `Quiz` 모델, 네 개 선택지와 정답 범위 검증, 핵심 동작 테스트
- 기능 커밋: `0176c09`
- 테스트 커밋: `4b60f03`
- 병합 커밋: `1c78a0b`

### PR #4: 기본 옵션 퀴즈 데이터와 품질 테스트

- 날짜: 2026-08-04
- 브랜치: `feature/default-quizzes`
- 핵심 기능: 옵션 전략, 델타헤지, 포트폴리오 보험 기본 퀴즈와 품질 테스트
- 데이터 커밋: `b474ca6`, `96f1c87`
- 테스트 커밋: `e51e39b`
- 병합 커밋: `df11df0`

### PR #5: QuizGame 클래스와 점수 테스트

- 날짜: 2026-08-04
- 브랜치: `feature/quiz-game`
- 핵심 기능: 퀴즈 목록, 답안 제출, 누적 점수와 정답률 관리
- 기능 커밋: `c1fc6b6`
- 테스트 커밋: `4bbd8ae`
- 병합 커밋: `12425f9`

### PR #6: 퀴즈 풀이 및 점수 확인

- 날짜: 2026-08-05
- 브랜치: `feature/play-score`
- 핵심 기능: 퀴즈 풀이 흐름, 정답 안내, 점수 출력 메뉴 연결
- 기능 커밋: `42413bb`
- 테스트 커밋: `1b7af4a`
- 정리 커밋: `2bddb4f`
- 병합 커밋: `15b175d`

### PR #7: 사용자 퀴즈 추가 및 목록 출력

- 날짜: 2026-08-05
- 브랜치: `feature/quiz-management`
- 핵심 기능: 사용자 퀴즈 입력, 퀴즈 추가, 등록된 퀴즈 목록 출력
- 기능 커밋: `8bb8cd2`
- 테스트 커밋: `261d5b4`
- 병합 커밋: `7554670`

### PR #8: JSON 게임 상태 저장 및 복원

- 날짜: 2026-08-05
- 브랜치: `feature/state-storage`
- 핵심 기능: 프로젝트 루트 `state.json` 저장 계층, 데이터 검증과 복구,
  저장 단위 테스트, `main.py` 시작·종료 및 변경 시점 연결
- 기능 커밋: `85cd205`, `7b4fc74`
- 테스트 커밋: `9f36dbe`, `da94100`
- 데이터 커밋: `adf0834`
- 문서 커밋: `2f8de19`, `cbd3e1c`
- PR: https://github.com/juny030507/option-strategy-quiz/pull/8
- 병합 커밋: `4cee799`

### PR #9: 퀴즈 흐름의 메인 메뉴 복귀

- 날짜: 2026-08-05
- 브랜치: `feature/menu-navigation`
- 핵심 기능: 퀴즈 풀이와 추가의 모든 입력 단계에서 0으로
  점수나 미완성 퀴즈를 변경하지 않고 메인 메뉴로 복귀
- 기능 커밋: `895011f`
- 테스트 커밋: `04eb721`
- 문서 커밋: `3832cd5`
- PR: https://github.com/juny030507/option-strategy-quiz/pull/9
- 병합 커밋: `4cd784a`

### PR #10: 최종 입력 검증과 코드 품질

- 날짜: 2026-08-05
- 브랜치: `refactor/final-quality`
- 핵심 기능: `Quiz`·`QuizGame` 불변 조건과 방어 경로 강화,
  숫자 입력 재시도·EOF 테스트, 커버드 콜 용어와 PEP 8 정리
- 기능 커밋: `8713c95`
- 테스트 커밋: `007a00e`
- 데이터 커밋: `bdb4f42`
- 문서 커밋: `b31924d`
- PR: https://github.com/juny030507/option-strategy-quiz/pull/10
- 병합 커밋: `18457dc`

### PR #11: Python 3.10 GitHub Actions

- 날짜: 2026-08-05
- 브랜치: `ci/github-actions`
- 핵심 기능: `main` push와 pull request에서 Python 3.10으로
  표준 라이브러리 단위 테스트 58개를 자동 실행
- CI 커밋: `dfdf0b9`
- 문서 커밋: `9d304fb`
- PR: https://github.com/juny030507/option-strategy-quiz/pull/11
- PR Actions: https://github.com/juny030507/option-strategy-quiz/actions/runs/30992519124
- `main` Actions: https://github.com/juny030507/option-strategy-quiz/actions/runs/30992597212
- 필수 검사 이름: `Python 3.10 unit tests`
- 병합 커밋: `43fe142`

## 테스트 증가 이력

| 전체 테스트 수 | 개발 단계 | 검증 범위의 의미 |
| ---: | --- | --- |
| 4개 | Quiz 핵심 동작 | 정답 판정, 선택지 수와 정답 번호 검증 |
| 8개 | 기본 퀴즈 데이터 | 기본 문제 수, 타입, 중복과 데이터 완전성 검증 포함 |
| 15개 | QuizGame | 퀴즈 추가, 누적 점수와 정답률 관리 검증 포함 |
| 21개 | 퀴즈 풀이와 점수 출력 | 실제 풀이 흐름, 입력 중단과 점수 화면 검증 포함 |
| 28개 | 사용자 퀴즈 관리 | 사용자 입력을 통한 추가와 목록 출력 검증 포함 |
| 38개 | JSON 저장 계층 | 직렬화, 왕복 저장, 손상·누락·I/O 오류 복구 검증 포함 |
| 42개 | main.py 저장 통합 | 시작 불러오기와 풀이·추가·종료 시 저장 호출 검증 포함 |
| 46개 | 메뉴 복귀 | 풀이와 추가의 각 입력 단계에서 0으로 취소하는 흐름 포함 |
| 58개 | 최종 코드 품질 | 모델 불변 조건, QuizGame 방어 경로, 숫자 입력 재시도·EOF와 금융 용어 검증 포함 |

## 주요 문제와 해결

- `instance`를 타입 검사 함수처럼 사용하면 런타임에 `NameError`가
  발생한다. 파이썬 내장 함수 `isinstance(value, Type)`를 사용해 객체
  타입을 명시적으로 확인했다.
- 테스트 파일만 존재하고 테스트 메서드가 없으면 파일을 커밋해도 테스트
  수가 증가하지 않는다. 테스트 발견 결과와 실제 실행 개수를 함께 확인했다.
- 테스트 메서드가 `setUp()` 안에 중첩되면 `unittest`가 클래스의
  테스트 메서드로 발견하지 못해 `Ran 0 tests`가 나온다. 모든
  `test_*` 메서드를 `unittest.TestCase` 클래스 바로 아래에 배치했다.
- 기대 출력과 실제 출력의 느낌표 하나 차이도 테스트 실패로 드러났다.
  사용자에게 보여 줄 문자열을 기준으로 구현과 테스트 기대값을 일치시켰다.
- `QuizGame` 객체 자체를 출력하면 기본 객체 표현에 메모리 주소가
  포함된다. 화면에는 객체 대신 퀴즈 수, 점수, 정답률처럼 필요한 속성을
  명시적으로 출력하도록 했다.
- Git 긴 옵션은 `--graph`, `--all`처럼 정확한 이름이 필요하다.
  명령이 성공했는지와 출력 대상 브랜치를 함께 확인해 기록의 신뢰성을
  확보했다.

## 개발 주체 기록

- PR #1부터 최종 문서 단계까지 설계, 구현, 테스트, Git·GitHub 작업과
  문서화를 사용자가 직접 수행했다.
- 기능·테스트·저장 통합·CI·브랜치 보호·문서 결정과 최종 결과를
  사용자가 테스트 결과와 Git diff로 직접 확인했다.
- 전체 구현 후 최종 코드 리뷰와 학습도 사용자가 코드를 직접 설명하는
  방식으로 진행할 예정이다.

## 터미널 검증 기록

### 2단계 저장 통합 당시

```bash
python3 -m py_compile main.py storage.py tests/test_main.py tests/test_storage.py
```

결과: 문법 검사 통과

```bash
python3 -m unittest discover -s tests -v
```

결과: 42개 테스트 통과

```bash
python3 -m json.tool state.json
```

결과: JSON 문법 검증 통과

```bash
git diff --check
```

결과: 공백 오류 없음

실제 프로그램 영속성 검증 결과:

- 첫 실행에서 프로젝트 루트의 `state.json`이 생성됐다.
- 사용자 퀴즈를 추가한 뒤 재실행했을 때 총 11개 퀴즈와 마지막 롱
  스트래들 문제가 유지됐다.
- 첫 번째 기본 문제를 맞힌 후 EOF로 풀이와 메뉴 입력을 중단했으며,
  재실행 후 `correct_count: 1`, `attempt_count: 1`, 정답률
  100.0%가 유지됐다.
- `python3 -m json.tool state.json`으로 JSON 문법 검증을 통과했다.
- 실제 상태 파일이 존재하는 상태에서도 전체 42개 테스트가 통과했다.
- 회귀 테스트 전후 상태 파일의 SHA-256 체크섬이 같아 테스트가 실제
  저장 데이터를 변경하지 않았음을 확인했다.

### 제출용 상태 초기화 결정

- 실제 영속성 검증에서 확인한 11개 퀴즈와 점수 1/1 결과는 위 기록에
  증거로 보존했다.
- 제출 파일에는 개인 검증 과정에서 추가한 퀴즈와 누적 점수를 남기지 않고,
  누구나 같은 첫 실행 상태에서 시작할 수 있도록 결정했다.
- `create_default_game()`과 `save_state()` 공개 함수를 사용해
  `state.json`을 기본 퀴즈 10개, `correct_count: 0`,
  `attempt_count: 0`으로 재생성했다.
- 재생성 후 JSON 문법과 전체 42개 테스트를 다시 검증했다.

### 4~5단계 최종 검증

- PR #11의 pull request 실행과 병합 후 `main` push 실행에서
  Python 3.10.20과 58개 테스트가 모두 통과했다.
- `main` 보호 규칙에 `Python 3.10 unit tests`, strict 상태 검사,
  PR 필수·승인 0명, 대화 해결 필수, 강제 push·삭제 금지를 적용했다.
- 제출용 `state.json`은 고유한 기본 퀴즈 10개, 각 선택지 4개,
  `correct_count: 0`, `attempt_count: 0`이며 SHA-256는
  `938a7ef9b9ca049fc53b5545c404a8b80c680dcc95e8528a86de45d444878e77`이다.
- 원격 `docs/final-readme` 브랜치를 새 임시 디렉터리에 clone한
  후 Python 3.10.4, 58개 테스트, `python3 main.py`의 5번 종료,
  README 상대 링크, JSON, 외부 절대경로 미사용과 깨끗한 작업 트리를
  확인했다.

## 남은 작업

- PR #12 Ready 전환·병합과 최신 `main`의 Actions·로컬 최종 검증
- 사용자의 UI 스크린샷 캡처
- 사용자 주도 전체 코드 리뷰와 스터디

### 단계 기록

- 날짜: 2026-08-05
- 단계: 2단계 - JSON 저장 기능 정리 및 로컬 게시 준비
- 작업 주체: 사용자 직접 수행
- 브랜치: `feature/state-storage`
- 목표: 저장 계층과 메인 연결을 검증하고 제출용 초기 상태로 정리해
  목적별 커밋을 생성
- 수정 파일: `storage.py`, `tests/test_storage.py`, `main.py`,
  `tests/test_main.py`, `state.json`, `docs/development-log.md`
- 설계 결정: 실제 11문제·1/1 영속성 검증 결과는 문서에 보존하고,
  제출 파일은 공개 저장 함수를 이용해 기본 10문제·0/0으로 초기화
- 주요 명령: `python3 -m json.tool state.json`,
  `python3 -m unittest discover -s tests -v`, `git diff --check`,
  파일별 `git add`와 `git commit`
- 테스트 결과: 저장 계층 10개, 메인 17개, 전체 42개 통과
- 발생한 문제: `gh auth status`에서 기본 GitHub 계정 토큰이
  유효하지 않은 것으로 확인됨
- 해결 방법: 인증을 우회하지 않고 안전한 로컬 커밋과 일반 push를
  완료한 뒤 사용자가 웹 인증을 승인해 GitHub CLI 인증을 복구
- 커밋: `85cd205` 저장 계층, `9f36dbe` 저장 테스트,
  `7b4fc74` 메인 연결, `da94100` 통합 테스트,
  `adf0834` 초기 상태 데이터, `2f8de19` 개발 로그
- 원격 push: `origin/feature/state-storage` 생성 및 추적 설정 완료
- PR: #8 - https://github.com/juny030507/option-strategy-quiz/pull/8
- 병합 결과: merge commit `4cee799`
- 남은 작업: 3~5단계

### 단계 기록

- 날짜: 2026-08-05
- 단계: 3-1단계 - 퀴즈 흐름의 메인 메뉴 복귀
- 작업 주체: 사용자 직접 수행
- 브랜치: `feature/menu-navigation`
- 목표: 퀴즈 풀이와 추가의 모든 입력 단계에서 0으로 메인 메뉴에 복귀
- 수정 파일: `main.py`, `tests/test_main.py`,
  `docs/development-log.md`
- 설계 결정: 0 입력은 점수와 미완성 퀴즈를 변경하지 않고 즉시 반환하며,
  기존 Ctrl+C·EOF 처리와 메인 저장 호출은 유지
- 주요 명령: `python3 -m py_compile main.py tests/test_main.py`,
  `python3 -m unittest discover -s tests -p 'test_main.py' -v`,
  `python3 -m unittest discover -s tests -v`, `git diff --check`
- 테스트 결과: 메인 테스트 21개, 전체 46개 통과
- 발생한 문제: 없음
- 해결 방법: 해당 없음
- 커밋: `895011f` 메뉴 복귀 기능, `04eb721` 메뉴 복귀 테스트,
  `3832cd5` 개발 로그
- PR: #9 - https://github.com/juny030507/option-strategy-quiz/pull/9
- 병합 결과: merge commit `4cd784a`
- 남은 작업: 3-2~5단계

### 단계 기록

- 날짜: 2026-08-05
- 단계: 3-2단계 - 최종 입력 검증과 코드 품질 점검
- 작업 주체: 사용자 직접 수행
- 브랜치: `refactor/final-quality`
- 목표: 검증된 동작을 유지하면서 모델·입력·게임 방어 경로와
  금융 용어, PEP 8 일관성을 최종 점검
- 수정 파일: `quiz.py`, `quiz_game.py`, `default_quizzes.py`,
  `tests/test_quiz.py`, `tests/test_quiz_game.py`, `tests/test_main.py`,
  `tests/test_default_quizzes.py`, `state.json`, `docs/development-log.md`
- 설계 결정: `Quiz`가 빈 문제·선택지와 bool을 포함한 잘못된
  정답을 거부하고, `QuizGame`도 bool 답안을 점수에 반영하지 않도록
  함. `state.json`은 수정된 기본 퀴즈와 공개 저장 함수로 재생성
- 주요 명령: `pycodestyle --max-line-length=88 *.py tests/*.py`,
  `ruff check .`, `python3 -m unittest discover -s tests -v`,
  `python3 -m json.tool state.json`, `git diff --check`
- 테스트 결과: 기존 46개에 12개를 추가해 전체 58개 통과.
  테스트 전후 `state.json` SHA-256가
  `07ce4f9fcaa468ac21226fb3de07c1dd3d0872805006ad9fdd49f1e19e8a8a0f`로
  같아 실제 상태 파일을 변경하지 않음
- 발생한 문제: 없음
- 해결 방법: 해당 없음
- 커밋: `8713c95` 모델·용어 정리, `007a00e` 방어 경로 테스트,
  `bdb4f42` 최신 기본 상태, `b31924d` 개발 로그
- PR: #10 - https://github.com/juny030507/option-strategy-quiz/pull/10
- 병합 결과: merge commit `18457dc`
- 남은 작업: 4~5단계

### 단계 기록

- 날짜: 2026-08-05
- 단계: 4-1단계 - GitHub Actions Python 3.10 자동 테스트
- 작업 주체: 사용자 직접 수행
- 브랜치: `ci/github-actions`
- 목표: `main` push와 pull request에서 표준 라이브러리 테스트를
  Python 3.10으로 자동 실행
- 수정 파일: `.github/workflows/tests.yml`,
  `docs/development-log.md`
- 설계 결정: 워크플로에 `actions/checkout@v6`,
  `actions/setup-python@v5`를 사용. 외부 의존성이
  없어 설치 단계를 두지 않고 `contents: read`만 부여
- 주요 명령: `ruby -e` YAML 구문 검사,
  `python3 -m unittest discover -s tests -v`, `git diff --check`
- 테스트 결과: YAML 구문 통과, 로컬 전체 58개 통과
- 발생한 문제: 로컬에 `actionlint`가 설치되어 있지 않음
- 해결 방법: 추가 의존성을 도입하지 않고 Ruby 표준 YAML 파서로
  구문을 확인하고 PR의 GitHub Actions 실행으로 최종 검증
- 커밋: `dfdf0b9` Python 3.10 자동 테스트 워크플로,
  `9d304fb` GitHub Actions 구성 기록
- PR: #11 - https://github.com/juny030507/option-strategy-quiz/pull/11
- 병합 결과: merge commit `43fe142`
- 남은 작업: 4-2~5단계

### 단계 기록

- 날짜: 2026-08-05
- 단계: 4-2단계 - `main` 브랜치 보호
- 작업 주체: 사용자 직접 수행
- 브랜치: `main`(코드 변경 없음, GitHub 저장소 설정)
- 목표: 성공한 실제 CI 검사를 `main` 병합 규칙으로 적용
- 수정 파일: 없음
- 설계 결정: 기존 branch protection과 ruleset이 없음을 먼저 확인.
  PR 필수·승인 0명, 성공한 검사·최신 `main` 기준 필수,
  대화 해결 필수, 강제 push·삭제 금지만 적용하고 관리자 강제 적용은
  현재 개인 과제 작업을 막을 위험으로 비활성화
- 주요 명령: `gh run list`, `gh run view`, branch protection·ruleset
  조회와 `gh api --method PUT`
- 테스트 결과: `main` Actions 58개 통과, 적용 후 API 재조회로
  필수 검사·strict·PR·대화 해결·강제 push·삭제 값 확인
- 발생한 문제: 없음
- 해결 방법: 해당 없음
- 커밋: 없음
- PR: 해당 없음
- 병합 결과: 해당 없음
- 남은 작업: 5단계

### 단계 기록

- 날짜: 2026-08-05
- 단계: 5단계 - README, 제출 증거, 최종 검증
- 작업 주체: 사용자 직접 수행
- 브랜치: `docs/final-readme`
- 목표: 사용법·구조·개발 이력을 README로 완성하고 텍스트 증거와
  수동 캡처 체크리스트를 준비한 뒤 원격 브랜치를 깨끗한 환경에서 검증
- 수정 파일: `README.md`, `docs/development-log.md`, `docs/evidence/`
- 설계 결정: README에는 성공한 Actions 배지만 표시하고 실제 UI
  스크린샷은 생성한 것처럼 기록하지 않으며 사용자 캡처 항목으로 분리
- 주요 명령: `git clone --branch docs/final-readme --single-branch`,
  `python3 -m unittest discover -s tests -v`, `python3 main.py`,
  `python3 -m json.tool state.json`, `git diff --check`, `git status --short --branch`
- 테스트 결과: 새 clone의 Python 3.10.4에서 58개 통과, 5번 정상
  종료, JSON·README 링크·외부 경로·깨끗한 Git 상태 검증 통과.
  [PR #12 Actions 실행 30996368348](https://github.com/juny030507/option-strategy-quiz/actions/runs/30996368348)도 58개 통과
- 발생한 문제: 기존 README의 실행 코드 블록이 닫히지 않았고
  실행 외 사용법·저장·테스트·개발 정보가 누락됨
- 해결 방법: 코드 블록을 닫고 과제 요구 항목을 실제 코드·Git·CI
  상태와 대조해 README를 재작성
- 커밋: `ec56c8c` README 사용법과 구조, 최종 문서·증거 정리 커밋
- PR: [#12 Docs: README와 최종 제출 자료 완성](https://github.com/juny030507/option-strategy-quiz/pull/12) (Draft)
- 병합 결과: 필수 검사 `Python 3.10 unit tests` 성공, Ready 전환·병합 전
- 남은 작업: PR #12 Ready 전환·병합과 최신 `main` 최종 검증
