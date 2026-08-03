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

def main() -> None:
    """사용자가 종료를 선택할 때까지 메뉴를 반복한다."""
    while True:
        show_menu()
        choice = input("메뉴 선택: ").strip()
        if choice == "1":
            print("퀴즈 풀기 기능을 준비 중입니다.")
        elif choice == "2":
            print("퀴즈 추가 기능을 준비 중입니다.")
        elif choice == "3":
            print("퀴즈 목록 기능을 준비 중입니다.")
        elif choice == "4":
            print("점수 확인 기능을 준비 중입니다.")
        elif choice == "5":
            print("퀴즈 게임을 종료합니다.")
            break
        else:
            print("1~5 사이의 숫자를 입력해주세요.")
if __name__ == "__main__":
    main()