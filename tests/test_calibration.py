import unittest

from core.calibration import evaluate_synthetic_corpus


class SyntheticCalibrationTests(unittest.TestCase):
    def test_metrics_are_bounded_and_counts_cover_corpus(self):
        report = evaluate_synthetic_corpus()
        self.assertGreater(report["total"], 0)
        self.assertEqual(
            report["total"],
            report["tp"] + report["fp"] + report["tn"] + report["fn"],
        )
        for metric in ("precision", "recall", "specificity"):
            self.assertIsNotNone(report[metric])
            self.assertGreaterEqual(report[metric], 0.0)
            self.assertLessEqual(report[metric], 1.0)

    def test_corpus_has_separate_language_results(self):
        report = evaluate_synthetic_corpus()
        self.assertIn("fr", report["by_language"])
        self.assertIn("en", report["by_language"])
        self.assertIn("ar-DZ", report["by_language"])
        self.assertEqual(sum(
            row["tp"] + row["fp"] + row["tn"] + row["fn"]
            for row in report["by_language"].values()
        ), report["total"])

    def test_empty_input_has_undefined_rates_not_division_errors(self):
        report = evaluate_synthetic_corpus([])
        self.assertEqual(report["total"], 0)
        self.assertIsNone(report["precision"])
        self.assertIsNone(report["recall"])
        self.assertIsNone(report["specificity"])


if __name__ == "__main__":
    unittest.main()
