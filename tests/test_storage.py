"""퀴즈 게임 상태의 변환과 JSON 파일 입출력을 검증한다."""

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import storage
from quiz import Quiz
from quiz_game import QuizGame
from storage import (
    STATE_FILE,
    game_to_dict,
    load_state,
    quiz_from_dict,
    save_state,
)


class TestStorage(unittest.TestCase):
    """게임 상태의 직렬화, 저장, 불러오기, 복구를 테스트한다."""

    def setUp(self) -> None:
        """각 테스트에서 사용할 임시 상태 파일 경로를 준비한다."""
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.state_path = Path(self.temporary_directory.name) / "state.json"

    def tearDown(self) -> None:
        """테스트에서 사용한 임시 디렉터리를 정리한다."""
        self.temporary_directory.cleanup()

    def test_state_file_points_to_project_root(self) -> None:
        """STATE_FILE이 프로젝트 루트의 state.json을 가리켜야 한다."""
        project_root = Path(storage.__file__).resolve().parent

        self.assertEqual(STATE_FILE.name, "state.json")
        self.assertEqual(STATE_FILE.parent, project_root)

    def test_missing_file_returns_default_game(self) -> None:
        """저장 파일이 없으면 안내 후 기본 게임을 반환해야 한다."""
        output = io.StringIO()

        with redirect_stdout(output):
            game = load_state(self.state_path)

        self.assertIsInstance(game, QuizGame)
        self.assertGreaterEqual(len(game.quizzes), 10)
        self.assertEqual(game.correct_count, 0)
        self.assertEqual(game.attempt_count, 0)
        self.assertIn("저장 파일이 없어", output.getvalue())

    def test_game_to_dict_contains_quizzes_and_score(self) -> None:
        """게임의 퀴즈와 점수를 복사한 JSON용 사전으로 변환해야 한다."""
        quiz = Quiz(
            "보호적 풋의 구성은?",
            ["기초자산 보유", "풋옵션 매수", "콜옵션 매수", "현금 보유"],
            2,
        )
        game = QuizGame([quiz])
        game.correct_count = 2
        game.attempt_count = 3

        data = game_to_dict(game)

        self.assertIn("quizzes", data)
        self.assertIn("score", data)
        self.assertEqual(data["quizzes"][0]["question"], quiz.question)
        self.assertEqual(data["quizzes"][0]["choices"], quiz.choices)
        self.assertEqual(data["quizzes"][0]["answer"], quiz.answer)
        self.assertEqual(
            data["score"],
            {"correct_count": 2, "attempt_count": 3},
        )

        data["quizzes"][0]["choices"][0] = "변경된 선택지"
        self.assertEqual(quiz.choices[0], "기초자산 보유")

    def test_quiz_from_dict_rejects_invalid_data(self) -> None:
        """잘못된 문제, 선택지, 정답 데이터를 거부해야 한다."""
        valid_choices = ["선택지1", "선택지2", "선택지3", "선택지4"]
        invalid_cases = {
            "not_a_dict": ["invalid"],
            "empty_question": {
                "question": " ",
                "choices": valid_choices,
                "answer": 1,
            },
            "choices_not_a_list": {
                "question": "문제",
                "choices": tuple(valid_choices),
                "answer": 1,
            },
            "wrong_choice_count": {
                "question": "문제",
                "choices": valid_choices[:3],
                "answer": 1,
            },
            "empty_choice": {
                "question": "문제",
                "choices": ["선택지1", "", "선택지3", "선택지4"],
                "answer": 1,
            },
            "string_answer": {
                "question": "문제",
                "choices": valid_choices,
                "answer": "1",
            },
            "boolean_answer": {
                "question": "문제",
                "choices": valid_choices,
                "answer": True,
            },
            "answer_zero": {
                "question": "문제",
                "choices": valid_choices,
                "answer": 0,
            },
            "answer_five": {
                "question": "문제",
                "choices": valid_choices,
                "answer": 5,
            },
        }

        for case_name, invalid_data in invalid_cases.items():
            with self.subTest(case=case_name):
                with self.assertRaises(ValueError):
                    quiz_from_dict(invalid_data)

    def test_save_state_writes_utf8_pretty_json_and_newline(self) -> None:
        """한글을 보존한 읽기 쉬운 JSON과 마지막 줄바꿈을 저장해야 한다."""
        quiz = Quiz(
            "한글 문제입니다.",
            ["강세장", "약세장", "횡보장", "알 수 없음"],
            1,
        )
        game = QuizGame([quiz])

        result = save_state(game, self.state_path)
        content = self.state_path.read_text(encoding="utf-8")

        self.assertTrue(result)
        self.assertIn("한글 문제입니다.", content)
        self.assertNotIn("\\ud55c", content.lower())
        self.assertIn('\n  "quizzes": [', content)
        self.assertTrue(content.endswith("\n"))
        self.assertEqual(
            json.loads(content)["quizzes"][0]["question"],
            "한글 문제입니다.",
        )

    def test_save_and_load_round_trip(self) -> None:
        """저장한 퀴즈와 점수를 동일하게 복원해야 한다."""
        quiz = Quiz(
            "스트래들 매수의 구성은?",
            ["콜 매수 + 풋 매수", "콜 매도", "풋 매도", "현금"],
            1,
        )
        game = QuizGame([quiz])
        game.correct_count = 2
        game.attempt_count = 4

        self.assertTrue(save_state(game, self.state_path))
        loaded_game = load_state(self.state_path)

        self.assertEqual(loaded_game.quizzes[0].question, quiz.question)
        self.assertEqual(loaded_game.quizzes[0].choices, quiz.choices)
        self.assertEqual(loaded_game.quizzes[0].answer, quiz.answer)
        self.assertEqual(loaded_game.correct_count, 2)
        self.assertEqual(loaded_game.attempt_count, 4)

    def test_corrupted_json_returns_default_game(self) -> None:
        """문법이 깨진 JSON이면 안내 후 기본 게임으로 복구해야 한다."""
        self.state_path.write_text('{"quizzes": [', encoding="utf-8")
        output = io.StringIO()

        with redirect_stdout(output):
            game = load_state(self.state_path)

        self.assertIsInstance(game, QuizGame)
        self.assertGreaterEqual(len(game.quizzes), 10)
        self.assertEqual(game.correct_count, 0)
        self.assertEqual(game.attempt_count, 0)
        self.assertIn("손상", output.getvalue())

    def test_invalid_state_values_return_default_game(self) -> None:
        """잘못된 퀴즈 구조와 점수 값을 기본 게임으로 복구해야 한다."""
        valid_quiz = {
            "question": "정상 문제",
            "choices": ["선택지1", "선택지2", "선택지3", "선택지4"],
            "answer": 1,
        }
        invalid_states = {
            "invalid_quiz": {
                "quizzes": [{"question": "", "choices": [], "answer": 0}],
                "score": {"correct_count": 0, "attempt_count": 0},
            },
            "empty_quizzes": {
                "quizzes": [],
                "score": {"correct_count": 0, "attempt_count": 0},
            },
            "score_not_a_dict": {
                "quizzes": [valid_quiz],
                "score": [],
            },
            "negative_score": {
                "quizzes": [valid_quiz],
                "score": {"correct_count": -1, "attempt_count": 0},
            },
            "correct_greater_than_attempt": {
                "quizzes": [valid_quiz],
                "score": {"correct_count": 2, "attempt_count": 1},
            },
            "boolean_score": {
                "quizzes": [valid_quiz],
                "score": {"correct_count": True, "attempt_count": 1},
            },
            "string_score": {
                "quizzes": [valid_quiz],
                "score": {"correct_count": "0", "attempt_count": 1},
            },
        }

        for case_name, invalid_state in invalid_states.items():
            with self.subTest(case=case_name):
                self.state_path.write_text(
                    json.dumps(invalid_state, ensure_ascii=False),
                    encoding="utf-8",
                )
                output = io.StringIO()

                with redirect_stdout(output):
                    game = load_state(self.state_path)

                self.assertIsInstance(game, QuizGame)
                self.assertGreaterEqual(len(game.quizzes), 10)
                self.assertEqual(game.correct_count, 0)
                self.assertEqual(game.attempt_count, 0)
                self.assertIn("손상", output.getvalue())

    def test_save_os_error_returns_false(self) -> None:
        """저장 중 OSError가 발생하면 안내 후 False를 반환해야 한다."""
        game = QuizGame()
        output = io.StringIO()

        with patch("storage.Path.open", side_effect=OSError("저장 실패")):
            with redirect_stdout(output):
                result = save_state(game, self.state_path)

        self.assertFalse(result)
        self.assertIn("상태를 저장하지 못했습니다", output.getvalue())

    def test_load_os_error_returns_default_game(self) -> None:
        """불러오기 중 OSError가 발생하면 안내 후 기본 게임을 반환해야 한다."""
        output = io.StringIO()

        with patch("storage.Path.open", side_effect=OSError("읽기 실패")):
            with redirect_stdout(output):
                game = load_state(self.state_path)

        self.assertIsInstance(game, QuizGame)
        self.assertGreaterEqual(len(game.quizzes), 10)
        self.assertEqual(game.correct_count, 0)
        self.assertEqual(game.attempt_count, 0)
        self.assertIn("손상", output.getvalue())


if __name__ == "__main__":
    unittest.main()
