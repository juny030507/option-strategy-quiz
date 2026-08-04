"""QuizGame 클래스의 퀴즈 및 점수 관리를 검증한다."""

import unittest

from quiz import Quiz
from quiz_game import QuizGame


class TestQuizGame(unittest.TestCase):
    """QuizGame 클래스의 핵심 동작을 테스트한다."""

    def setUp(self) -> None:
        """각 테스트에서 사용할 퀴즈와 게임을 준비한다."""
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

    def test_initial_quizzes_are_copied(self) -> None:
        """외부의 퀴즈 목록을 변경해도 게임 목록은 유지되어야 한다."""
        original_quizzes = [self.quiz]
        game = QuizGame(original_quizzes)

        original_quizzes.clear()

        self.assertEqual(len(game.quizzes), 1)

    def test_add_quiz(self) -> None:
        """새로운 Quiz 객체를 목록에 추가할 수 있어야 한다."""
        new_quiz = Quiz(
            "콜옵션 매수에 적합한 전망은?",
            ["강세장", "약세장", "횡보장", "방향과 무관"],
            1,
        )

        self.game.add_quiz(new_quiz)

        self.assertIn(new_quiz, self.game.quizzes)

    def test_correct_answer_updates_score(self) -> None:
        """정답을 제출하면 풀이 수와 정답 수가 증가해야 한다."""
        result = self.game.submit_answer(self.quiz, 1)

        self.assertTrue(result)
        self.assertEqual(self.game.correct_count, 1)
        self.assertEqual(self.game.attempt_count, 1)

    def test_wrong_answer_updates_attempt_only(self) -> None:
        """오답을 제출하면 풀이 수만 증가해야 한다."""
        result = self.game.submit_answer(self.quiz, 2)

        self.assertFalse(result)
        self.assertEqual(self.game.correct_count, 0)
        self.assertEqual(self.game.attempt_count, 1)

    def test_calculate_accuracy(self) -> None:
        """정답 수와 풀이 수를 이용하여 정답률을 계산해야 한다."""
        self.game.submit_answer(self.quiz, 1)
        self.game.submit_answer(self.quiz, 2)

        self.assertEqual(self.game.calculate_accuracy(), 50.0)

    def test_accuracy_is_zero_before_playing(self) -> None:
        """아직 문제를 풀지 않았다면 정답률은 0이어야 한다."""
        self.assertEqual(self.game.calculate_accuracy(), 0.0)

    def test_reset_score(self) -> None:
        """점수를 초기화하면 정답 수와 풀이 수가 모두 0이 되어야 한다."""
        self.game.submit_answer(self.quiz, 1)

        self.game.reset_score()

        self.assertEqual(self.game.correct_count, 0)
        self.assertEqual(self.game.attempt_count, 0)


if __name__ == "__main__":
    unittest.main()