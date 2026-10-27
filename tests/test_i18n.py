"""Regression tests for SafeSignal's interface translations."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "i18n"
LANGUAGES = ("fr", "en", "ar")


class TranslationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.translations = {
            path.stem: json.loads(path.read_text(encoding="utf-8"))
            for path in ROOT.glob("*.json")
        }

    def test_all_interfaces_have_the_same_keys(self):
        self.assertEqual(set(self.translations), set(LANGUAGES))
        expected = set(self.translations["fr"])
        for language, data in self.translations.items():
            with self.subTest(language=language):
                self.assertEqual(set(data), expected)

    def test_all_translation_values_are_non_empty_strings(self):
        for language, data in self.translations.items():
            for key, value in data.items():
                with self.subTest(language=language, key=key):
                    self.assertIsInstance(value, str)
                    self.assertTrue(value.strip())

    def test_format_placeholders_match_between_languages(self):
        def placeholders(value):
            return set(re.findall(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", value))

        reference = self.translations["fr"]
        for language in ("en", "ar"):
            for key in reference:
                with self.subTest(language=language, key=key):
                    self.assertEqual(
                        placeholders(reference[key]),
                        placeholders(self.translations[language][key]),
                        f"Format placeholders differ for {key}",
                    )


if __name__ == "__main__":
    unittest.main()
