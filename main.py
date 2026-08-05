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
    """현재까지 누적된 점수와 정답률을 출력한다."""
    print("\n" + "=" * 40)
    print("현재 점수")
    print("=" * 40)
    print(f"푼 문제: {game.attempt_count}개")
    print(f"맞힌 문제: {game.correct_count}개")
    print(f"정답률: {game.calculate_accuracy():.1f}%")
    print("=" * 40)


def play_quizzes(game: QuizGame) -> None:
    """등록된 퀴즈를 차례대로 풀고 채점한다."""
    if not game.quizzes:
        print("\n등록된 퀴즈가 없습니다.")
        return

    quiz_count = len(game.quizzes)
    print(f"\n총 {quiz_count}개의 퀴즈를 시작합니다.")

    for quiz_number, quiz in enumerate(game.quizzes, start=1):
        print(f"\n[{quiz_number}/{quiz_count}]")
        quiz.display()

        selected_answer = read_number(
            "정답 선택 (0: 메뉴, 1~4): ",
            0,
            4,
        )

        if selected_answer is None:
            print("퀴즈 풀이를 중단하고 메뉴로 돌아갑니다.")
            return

        if selected_answer == 0:
            print("메인 메뉴로 돌아갑니다.")
            return

        if game.submit_answer(quiz, selected_answer):
            print("정답입니다!")
        else:
            correct_choice = quiz.choices[quiz.answer - 1]
            print(
                f"오답입니다. 정답은 {quiz.answer}번, "
                f"{correct_choice}입니다."
            )

    print("\n모든 퀴즈를 풀었습니다.")
    show_score(game)


def main() -> None:
    """사용자가 종료를 선택할 때까지 메뉴를 반복한다."""
    game = load_state()

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
