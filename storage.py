"""퀴즈 게임 상태의 JSON 변환과 파일 입출력을 담당한다."""

import json
from pathlib import Path

from default_quizzes import create_default_quizzes
from quiz import Quiz
from quiz_game import QuizGame


STATE_FILE = Path(__file__).resolve().parent / "state.json"


def create_default_game() -> QuizGame:
    """기본 퀴즈와 0점 상태를 가진 게임을 생성한다."""
    return QuizGame(create_default_quizzes())


def game_to_dict(game: QuizGame) -> dict[str, object]:
    """게임의 퀴즈 목록과 누적 점수를 JSON용 사전으로 변환한다."""
    quizzes = [
        {
            "question": quiz.question,
            "choices": quiz.choices.copy(),
            "answer": quiz.answer,
        }
        for quiz in game.quizzes
    ]

    return {
        "quizzes": quizzes,
        "score": {
            "correct_count": game.correct_count,
            "attempt_count": game.attempt_count,
        },
    }


def quiz_from_dict(data: object) -> Quiz:
    """JSON 퀴즈 항목을 검증하고 Quiz 객체로 변환한다."""
    if not isinstance(data, dict):
        raise ValueError("퀴즈 데이터는 사전이어야 합니다.")

    question = data.get("question")
    choices = data.get("choices")
    answer = data.get("answer")

    if not isinstance(question, str) or not question.strip():
        raise ValueError("문제는 비어 있지 않은 문자열이어야 합니다.")

    if (
        not isinstance(choices, list)
        or len(choices) != 4
        or not all(
            isinstance(choice, str) and choice.strip()
            for choice in choices
        )
    ):
        raise ValueError(
            "선택지는 비어 있지 않은 문자열 정확히 4개여야 합니다."
        )

    if type(answer) is not int or not 1 <= answer <= 4:
        raise ValueError("정답은 1~4 사이의 정수여야 합니다.")

    return Quiz(question, choices, answer)


def save_state(game: QuizGame, path: str | Path = STATE_FILE) -> bool:
    """게임 상태를 UTF-8 JSON 파일로 저장한다."""
    try:
        with Path(path).open("w", encoding="utf-8") as state_file:
            json.dump(
                game_to_dict(game),
                state_file,
                ensure_ascii=False,
                indent=2,
            )
            state_file.write("\n")
    except OSError as error:
        print(f"상태를 저장하지 못했습니다: {error}")
        return False

    return True


def load_state(path: str | Path = STATE_FILE) -> QuizGame:
    """JSON 파일에서 게임 상태를 불러오고 오류 시 기본값을 복구한다."""
    try:
        with Path(path).open("r", encoding="utf-8") as state_file:
            data = json.load(state_file)

        if not isinstance(data, dict):
            raise ValueError("JSON 최상위 데이터는 사전이어야 합니다.")

        quizzes_data = data.get("quizzes")
        if not isinstance(quizzes_data, list) or not quizzes_data:
            raise ValueError("퀴즈 목록은 비어 있지 않은 리스트여야 합니다.")

        quizzes = [quiz_from_dict(quiz_data) for quiz_data in quizzes_data]

        score = data.get("score")
        if not isinstance(score, dict):
            raise ValueError("점수 데이터는 사전이어야 합니다.")

        correct_count = score.get("correct_count")
        attempt_count = score.get("attempt_count")

        if (
            type(correct_count) is not int
            or type(attempt_count) is not int
            or correct_count < 0
            or attempt_count < 0
        ):
            raise ValueError("점수는 0 이상의 정수여야 합니다.")

        if correct_count > attempt_count:
            raise ValueError("정답 수는 풀이 수보다 클 수 없습니다.")

        game = QuizGame(quizzes)
        game.correct_count = correct_count
        game.attempt_count = attempt_count
        return game
    except FileNotFoundError:
        print("저장 파일이 없어 기본 퀴즈를 사용합니다.")
        return create_default_game()
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as error:
        print(f"저장 파일이 손상되어 기본 퀴즈로 복구합니다: {error}")
        return create_default_game()
