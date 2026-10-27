import unittest
from core.detector import analyze_message
from core.language import detect_language


class DetectorTests(unittest.TestCase):
    def test_urgency(self):
        self.assertIn("urgency", [x["rule_id"] for x in analyze_message("URGENT act now", "en")["findings"]])

    def test_reward(self):
        self.assertIn("reward", [x["rule_id"] for x in analyze_message("Vous avez gagné un cadeau gratuit", "fr")["findings"]])

    def test_keyword_dictionary_detects_french_phrases(self):
        findings = analyze_message("Dernière chance : votre compte suspendu, cliquez ici.", "fr")["findings"]
        rule_ids = [item["rule_id"] for item in findings]
        self.assertIn("urgency", rule_ids)

    def test_keyword_dictionary_detects_english_reward(self):
        findings = analyze_message("Congratulations, you won a prize!", "en")["findings"]
        self.assertIn("reward", [item["rule_id"] for item in findings])

    def test_keyword_dictionary_detects_arabic_urgency_and_reward(self):
        report = analyze_message("عاجل، مبروك ربحت جائزة، اضغط هنا", "ar")
        rule_ids = [item["rule_id"] for item in report["findings"]]
        self.assertIn("urgency", rule_ids)
        self.assertIn("reward", rule_ids)

    def test_short_link(self):
        self.assertIn("short_link", [x["rule_id"] for x in analyze_message("https://bit.ly/abc", "fr")["findings"]])

    def test_sensitive_data(self):
        self.assertIn("sensitive_data", [x["rule_id"] for x in analyze_message("confirmez votre mot de passe", "fr")["findings"]])

    def test_no_false_verdict(self):
        self.assertEqual(analyze_message("Bonjour à demain", "fr")["findings"], [])

    def test_arabic_language(self):
        self.assertEqual(detect_language("رمز التحقق عاجل"), "ar")

    def test_explanations_exist(self):
        self.assertTrue(all(x["advice"] and x["explanation"] for x in analyze_message("Vous avez gagné", "fr")["findings"]))


if __name__ == "__main__":
    unittest.main()
