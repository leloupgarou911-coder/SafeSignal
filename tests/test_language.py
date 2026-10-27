import unittest
from core.language import detect_language

class LanguageTests(unittest.TestCase):
    def test_arabic_script(self):
        self.assertEqual(detect_language("تم إيقاف حسابك، تحقق الآن"), "ar")
    def test_english_vocabulary(self):
        self.assertEqual(detect_language("Your account is suspended, verify your password"), "en")
    def test_french_vocabulary(self):
        self.assertEqual(detect_language("Votre compte est urgent, cliquez pour vérifier"), "fr")
    def test_algerian_service_names_in_french_message(self):
        self.assertEqual(detect_language("Votre compte BaridiMob est bloqué, vérifiez"), "fr")
    def test_empty_and_unknown_text_fallback(self):
        self.assertEqual(detect_language(""), "fr")
        self.assertEqual(detect_language("xyz qwerty"), "fr")

if __name__ == "__main__":
    unittest.main()
