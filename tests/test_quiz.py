"""Quiz 클래스의 동작을 검증하는 테스트"""

import unittest

from quiz import Quiz


class TestQuiz(unittest.TestCase):
    """Quiz 클래스의 핵심 기능을 테스트한다."""

    def setUp(self) -> None:
        """각 테스트에서 사용할 정상적인 퀴즈를 준비한다."""
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

    def test_correct_answer_returns_true(self) -> None:
        """정답을 선택하면 True를 반환한다."""
        self.assertTrue(self.quiz.is_correct(1))

    def test_wrong_answer_returns_false(self) -> None:
        """오답을 선택하면 False를 반환한다."""
        self.assertFalse(self.quiz.is_correct(2))

    def test_quiz_requires_four_choices(self) -> None:
        """선택지가 4개가 아니면 객체 생성을 거부한다."""
        with self.assertRaises(ValueError):
            Quiz("잘못된 문제", ["선택지1", "선택지2"], 1)

    def test_answer_must_be_between_one_and_four(self) -> None:
        """정답 번호가 1~4 사이가 아니면 객체 생성을 거부한다."""
        for invalid_answer in (0, 5):
            with self.subTest(answer=invalid_answer):
                with self.assertRaises(ValueError):
                    Quiz(
                        "잘못된 정답 번호",
                        ["선택지1", "선택지2", "선택지3", "선택지4"],
                        invalid_answer,
                    )

    def test_question_must_be_non_empty_string(self) -> None:
        """문제가 빈 문자열이거나 문자열이 아니면 생성을 거부한다."""
        for invalid_question in ("", "   ", None):
            with self.subTest(question=invalid_question):
                with self.assertRaises(ValueError):
                    Quiz(
                        invalid_question,
                        ["선택지1", "선택지2", "선택지3", "선택지4"],
                        1,
                    )

    def test_choices_must_be_non_empty_string_list(self) -> None:
        """선택지가 문자열 목록이 아니거나 빈 값을 포함하면 거부한다."""
        invalid_choices = (
            ["선택지1", "", "선택지3", "선택지4"],
            ["선택지1", "   ", "선택지3", "선택지4"],
            ["선택지1", 2, "선택지3", "선택지4"],
            ("선택지1", "선택지2", "선택지3", "선택지4"),
        )

        for choices in invalid_choices:
            with self.subTest(choices=choices):
                with self.assertRaises(ValueError):
                    Quiz("잘못된 선택지", choices, 1)

    def test_answer_must_be_integer_not_boolean(self) -> None:
        """정답은 불리언이나 문자열이 아닌 정수여야 한다."""
        for invalid_answer in (True, "1"):
            with self.subTest(answer=invalid_answer):
                with self.assertRaises(ValueError):
                    Quiz(
                        "잘못된 정답 타입",
                        ["선택지1", "선택지2", "선택지3", "선택지4"],
                        invalid_answer,
                    )


if __name__ == "__main__":
    unittest.main()
