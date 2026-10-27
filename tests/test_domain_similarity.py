import unittest

from core.detector import analyze_message
from core.rules.domain_similarity import analyze_suspicious_domains


class DomainSimilarityTests(unittest.TestCase):
    def test_detects_near_match_to_known_algerian_domain(self):
        findings = analyze_suspicious_domains("Visitez https://bar1dimob.com/login", "fr")
        self.assertTrue(findings)
        self.assertIn(findings[0]["rule_id"], {"lookalike_domain", "domain_suffix_mismatch"})

    def test_detects_unicode_confusable_domain(self):
        # Cyrillic 'і' visually resembles Latin 'i'.
        findings = analyze_suspicious_domains("https://bar\u0456dimob.dz/login", "en")
        self.assertTrue(findings)
        self.assertIn("homoglyph_domain", [item["rule_id"] for item in findings])

    def test_official_domain_does_not_trigger_similarity_rule(self):
        findings = analyze_suspicious_domains("https://baridimob.dz", "fr")
        self.assertEqual(findings, [])

    def test_unrelated_domain_does_not_trigger_similarity_rule(self):
        findings = analyze_suspicious_domains("https://example.org/path", "fr")
        self.assertEqual(findings, [])

    def test_integrated_detector_explains_domain_warning(self):
        report = analyze_message("Please review https://bar1dimob.com/login", "en")
        item = next(
            (finding for finding in report["findings"]
             if finding["rule_id"] in {"lookalike_domain", "domain_suffix_mismatch", "homoglyph_domain"}),
            None,
        )
        self.assertIsNotNone(item)
        self.assertTrue(item["explanation"])
        self.assertTrue(item["advice"])
        self.assertEqual(item["confidence"], "low")


if __name__ == "__main__":
    unittest.main()
