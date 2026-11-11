
import json
import os
import tempfile
import unittest

from main import Quiz, QuizGame


class QuizGameTest(unittest.TestCase):

    def test_quiz_to_dict(self):
        quiz = Quiz("강아지 문제", "1", ["기쁨", "배고픔", "졸음", "추위"])

        result = quiz.to_dict()

        self.assertEqual(result["question"], "강아지 문제")
        self.assertEqual(result["answer"], "1")
        self.assertEqual(len(result["choices"]), 4)

    def test_save_and_load_data(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame()
            game.filename = os.path.join(temp_dir, "test_state.json")
            game.high_score = 3
            game.quizzes = [
                {
                    "question": "고양이가 기분 좋을 때 내는 소리는?",
                    "choices": ["멍멍", "골골송", "짹짹", "꿀꿀"],
                    "answer": "2"
                }
            ]

            self.assertTrue(game.save_data())

            loaded_game = QuizGame()
            loaded_game.filename = game.filename
            loaded_game.load_data()

            self.assertEqual(loaded_game.high_score, 3)
            self.assertEqual(len(loaded_game.quizzes), 1)
            self.assertEqual(
                loaded_game.quizzes[0]["answer"], "2"
            )

    def test_invalid_quiz_is_ignored(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            game = QuizGame()
            game.filename = os.path.join(temp_dir, "test_state.json")

            data = {
                "high_score": 0,
                "quizzes": [
                    {
                        "question": "잘못된 문제",
                        "choices": ["하나", "둘"],
                        "answer": "1"
                    }
                ]
            }

            with open(game.filename, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False)

            game.load_data()

            self.assertEqual(len(game.quizzes), 5)


if __name__ == "__main__":
    unittest.main()
