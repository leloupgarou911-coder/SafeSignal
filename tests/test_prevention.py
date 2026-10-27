import unittest

from core.prevention import GUIDES, get_guides


class PreventionGuideTests(unittest.TestCase):
    def test_all_supported_languages_have_same_guide_ids(self):
        expected = [guide["id"] for guide in GUIDES["fr"]]
        self.assertEqual(len(expected), len(set(expected)))
        for language in ("fr", "en", "ar"):
            self.assertEqual([guide["id"] for guide in get_guides(language)], expected)

    def test_every_guide_has_complete_interactive_content(self):
        required = {"id", "icon", "title", "summary", "checklist", "legit_label", "legit", "scam_label", "scam"}
        for language in ("fr", "en", "ar"):
            for guide in get_guides(language):
                with self.subTest(language=language, guide=guide["id"]):
                    self.assertTrue(required.issubset(guide))
                    self.assertGreaterEqual(len(guide["checklist"]), 3)
                    self.assertTrue(all(item.strip() for item in guide["checklist"]))
                    self.assertTrue(guide["legit"].strip())
                    self.assertTrue(guide["scam"].strip())

    def test_unknown_language_falls_back_to_french(self):
        self.assertEqual(get_guides("unsupported"), get_guides("fr"))

    def test_guides_cover_common_scam_types(self):
        guide_ids = {guide["id"] for guide in get_guides("fr")}
        self.assertTrue({"phishing", "parcel", "bank", "tech_support"}.issubset(guide_ids))


if __name__ == "__main__":
    unittest.main()
