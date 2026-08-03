"""옵션 투자기법 퀴즈 게임의 실행 파일."""

def show_menu() -> None:
    """사용자가 선택할 수 있는 메뉴를 출력한다."""
    print("\n" + "=" * 40)
    print("옵션 투자기법 퀴즈 게임")
    print("=" * 40)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("=" * 40)

def read_number(
    prompt: str,
    minimum: int,
    maximum: int
) -> int | None:
    """지정된 범위의 정수를 입력받는다."""
    while True:
        try:
            raw_value = input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            print("\n입력이 중단되었습니다.")
            return None
        if not raw_value:
            print("빈 입력은 사용할 수 없습니다.")
            continue
        try:
            number = int(raw_value)
        except ValueError:
            print("숫자만 입력할 수 있습니다.")
            continue
        if minimum <= number <= maximum:
            return number
        print(f"{minimum}~{maximum} 사이의 숫자를 입력해주세요.")


def main() -> None:
    """사용자가 종료를 선택할 때까지 메뉴를 반복한다."""
    while True:
        show_menu()
        choice = read_number("메뉴 선택: ", 1, 5)
        if choice is None:
            print("퀴즈 게임을 안전하게 종료합니다.")
            break

        if choice == 1:
            print("퀴즈 풀기 기능을 준비 중입니다.")
        elif choice == 2:
            print("퀴즈 추가 기능을 준비 중입니다.")
        elif choice == 3:
            print("퀴즈 목록 기능을 준비 중입니다.")
        elif choice == 4:
            print("점수 확인 기능을 준비 중입니다.")
        elif choice == 5:
            print("퀴즈 게임을 종료합니다.")
            break
if __name__ == "__main__":
    main()