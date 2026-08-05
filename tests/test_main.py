"""메인 프로그램의 퀴즈 풀이와 점수 출력을 겸증한다."""

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from main import main, play_quizzes, show_score
from quiz import Quiz
from quiz_game import QuizGame

class TestMainQuizFlow(unittest.TestCase):
    """퀴즈 풀이와 점수 출력 흐름을 테스트한다."""

    def setUp(self) -> None:
        """각 테스트에서 사용할 퀴즈 게임을 준비한다."""
        self.quiz = Quiz(
            "보호적 풋의 구성은?",
            [
                "기초자산 보유 + 풋옵션 매수",
                "기초자산 보유 + 콜옵션 매도",
                "콜옵션 매수 + 풋옵션 매수",
                "콜옵션 매도 + 풋옵션 매도",
            ],
            1,
        )
        self.game = QuizGame([self.quiz])

    def test_play_quizzes_displays_correct_result(self) -> None:
        """정답을 입력하면 정답 안내를 출력해야 한다."""
        output = io.StringIO()

        with patch("builtins.input", return_value="1"):
            with redirect_stdout(output):
                play_quizzes(self.game)

        result = output.getvalue()
        self.assertIn("정답입니다!", result)
        self.assertIn("푼 문제: 1개", result)

    def test_play_quizzes_displays_correct_choice_for_wrong_answer(
        self,
    ) -> None:
        """오답을 입력하면 올바른 정답을 안내해야 한다."""
        output = io.StringIO()

        with patch("builtins.input", return_value="2"):
            with redirect_stdout(output):
                play_quizzes(self.game)

        result = output.getvalue()
        self.assertIn("오답입니다.", result)
        self.assertIn("정답은 1번", result)

    def test_empty_game_displays_message(self) -> None:
        """등록된 문제가 없으면 안내 문구를 출력해야 한다."""
        empty_game = QuizGame()
        output = io.StringIO()

        with redirect_stdout(output):
            play_quizzes(empty_game)

        self.assertIn("등록된 퀴즈가 없습니다.", output.getvalue())

    def test_show_score_displays_current_result(self) -> None:
        """현재 점수와 정답률을 출력해야 한다."""
        self.game.submit_answer(self.quiz, 1)
        output = io.StringIO()

        with redirect_stdout(output):
            show_score(self.game)

        result = output.getvalue()
        self.assertIn("푼 문제: 1개", result)
        self.assertIn("맞힌 문제: 1개", result)
        self.assertIn("정답률: 100.0%", result)

    def test_interrupted_input_returns_without_scoring(self) -> None:
        """입력이 중단되면 점수를 변경하지 않고 돌아가야 한다."""
        output = io.StringIO()

        with patch("builtins.input", side_effect=EOFError):
            with redirect_stdout(output):
                play_quizzes(self.game)

            self.assertEqual(self.game.attempt_count, 0)
            self.assertIn("퀴즈 풀이를 중단", output.getvalue())

    def test_score_menu_calls_show_score(self) -> None:
        """4번 메뉴를 선택하면 점수 출력 함수를 호출해야 한다."""
        output = io.StringIO()

        with patch("main.read_number", side_effect=[4, 5]):
            with patch("main.show_score") as mock_show_score:
                with redirect_stdout(output):
                    main()

        mock_show_score.assert_called_once()

if __name__ == "__main__":
    unittest.main()
