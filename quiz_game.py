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

    def add_quiz(self, quiz: Quiz) -> None:
        """게임에 새로운 퀴즈를 추가한다."""
        if not isinstance(quiz, Quiz):
            raise TypeError("Quiz 객체만 추가할 수 있습니다.")

        self.quizzes.append(quiz)

    def submit_answer(self, quiz: Quiz, selected_answer: int) -> bool:
        """답안을 채점하고 누적 점수를 갱신한다."""
        if quiz not in self.quizzes:
            raise ValueError("게임에 등록되지 않은 퀴즈입니다.")

        if selected_answer not in range(1, 5):
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

    def reset_score(self) -> None:
        """누적 점수와 풀이 횟수를 초기화한다."""
        self.correct_count = 0
        self.attempt_count = 0

