import tempfile
import unittest
from pathlib import Path

from core.detector import analyze_message
from db import storage


class CustomRuleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        storage.DB_PATH = Path(self.tmp.name) / "custom-rules.sqlite3"
        storage.init_db()

    def tearDown(self):
        self.tmp.cleanup()

    def test_add_list_duplicate_and_delete_custom_rule(self):
        self.assertTrue(storage.add_custom_rule("PAY NOW", "Urgent payment", "Check independently"))
        self.assertFalse(storage.add_custom_rule("pay now", "Duplicate", "Duplicate keyword"))
        rules = storage.get_custom_rules()
        self.assertEqual(len(rules), 1)
        rule_id, keyword, label, explanation = rules[0]
        self.assertEqual(keyword, "pay now")
        self.assertEqual(label, "Urgent payment")
        self.assertEqual(explanation, "Check independently")
        storage.delete_custom_rule(rule_id)
        self.assertEqual(storage.get_custom_rules(), [])

    def test_empty_custom_rule_is_rejected(self):
        with self.assertRaises(ValueError):
            storage.add_custom_rule(" ", "Alert", "Explanation")

    def test_custom_rule_is_included_as_low_confidence_finding(self):
        storage.add_custom_rule("invoice-verify", "My invoice warning", "Check the sender first")
        report = analyze_message(
            "Please invoice-verify now",
            "en",
            custom_rules=storage.get_custom_rules(),
        )
        finding = next(item for item in report["findings"] if item["rule_id"].startswith("custom_rule_"))
        self.assertEqual(finding["title"], "My invoice warning")
        self.assertEqual(finding["severity"], "low")
        self.assertEqual(finding["confidence"], "low")
        self.assertIn("Check the sender first", finding["explanation"])

    def test_custom_rules_are_optional_for_detector(self):
        report = analyze_message("A simple hello", "fr")
        self.assertEqual(report["findings"], [])


if __name__ == "__main__":
    unittest.main()
