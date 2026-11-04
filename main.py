import json
import os


class Quiz:
    def __init__(self, question, answer, choices):
        self.question = question
        self.answer = answer
        self.choices = choices

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.high_score = 0
        self.filename = "state.json"

    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as file:
                    data = json.load(file)

                self.high_score = data.get("high_score", 0)
                self.quizzes = data.get("quizzes", [])

            except (json.JSONDecodeError, OSError, AttributeError):
                print("저장 파일을 읽을 수 없어 기본 퀴즈를 불러옵니다.")
                self.quizzes = []
                self.high_score = 0

        if not self.quizzes:
            self.quizzes = [
                {
                    "question": "강아지가 꼬리를 흔드는 행동은 무엇을 표현할까요?",
                    "choices": ["기쁨이나 흥분", "배고픔", "졸음", "추위"],
                    "answer": "1"
                },
                {
                    "question": "고양이가 기분 좋을 때 내는 소리는?",
                    "choices": ["멍멍", "골골송", "짹짹", "꿀꿀"],
                    "answer": "2"
                },
                {
                    "question": "토끼가 좋아하는 먹이로 잘 알려진 것은?",
                    "choices": ["초콜릿", "사탕", "건초", "과자"],
                    "answer": "3"
                },
                {
                    "question": "햄스터가 먹이를 저장하는 신체 부위는?",
                    "choices": ["볼주머니", "꼬리", "귀", "발"],
                    "answer": "1"
                },
                {
                    "question": "펭귄은 주로 어디에서 생활할까요?",
                    "choices": ["사막", "바다와 해안", "나무 위", "동굴 속"],
                    "answer": "2"
                }
            ]
            self.save_data()

    def save_data(self):
        data = {
            "high_score": self.high_score,
            "quizzes": self.quizzes
        }

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def play_quiz(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        score = 0

        for index, quiz_data in enumerate(self.quizzes, 1):
            quiz = Quiz(
                quiz_data["question"],
                quiz_data["answer"],
                quiz_data["choices"]
            )

            print(f"\n문제 {index}. {quiz.question}")

            for number, choice in enumerate(quiz.choices, 1):
                print(f"{number}. {choice}")

            while True:
                answer = input("정답 번호를 입력하세요: ").strip()

                if answer.isdigit() and 1 <= int(answer) <= len(quiz.choices):
                    break

                print("올바른 번호를 입력해 주세요.")

            if answer == quiz.answer:
                print("정답입니다!")
                score += 1
            else:
                print("아쉽지만 오답입니다.")
                print(f"정답은 {quiz.answer}번: {quiz.choices[int(quiz.answer) - 1]}입니다.")

        print(f"\n최종 점수: {score}/{len(self.quizzes)}")

        if score > self.high_score:
            self.high_score = score
            self.save_data()
            print("최고 점수가 갱신되었습니다!")

    def add_quiz(self):
        print("\n===== 새 퀴즈 추가 =====")

        question = input("문제를 입력하세요: ").strip()

        while not question:
            print("문제는 비워둘 수 없습니다.")
            question = input("문제를 입력하세요: ").strip()

        choices = []

        for i in range(1, 5):
            while True:
                choice = input(f"{i}번 선택지를 입력하세요: ").strip()

                if not choice:
                    print("선택지는 비워둘 수 없습니다.")
                    continue

                if choice in choices:
                    print("이미 입력한 선택지입니다. 다른 내용을 입력해 주세요.")
                    continue

                choices.append(choice)
                break
        while True:
            answer = input("정답 번호를 입력하세요 (1~4): ").strip()

            if answer in ["1", "2", "3", "4"]:
                break

            print("1~4 사이의 번호를 입력해 주세요.")
        for quiz in self.quizzes:
            if quiz["question"] == question:
                print("이미 등록된 문제입니다.")
                return
        new_quiz = Quiz(question, answer, choices)

        self.quizzes.append(new_quiz.to_dict())
        self.save_data()

        print("새 퀴즈가 저장되었습니다!")

    def show_quizzes(self):
        print("\n===== 퀴즈 목록 =====")

        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        for index, quiz in enumerate(self.quizzes, 1):
            print(f"{index}. {quiz['question']}")

        print(f"\n총 {len(self.quizzes)}개의 퀴즈가 있습니다.")

    def delete_quiz(self):
        print("\n===== 퀴즈 삭제 =====")

        if not self.quizzes:
            print("삭제할 퀴즈가 없습니다.")
            return

        self.show_quizzes()

        while True:
            choice = input("\n삭제할 퀴즈 번호를 입력하세요 (취소: 0): ").strip()

            if choice == "0":
                print("퀴즈 삭제를 취소했습니다.")
                return

            if choice.isdigit() and 1 <= int(choice) <= len(self.quizzes):
                break

            print("목록에 있는 번호를 입력해 주세요.")

        index = int(choice) - 1
        question = self.quizzes[index]["question"]

        print(f"\n삭제할 문제: {question}")

        confirm = input("정말 삭제할까요? (y/n): ").strip().lower()

        if confirm == "y":
            self.quizzes.pop(index)
            self.save_data()
            print("퀴즈가 삭제되었습니다!")
        else:
            print("퀴즈 삭제를 취소했습니다.")

    def show_high_score(self):
        print("\n===== 최고 점수 =====")
        print(f"최고 점수: {self.high_score}점")

    def show_menu(self):
        while True:
            print("\n===== 귀여운 동물 상식 퀴즈 =====")
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가")
            print("3. 퀴즈 목록")
            print("4. 최고 점수 보기")
            print("5. 퀴즈 삭제")
            print("6. 종료")

            choice = input("메뉴를 선택하세요: ").strip()

            if choice == "1":
                self.play_quiz()
            elif choice == "2":
                self.add_quiz()
            elif choice == "3":
                self.show_quizzes()
            elif choice == "4":
                self.show_high_score()
            elif choice == "5":
                self.delete_quiz()
            elif choice == "6":
                print("퀴즈 게임을 종료합니다!")
                break
            else:
                print("1~6 사이의 번호를 입력해 주세요.")


if __name__ == "__main__":
    game = QuizGame()

    try:
        game.load_data()
        game.show_menu()

    except (KeyboardInterrupt, EOFError):
        print("\n프로그램을 안전하게 종료합니다.")
        try:
            game.save_data()
        except OSError:
            print("저장에 실패했습니다. 저장 파일을 확인해 주세요.")