"""퀴즈 목록과 점수를 관리하는 게임 클래스를 제공한다."""

from quiz import Quiz


class QuizGame:
    """퀴즈 추가, 정답 확인, 점수 계산을 담당한다."""

    def __init__(self, quizzes: list[Quiz] | None = None) -> None:
        """초기 퀴즈 목록과 점수를 설정한다."""
        self.quizzes = list(quizzes) if quizzes is not None else []

        if not all(isinstance(quiz, Quiz) for quiz in self.quizzes):
            raise TypeError("퀴즈 목록에는 Quiz 객체만 넣을 수 있습니다.")

        self.correct_count = 0
        self.attempt_count = 0
        self.best_score = 0
        self.best_total = 0
        self.session_answered_count = 0
        self.session_correct_count = 0
        self.session_total = 0

    def add_quiz(self, quiz: Quiz) -> None:
        """게임에 새로운 퀴즈를 추가한다."""
        if not isinstance(quiz, Quiz):
            raise TypeError("Quiz 객체만 추가할 수 있습니다.")

        self.quizzes.append(quiz)

    def submit_answer(self, quiz: Quiz, selected_answer: int) -> bool:
        """답안을 채점하고 누적 점수를 갱신한다."""
        if quiz not in self.quizzes:
            raise ValueError("게임에 등록되지 않은 퀴즈입니다.")

        if type(selected_answer) is not int or not 1 <= selected_answer <= 4:
            raise ValueError("정답 번호는 1~4 사이여야 합니다.")

        self.attempt_count += 1
        is_correct = quiz.is_correct(selected_answer)

        if is_correct:
            self.correct_count += 1

        return is_correct

    def calculate_accuracy(self) -> float:
        """현재까지의 정답률을 백분율로 반환한다."""
        if self.attempt_count == 0:
            return 0.0

        return (self.correct_count / self.attempt_count) * 100

    def has_active_session(self) -> bool:
        """중단 후 이어서 풀 수 있는 회차가 있는지 반환한다."""
        return self.session_total > 0

    def start_session(self) -> None:
        """현재 퀴즈 목록으로 새로운 풀이 회차를 시작한다."""
        if not self.quizzes:
            raise ValueError("등록된 퀴즈가 없어 회차를 시작할 수 없습니다.")

        self.session_answered_count = 0
        self.session_correct_count = 0
        self.session_total = len(self.quizzes)

    def submit_session_answer(
        self,
        quiz: Quiz,
        selected_answer: int,
    ) -> bool:
        """진행 중인 회차의 다음 답안을 채점하고 진행 상태를 갱신한다."""
        if not self.has_active_session():
            raise ValueError("진행 중인 퀴즈 회차가 없습니다.")

        if self.session_answered_count >= self.session_total:
            raise ValueError("현재 회차의 모든 문제를 이미 풀었습니다.")

        expected_quiz = self.quizzes[self.session_answered_count]
        if quiz is not expected_quiz:
            raise ValueError("현재 순서의 퀴즈가 아닙니다.")

        is_correct = self.submit_answer(quiz, selected_answer)
        self.session_answered_count += 1

        if is_correct:
            self.session_correct_count += 1

        return is_correct

    def restore_session(
        self,
        answered_count: int,
        correct_count: int,
        total_questions: int,
    ) -> None:
        """저장 파일에서 검증된 진행 중 회차를 복원한다."""
        values = (answered_count, correct_count, total_questions)
        if any(type(value) is not int for value in values):
            raise TypeError("진행 상태의 문제 수와 점수는 정수여야 합니다.")

        if not 0 < total_questions <= len(self.quizzes):
            raise ValueError("진행 회차의 전체 문제 수가 올바르지 않습니다.")

        if not 0 <= answered_count < total_questions:
            raise ValueError("푼 문제 수가 진행 회차 범위를 벗어났습니다.")

        if not 0 <= correct_count <= answered_count:
            raise ValueError("현재 정답 수는 푼 문제 수보다 클 수 없습니다.")

        self.session_answered_count = answered_count
        self.session_correct_count = correct_count
        self.session_total = total_questions

    def finish_session(self) -> bool:
        """완료한 회차를 최고 점수와 비교한 뒤 진행 상태를 비운다."""
        if (
            not self.has_active_session()
            or self.session_answered_count != self.session_total
        ):
            raise ValueError("아직 완료하지 않은 회차입니다.")

        is_new_best = self.update_best_score(
            self.session_correct_count,
            self.session_total,
        )
        self.session_answered_count = 0
        self.session_correct_count = 0
        self.session_total = 0
        return is_new_best

    def update_best_score(
        self,
        session_score: int,
        total_questions: int,
    ) -> bool:
        """완료한 한 회차의 점수가 최고 기록이면 갱신한다."""
        if type(session_score) is not int or type(total_questions) is not int:
            raise TypeError("점수와 문제 수는 정수여야 합니다.")

        if total_questions <= 0 or not 0 <= session_score <= total_questions:
            raise ValueError("점수는 0부터 전체 문제 수 사이여야 합니다.")

        if self.best_total == 0 or session_score > self.best_score:
            self.best_score = session_score
            self.best_total = total_questions
            return True

        return False

    def reset_score(self) -> None:
        """누적 점수와 풀이 횟수를 초기화한다."""
        self.correct_count = 0
        self.attempt_count = 0
