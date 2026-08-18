"""옵션 투자기법 퀴즈 게임의 실행 파일."""

from quiz import Quiz
from quiz_game import QuizGame
from storage import load_state, save_state


def show_menu() -> None:
    """사용자가 선택할 수 있는 메뉴를 출력한다."""
    print("\n" + "=" * 40)
    print("옵션 투자기법 퀴즈 게임")
    print("=" * 40)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("퀴즈 풀이·추가 중 0을 입력하면 메뉴로 돌아갑니다.")
    print("=" * 40)


def read_number(
    prompt: str,
    minimum: int,
    maximum: int
) -> int | None:
    """지정된 범위의 정수를 입력받는다."""
    while True:
        try:
            raw_value = input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            print("\n입력이 중단되었습니다.")
            return None
        if not raw_value:
            print("빈 입력은 사용할 수 없습니다.")
            continue
        try:
            number = int(raw_value)
        except ValueError:
            print("숫자만 입력할 수 있습니다.")
            continue
        if minimum <= number <= maximum:
            return number
        print(f"{minimum}~{maximum} 사이의 숫자를 입력해주세요.")


def read_text(prompt: str) -> str | None:
    """비어 있지 않은 문자열을 입력받는다."""
    while True:
        try:
            value = input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            print("\n입력이 중단되었습니다.")
            return None

        if value:
            return value

        print("빈 입력은 사용할 수 없습니다.")


def add_new_quiz(game: QuizGame) -> None:
    """사용자에게 문제 정보를 입력받아 퀴즈를 추가한다."""
    print("\n" + "=" * 40)
    print("새 퀴즈 추가")
    print("=" * 40)

    question = read_text("문제 (0: 메뉴): ")

    if question is None or question == "0":
        print("퀴즈 추가를 취소하고 메뉴로 돌아갑니다.")
        return

    choices: list[str] = []

    for number in range(1, 5):
        choice = read_text(f"선택지 {number} (0: 메뉴): ")

        if choice is None or choice == "0":
            print("퀴즈 추가를 취소하고 메뉴로 돌아갑니다.")
            return

        choices.append(choice)

    answer = read_number("정답 번호 (0: 메뉴, 1~4): ", 0, 4)

    if answer is None or answer == 0:
        print("퀴즈 추가를 취소하고 메뉴로 돌아갑니다.")
        return

    quiz = Quiz(question, choices, answer)
    game.add_quiz(quiz)

    print(f"퀴즈가 추가되었습니다. 현재 총 {len(game.quizzes)}개입니다.")


def show_quiz_list(game: QuizGame) -> None:
    """등록된 퀴즈의 문제와 선택지를 출력한다."""
    if not game.quizzes:
        print("\n등록된 퀴즈가 없습니다.")
        return

    print("\n" + "=" * 40)
    print(f"퀴즈 목록: 총 {len(game.quizzes)}개")
    print("=" * 40)

    for quiz_number, quiz in enumerate(game.quizzes, start=1):
        print(f"\n{quiz_number}. {quiz.question}")

        for choice_number, choice in enumerate(quiz.choices, start=1):
            print(f"   {choice_number}) {choice}")


def show_score(game: QuizGame) -> None:
    """최고 점수와 현재까지 누적된 풀이 통계를 출력한다."""
    print("\n" + "=" * 40)
    print("점수 확인")
    print("=" * 40)

    if game.best_total == 0:
        print("아직 완료한 퀴즈가 없어 최고 점수가 없습니다.")
    else:
        print(
            f"완료 회차 최고 점수: {game.best_score}개 정답 "
            f"(총 {game.best_total}문제)"
        )

    print("-" * 40)
    print("진행 중 회차")
    if game.has_active_session():
        print(
            f"진행 상황: {game.session_answered_count}/"
            f"{game.session_total}문제 완료"
        )
        print(f"현재 회차 점수: {game.session_correct_count}개 정답")
        print(f"다음 문제: {game.session_answered_count + 1}번")
    else:
        print("진행 중인 회차가 없습니다.")

    print("-" * 40)
    print("누적 풀이 통계")
    print(f"푼 문제: {game.attempt_count}개")
    print(f"맞힌 문제: {game.correct_count}개")
    print(f"정답률: {game.calculate_accuracy():.1f}%")
    print("=" * 40)


def play_quizzes(game: QuizGame) -> None:
    """등록된 퀴즈를 차례대로 풀고 채점한다."""
    if not game.quizzes:
        print("\n등록된 퀴즈가 없습니다.")
        return

    if game.has_active_session():
        print("\n저장된 퀴즈 회차를 이어서 진행합니다.")
        print(
            f"현재 {game.session_answered_count}/"
            f"{game.session_total}문제 완료, "
            f"{game.session_correct_count}문제 정답"
        )
    else:
        game.start_session()
        print(f"\n총 {game.session_total}개의 퀴즈를 시작합니다.")

    while game.session_answered_count < game.session_total:
        quiz_number = game.session_answered_count + 1
        quiz = game.quizzes[game.session_answered_count]
        print(f"\n[{quiz_number}/{game.session_total}]")
        quiz.display()

        selected_answer = read_number(
            "정답 선택 (0: 메뉴, 1~4): ",
            0,
            4,
        )

        if selected_answer is None:
            print(
                "퀴즈 풀이를 중단합니다. "
                f"{game.session_answered_count}/"
                f"{game.session_total}문제까지의 상태를 저장합니다."
            )
            return

        if selected_answer == 0:
            print(
                "메인 메뉴로 돌아갑니다. "
                f"{game.session_answered_count}/"
                f"{game.session_total}문제까지의 상태를 저장합니다."
            )
            return

        if game.submit_session_answer(quiz, selected_answer):
            print("정답입니다!")
        else:
            correct_choice = quiz.choices[quiz.answer - 1]
            print(
                f"오답입니다. 정답은 {quiz.answer}번, "
                f"{correct_choice}입니다."
            )

    session_score = game.session_correct_count
    session_total = game.session_total
    is_new_best = game.finish_session()

    print("\n모든 퀴즈를 풀었습니다.")
    print(f"이번 결과: {session_total}문제 중 {session_score}문제 정답")

    if is_new_best:
        print("새로운 최고 점수입니다!")

    show_score(game)


def main() -> None:
    """사용자가 종료를 선택할 때까지 메뉴를 반복한다."""
    game = load_state()

    if game.has_active_session():
        print(
            "저장된 진행 기록이 있습니다: "
            f"{game.session_answered_count}/"
            f"{game.session_total}문제 완료, "
            f"현재 {game.session_correct_count}문제 정답"
        )

    while True:
        show_menu()
        choice = read_number("메뉴 선택: ", 1, 5)
        if choice is None:
            save_state(game)
            print("퀴즈 게임을 안전하게 종료합니다.")
            break

        if choice == 1:
            play_quizzes(game)
            save_state(game)
        elif choice == 2:
            add_new_quiz(game)
            save_state(game)
        elif choice == 3:
            show_quiz_list(game)
        elif choice == 4:
            show_score(game)
        elif choice == 5:
            save_state(game)
            print("퀴즈 게임을 종료합니다.")
            break


if __name__ == "__main__":
    main()
