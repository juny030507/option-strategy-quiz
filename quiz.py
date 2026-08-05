"""개별 퀴즈 문제를 표현하는 클래스"""


class Quiz:
    """문제, 선택지, 정답을 하나의 객체로 관리한다."""

    def __init__(
        self,
        question: str,
        choices: list[str],
        answer: int,
    ) -> None:
        """Quiz 객체를 생성하고 전달받은 값을 속성에 저장한다."""
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제는 비어 있지 않은 문자열이어야 합니다.")

        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 정확히 4개여야 합니다.")

        if not all(
            isinstance(choice, str) and choice.strip()
            for choice in choices
        ):
            raise ValueError(
                "선택지는 모두 비어 있지 않은 문자열이어야 합니다."
            )

        if type(answer) is not int or not 1 <= answer <= 4:
            raise ValueError("정답은 1~4 사이의 정수여야 합니다.")

        self.question = question
        self.choices = choices.copy()
        self.answer = answer

    def display(self) -> None:
        """문제와 네 개의 선택지를 출력한다."""
        print(self.question)

        for number, choice in enumerate(self.choices, start=1):
            print(f"{number}. {choice}")

    def is_correct(self, selected_answer: int) -> bool:
        """사용자가 선택한 번호가 정답인지 확인한다."""
        return selected_answer == self.answer
