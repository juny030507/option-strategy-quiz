"""메인 프로그램의 퀴즈 풀이와 점수 출력을 검증한다."""

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from main import (
    add_new_quiz,
    main,
    play_quizzes,
    read_number,
    read_text,
    show_quiz_list,
    show_score,
)
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

        with patch("main.load_state", return_value=self.game):
            with patch("main.save_state"):
                with patch("main.read_number", side_effect=[4, 5]):
                    with patch("main.show_score") as mock_show_score:
                        with redirect_stdout(output):
                            main()

        mock_show_score.assert_called_once()

    def test_read_text_retries_after_empty_input(self) -> None:
        """빈 문자열 다음에 정상 문자열을 다시 입력받아야 한다."""
        output = io.StringIO()

        with patch(
            "builtins.input",
            side_effect=["", "정상 입력"],
        ):
            with redirect_stdout(output):
                result = read_text("입력: ")

        self.assertEqual(result, "정상 입력")
        self.assertIn("빈 입력은 사용할 수 없습니다.", output.getvalue())

    def test_read_number_retries_after_empty_input(self) -> None:
        """빈 입력 다음에 범위 내 정수를 다시 입력받는다."""
        output = io.StringIO()

        with patch("builtins.input", side_effect=["", "2"]):
            with redirect_stdout(output):
                result = read_number("입력: ", 1, 5)

        self.assertEqual(result, 2)
        self.assertIn("빈 입력은 사용할 수 없습니다.", output.getvalue())

    def test_read_number_retries_after_non_numeric_input(self) -> None:
        """숫자가 아닌 입력 다음에 정상 정수를 다시 입력받는다."""
        output = io.StringIO()

        with patch("builtins.input", side_effect=["abc", "2"]):
            with redirect_stdout(output):
                result = read_number("입력: ", 1, 5)

        self.assertEqual(result, 2)
        self.assertIn("숫자만 입력할 수 있습니다.", output.getvalue())

    def test_read_number_retries_after_out_of_range_input(self) -> None:
        """범위 밖 입력 다음에 정상 정수를 다시 입력받는다."""
        output = io.StringIO()

        with patch("builtins.input", side_effect=["9", "4"]):
            with redirect_stdout(output):
                result = read_number("입력: ", 1, 5)

        self.assertEqual(result, 4)
        self.assertIn("1~5 사이의 숫자", output.getvalue())

    def test_read_number_returns_none_on_eof(self) -> None:
        """EOF로 입력이 종료되면 None과 중단 안내를 반환한다."""
        output = io.StringIO()

        with patch("builtins.input", side_effect=EOFError):
            with redirect_stdout(output):
                result = read_number("입력: ", 1, 5)

        self.assertIsNone(result)
        self.assertIn("입력이 중단되었습니다.", output.getvalue())

    def test_add_new_quiz_from_input(self) -> None:
        """입력받은 문제를 게임의 퀴즈 목록에 추가해야 한다."""
        output = io.StringIO()
        inputs = [
            "스트래들 매수 전략의 구성은?",
            "콜옵션 매수 + 풋옵션 매수",
            "콜옵션 매도 + 풋옵션 매도",
            "기초자산 매수 + 콜옵션 매도",
            "기초자산 매수 + 풋옵션 매수",
            "1",
        ]

        with patch("builtins.input", side_effect=inputs):
            with redirect_stdout(output):
                add_new_quiz(self.game)

        added_quiz = self.game.quizzes[-1]

        self.assertEqual(len(self.game.quizzes), 2)
        self.assertEqual(
            added_quiz.question,
            "스트래들 매수 전략의 구성은?",
        )
        self.assertEqual(added_quiz.answer, 1)
        self.assertIn("현재 총 2개", output.getvalue())

    def test_add_new_quiz_cancels_on_interrupted_input(self) -> None:
        """입력이 중단되면 새로운 퀴즈를 추가하지 않아야 한다."""
        output = io.StringIO()

        with patch("builtins.input", side_effect=EOFError):
            with redirect_stdout(output):
                add_new_quiz(self.game)

        self.assertEqual(len(self.game.quizzes), 1)
        self.assertIn("퀴즈 추가를 취소", output.getvalue())

    def test_show_quiz_list_displays_registered_quiz(self) -> None:
        """퀴즈 목록에 등록된 문제와 선택지를 출력해야 한다."""
        output = io.StringIO()

        with redirect_stdout(output):
            show_quiz_list(self.game)

        result = output.getvalue()
        self.assertIn("퀴즈 목록: 총 1개", result)
        self.assertIn("보호적 풋의 구성은?", result)
        self.assertIn(
            "기초자산 보유 + 풋옵션 매수",
            result,
        )

    def test_show_quiz_list_handles_empty_game(self) -> None:
        """등록된 퀴즈가 없으면 안내 문구를 출력해야 한다."""
        empty_game = QuizGame()
        output = io.StringIO()

        with redirect_stdout(output):
            show_quiz_list(empty_game)

        self.assertIn("등록된 퀴즈가 없습니다.", output.getvalue())

    def test_add_menu_calls_add_new_quiz(self) -> None:
        """2번 메뉴를 선택하면 퀴즈 추가 함수를 호출해야 한다."""
        output = io.StringIO()

        with patch("main.load_state", return_value=self.game):
            with patch("main.save_state"):
                with patch("main.read_number", side_effect=[2, 5]):
                    with patch("main.add_new_quiz") as mock_add_new_quiz:
                        with redirect_stdout(output):
                            main()

        mock_add_new_quiz.assert_called_once()

    def test_list_menu_calls_show_quiz_list(self) -> None:
        """3번 메뉴를 선택하면 퀴즈 목록 함수를 호출해야 한다."""
        output = io.StringIO()

        with patch("main.load_state", return_value=self.game):
            with patch("main.save_state"):
                with patch("main.read_number", side_effect=[3, 5]):
                    with patch("main.show_quiz_list") as mock_show_quiz_list:
                        with redirect_stdout(output):
                            main()

        mock_show_quiz_list.assert_called_once()

    def test_main_loads_state_and_saves_on_normal_exit(self) -> None:
        """시작 시 상태를 불러오고 정상 종료 시 저장해야 한다."""
        output = io.StringIO()

        with patch(
            "main.load_state",
            return_value=self.game,
        ) as mock_load_state:
            with patch("main.save_state") as mock_save_state:
                with patch("main.read_number", return_value=5):
                    with redirect_stdout(output):
                        main()

        mock_load_state.assert_called_once_with()
        mock_save_state.assert_called_once_with(self.game)

    def test_main_saves_after_playing_quizzes(self) -> None:
        """퀴즈 풀이 후와 정상 종료 시 각각 상태를 저장해야 한다."""
        output = io.StringIO()

        with patch("main.load_state", return_value=self.game):
            with patch("main.save_state") as mock_save_state:
                with patch("main.read_number", side_effect=[1, 5]):
                    with patch("main.play_quizzes") as mock_play_quizzes:
                        with redirect_stdout(output):
                            main()

        mock_play_quizzes.assert_called_once_with(self.game)
        self.assertEqual(mock_save_state.call_count, 2)
        for save_call in mock_save_state.call_args_list:
            self.assertIs(save_call.args[0], self.game)

    def test_main_saves_after_adding_quiz(self) -> None:
        """퀴즈 추가 후와 정상 종료 시 각각 상태를 저장해야 한다."""
        output = io.StringIO()

        with patch("main.load_state", return_value=self.game):
            with patch("main.save_state") as mock_save_state:
                with patch("main.read_number", side_effect=[2, 5]):
                    with patch("main.add_new_quiz") as mock_add_new_quiz:
                        with redirect_stdout(output):
                            main()

        mock_add_new_quiz.assert_called_once_with(self.game)
        self.assertEqual(mock_save_state.call_count, 2)
        for save_call in mock_save_state.call_args_list:
            self.assertIs(save_call.args[0], self.game)

    def test_main_saves_on_interrupted_menu_input(self) -> None:
        """메뉴 입력 중단 시 상태를 저장하고 안전하게 종료해야 한다."""
        output = io.StringIO()

        with patch("main.load_state", return_value=self.game):
            with patch("main.save_state") as mock_save_state:
                with patch("main.read_number", return_value=None):
                    with redirect_stdout(output):
                        main()

        mock_save_state.assert_called_once_with(self.game)
        self.assertIn(
            "퀴즈 게임을 안전하게 종료합니다.",
            output.getvalue(),
        )

    def test_play_quizzes_returns_to_menu_on_zero(self) -> None:
        """퀴즈 풀이에서 0을 입력하면 점수 변화 없이 돌아가야 한다."""
        output = io.StringIO()
        quiz_count = len(self.game.quizzes)

        with patch("builtins.input", return_value="0"):
            with redirect_stdout(output):
                play_quizzes(self.game)

        self.assertEqual(len(self.game.quizzes), quiz_count)
        self.assertEqual(self.game.attempt_count, 0)
        self.assertIn("메인 메뉴로 돌아갑니다.", output.getvalue())

    def test_add_new_quiz_returns_to_menu_on_zero_question(self) -> None:
        """문제 입력에서 0을 입력하면 퀴즈 추가를 취소해야 한다."""
        output = io.StringIO()
        quiz_count = len(self.game.quizzes)

        with patch("builtins.input", return_value="0"):
            with redirect_stdout(output):
                add_new_quiz(self.game)

        self.assertEqual(len(self.game.quizzes), quiz_count)
        self.assertEqual(self.game.attempt_count, 0)
        self.assertIn("메뉴로 돌아갑니다.", output.getvalue())

    def test_add_new_quiz_returns_to_menu_on_zero_choice(self) -> None:
        """선택지 입력에서 0을 입력하면 퀴즈 추가를 취소해야 한다."""
        output = io.StringIO()
        quiz_count = len(self.game.quizzes)

        with patch(
            "builtins.input",
            side_effect=["새 문제", "0"],
        ):
            with redirect_stdout(output):
                add_new_quiz(self.game)

        self.assertEqual(len(self.game.quizzes), quiz_count)
        self.assertEqual(self.game.attempt_count, 0)
        self.assertIn("메뉴로 돌아갑니다.", output.getvalue())

    def test_add_new_quiz_returns_to_menu_on_zero_answer(self) -> None:
        """정답 입력에서 0을 입력하면 퀴즈 추가를 취소해야 한다."""
        output = io.StringIO()
        quiz_count = len(self.game.quizzes)
        inputs = [
            "새 문제",
            "선택지1",
            "선택지2",
            "선택지3",
            "선택지4",
            "0",
        ]

        with patch("builtins.input", side_effect=inputs):
            with redirect_stdout(output):
                add_new_quiz(self.game)

        self.assertEqual(len(self.game.quizzes), quiz_count)
        self.assertEqual(self.game.attempt_count, 0)
        self.assertIn("메뉴로 돌아갑니다.", output.getvalue())


if __name__ == "__main__":
    unittest.main()
