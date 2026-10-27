import unittest
from core.detector import analyze_message

class RegionalRuleTests(unittest.TestCase):
    def test_algerian_payment_brand_is_flagged_as_context_not_proof(self):
        report = analyze_message("Votre compte BaridiMob est bloqué", "fr")
        item = next(x for x in report["findings"] if x["rule_id"] == "regional_payment_impersonation")
        self.assertIn("ne prouve pas", item["explanation"])
    def test_delivery_fee_pattern(self):
        report = analyze_message("Votre colis est bloqué, frais de livraison à payer", "fr")
        self.assertIn("delivery_fee", [x["rule_id"] for x in report["findings"]])
    def test_report_translation_uses_selected_language(self):
        report = analyze_message("Votre compte BaridiMob est bloqué", "en")
        item = next(x for x in report["findings"] if x["rule_id"] == "regional_payment_impersonation")
        self.assertEqual(item["title"], "Payment service or carrier mentioned")
        self.assertEqual(report["language"], "en")

if __name__ == "__main__":
    unittest.main()
