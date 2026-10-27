import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "i18n"

class TranslationTests(unittest.TestCase):
    def test_all_interfaces_have_the_same_keys(self):
        translations = {
            path.stem: json.loads(path.read_text(encoding="utf-8"))
            for path in ROOT.glob("*.json")
        }
        self.assertEqual(set(translations), {"fr", "en", "ar"})
        expected = set(translations["fr"])
        for language, data in translations.items():
            with self.subTest(language=language):
                self.assertEqual(set(data), expected)
                self.assertTrue(all(isinstance(value, str) and value.strip() for value in data.values()))

if __name__ == "__main__":
    unittest.main()
