"""Regression tests for the multilingual synthetic evaluation corpus."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from core.detector import analyze_message
from core.calibration import evaluate_synthetic_corpus

CASES = json.loads((ROOT / "tests" / "fixtures" / "messages.json").read_text(encoding="utf-8"))

class SyntheticCorpusTests(unittest.TestCase):
    def test_corpus_has_benign_and_suspicious_examples_in_all_languages(self):
        for language in ("fr", "en", "ar-DZ"):
            rows = [case for case in CASES if case["language"] == language]
            with self.subTest(language=language):
                self.assertTrue(any(case["label"] == "benign" for case in rows))
                self.assertTrue(any(case["label"] == "suspicious" for case in rows))

    def test_ordinary_brand_and_service_mentions_do_not_alone_trigger_alerts(self):
        examples = [
            ("fr", "J'utilise Microsoft Excel pour préparer mon exposé."),
            ("en", "The bank branch opens at 9 AM on weekdays."),
            ("ar", "البنك يفتح على الساعة التاسعة صباحاً في أيام الأسبوع."),
        ]
        for language, message in examples:
            with self.subTest(language=language, message=message):
                self.assertEqual(analyze_message(message, language)["findings"], [])

    def test_each_corpus_case_matches_its_binary_label(self):
        false_positives = []
        false_negatives = []
        for case in CASES:
            language = "ar" if case["language"] == "ar-DZ" else case["language"]
            predicted = bool(analyze_message(case["text"], language)["findings"])
            if case["label"] == "benign" and predicted:
                false_positives.append(case["id"])
            if case["label"] == "suspicious" and not predicted:
                false_negatives.append(case["id"])
        self.assertEqual(false_positives, [], f"Synthetic false positives: {false_positives}")
        self.assertEqual(false_negatives, [], f"Synthetic false negatives: {false_negatives}")

    def test_evaluation_reports_all_languages_and_rates(self):
        metrics = evaluate_synthetic_corpus(CASES)
        self.assertEqual(metrics["total"], len(CASES))
        self.assertEqual(set(metrics["by_language"]), {"fr", "en", "ar-DZ"})
        self.assertEqual(metrics["fp"], 0)
        self.assertEqual(metrics["fn"], 0)
        self.assertEqual(metrics["specificity"], 1.0)
        self.assertEqual(metrics["recall"], 1.0)

if __name__ == "__main__":
    unittest.main()
