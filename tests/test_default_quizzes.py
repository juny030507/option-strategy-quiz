"""기본 퀴즈 데이터의 구조와 품질을 검증한다."""

import unittest

from default_quizzes import create_default_quizzes
from quiz import Quiz


class TestDefaultQuizzes(unittest.TestCase):
    """기본 퀴즈 목록이 과제 지시사항을 만족하는지 테스트한다."""

    def setUp(self) -> None:
        """각 테스트에 새로운 기본 퀴즈 목록을 준비한다."""
        self.quizzes = create_default_quizzes()

    def test_contains_at_least_ten_quizzes(self) -> None:
        """기본 퀴즈가 10개 이상 포함되어 있어야 한다."""
        self.assertGreaterEqual(len(self.quizzes), 10)

    def test_all_items_are_quiz_instances(self) -> None:
        """목록의 모든 항목은 Quiz 객체여야 한다."""
        self.assertTrue(
            all(isinstance(quiz, Quiz) for quiz in self.quizzes)
        )

    def test_questions_are_unique(self) -> None:
        """서로 같은 문제가 중복되어서는 안 된다."""
        questions = [quiz.question for quiz in self.quizzes]
        self.assertEqual(len(questions), len(set(questions)))

    def test_all_quizzes_have_complete_data(self) -> None:
        """각 문제는 질문, 선택지 4개, 정상 정답 번호를 가져야 한다."""
        for quiz in self.quizzes:
            with self.subTest(question=quiz.question):
                self.assertTrue(quiz.question.strip())
                self.assertEqual(len(quiz.choices), 4)
                self.assertTrue(
                    all(choice.strip() for choice in quiz.choices)
                )
                self.assertIn(quiz.answer, range(1, 5))

    def test_covered_call_uses_consistent_term(self) -> None:
        """커버드 콜 문제가 정확하고 일관된 용어를 사용한다."""
        questions = [quiz.question for quiz in self.quizzes]

        self.assertTrue(
            any("커버드 콜(Covered Call)" in question for question in questions)
        )
        self.assertFalse(
            any("보증된 콜(Covered Call)" in question for question in questions)
        )


if __name__ == "__main__":
    unittest.main()
