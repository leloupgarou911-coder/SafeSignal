import unittest

from core.quiz import QUIZ_QUESTIONS, get_quiz


class QuizTests(unittest.TestCase):
    def test_supported_languages_have_same_question_ids(self):
        expected = [question["id"] for question in QUIZ_QUESTIONS["fr"]]
        self.assertEqual(len(expected), len(set(expected)))
        for language in ("fr", "en", "ar"):
            self.assertEqual([q["id"] for q in get_quiz(language)], expected)

    def test_questions_have_complete_content(self):
        for language in ("fr", "en", "ar"):
            for question in get_quiz(language):
                with self.subTest(language=language, question=question["id"]):
                    self.assertTrue(question["message"].strip())
                    self.assertIsInstance(question["is_scam"], bool)
                    self.assertTrue(question["explanation"].strip())

    def test_unknown_language_falls_back_to_french(self):
        self.assertEqual(get_quiz("unsupported"), get_quiz("fr"))


if __name__ == "__main__":
    unittest.main()
