import json
import unittest
from pathlib import Path

from core.detector import analyze_message


FIXTURES = Path(__file__).parent / "fixtures" / "messages.json"


class MultilingualFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = json.loads(FIXTURES.read_text(encoding="utf-8"))

    def test_fixture_corpus_has_each_requested_language(self):
        languages = {case["language"] for case in self.cases}
        self.assertTrue({"fr", "ar-DZ", "en"}.issubset(languages))

    def test_suspicious_examples_trigger_expected_rule(self):
        for case in self.cases:
            if case["label"] != "suspicious":
                continue
            with self.subTest(case=case["id"]):
                language = "ar" if case["language"] == "ar-DZ" else case["language"]
                report = analyze_message(case["text"], language)
                rule_ids = {finding["rule_id"] for finding in report["findings"]}
                self.assertIn(case["expected_rule"], rule_ids)

    def test_benign_examples_do_not_trigger_regional_or_delivery_rules(self):
        guarded_rules = {"regional_payment_impersonation", "delivery_fee"}
        for case in self.cases:
            if case["label"] != "benign":
                continue
            with self.subTest(case=case["id"]):
                language = "ar" if case["language"] == "ar-DZ" else case["language"]
                report = analyze_message(case["text"], language)
                rule_ids = {finding["rule_id"] for finding in report["findings"]}
                self.assertTrue(guarded_rules.isdisjoint(rule_ids), rule_ids)

    def test_brand_mention_without_risk_cue_is_not_a_regional_finding(self):
        report = analyze_message("J'utilise BaridiMob pour consulter mes opérations.", "fr")
        self.assertNotIn(
            "regional_payment_impersonation",
            {finding["rule_id"] for finding in report["findings"]},
        )


if __name__ == "__main__":
    unittest.main()
