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

    def test_initial_quizzes_reject_non_quiz_item(self) -> None:
        """초기 목록에 Quiz가 아닌 객체가 있으면 거부한다."""
        with self.assertRaises(TypeError):
            QuizGame([object()])

    def test_add_quiz_rejects_non_quiz_item(self) -> None:
        """Quiz가 아닌 객체를 게임에 추가할 수 없어야 한다."""
        with self.assertRaises(TypeError):
            self.game.add_quiz(object())

    def test_submit_answer_rejects_unregistered_quiz(self) -> None:
        """게임에 등록되지 않은 퀴즈는 채점하지 않는다."""
        unregistered_quiz = Quiz(
            "스트래들 매수의 구성은?",
            ["콜 매수 + 풋 매수", "콜 매도", "풋 매도", "기초자산 매수"],
            1,
        )

        with self.assertRaises(ValueError):
            self.game.submit_answer(unregistered_quiz, 1)

        self.assertEqual(self.game.correct_count, 0)
        self.assertEqual(self.game.attempt_count, 0)

    def test_submit_answer_rejects_invalid_answer(self) -> None:
        """범위 밖이거나 정수가 아닌 답안은 점수에 반영하지 않는다."""
        for invalid_answer in (0, 5, True, "1"):
            with self.subTest(answer=invalid_answer):
                with self.assertRaises(ValueError):
                    self.game.submit_answer(self.quiz, invalid_answer)

        self.assertEqual(self.game.correct_count, 0)
        self.assertEqual(self.game.attempt_count, 0)

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

    def test_first_completed_session_sets_best_score(self) -> None:
        """첫 완료 회차는 0점이어도 최고 기록으로 저장해야 한다."""
        updated = self.game.update_best_score(0, 1)

        self.assertTrue(updated)
        self.assertEqual(self.game.best_score, 0)
        self.assertEqual(self.game.best_total, 1)

    def test_higher_session_score_updates_best_score(self) -> None:
        """기존 기록보다 높은 회차 점수로 최고 기록을 갱신해야 한다."""
        self.game.update_best_score(1, 4)

        updated = self.game.update_best_score(3, 4)

        self.assertTrue(updated)
        self.assertEqual(self.game.best_score, 3)
        self.assertEqual(self.game.best_total, 4)

    def test_lower_session_score_keeps_best_score(self) -> None:
        """기존 기록보다 낮은 회차 점수는 최고 기록을 바꾸지 않는다."""
        self.game.update_best_score(3, 4)

        updated = self.game.update_best_score(2, 5)

        self.assertFalse(updated)
        self.assertEqual(self.game.best_score, 3)
        self.assertEqual(self.game.best_total, 4)

    def test_update_best_score_rejects_invalid_values(self) -> None:
        """잘못된 회차 점수와 문제 수는 최고 기록에 반영하지 않는다."""
        invalid_values = ((-1, 4), (5, 4), (0, 0), (True, 4), (1, "4"))

        for session_score, total_questions in invalid_values:
            with self.subTest(
                score=session_score,
                total=total_questions,
            ):
                with self.assertRaises((TypeError, ValueError)):
                    self.game.update_best_score(
                        session_score,
                        total_questions,
                    )

    def test_reset_score(self) -> None:
        """누적 통계를 초기화해도 최고 점수는 유지되어야 한다."""
        self.game.submit_answer(self.quiz, 1)
        self.game.update_best_score(1, 1)

        self.game.reset_score()

        self.assertEqual(self.game.correct_count, 0)
        self.assertEqual(self.game.attempt_count, 0)
        self.assertEqual(self.game.best_score, 1)
        self.assertEqual(self.game.best_total, 1)


if __name__ == "__main__":
    unittest.main()
