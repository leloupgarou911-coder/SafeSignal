"""Accessibility regression checks for focus visibility, contrast and labels."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def relative_luminance(hex_color: str) -> float:
    values = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [
        value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4
        for value in values
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(foreground: str, background: str) -> float:
    first, second = sorted(
        (relative_luminance(foreground), relative_luminance(background)),
        reverse=True,
    )
    return (first + 0.05) / (second + 0.05)


class AccessibilityRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = (ROOT / "app.py").read_text(encoding="utf-8")
        cls.translations = {
            language: json.loads((ROOT / "i18n" / f"{language}.json").read_text(encoding="utf-8"))
            for language in ("fr", "en", "ar")
        }

    def test_keyboard_focus_and_skip_link_are_defined(self):
        self.assertIn(":focus-visible", self.app)
        self.assertIn("outline:3px solid #075fc7", self.app)
        self.assertIn(".skip-link:focus", self.app)
        self.assertIn('href="#main-content"', self.app)
        self.assertIn('id="main-content" tabindex="-1"', self.app)

    def test_text_colors_meet_wcag_aa_for_normal_text(self):
        # WCAG AA contrast target for normal text is at least 4.5:1.
        self.assertGreaterEqual(contrast_ratio("#465568", "#ffffff"), 4.5)
        self.assertGreaterEqual(contrast_ratio("#243447", "#ffffff"), 4.5)
        self.assertGreaterEqual(contrast_ratio("#12344d", "#eaf5ff"), 4.5)
        self.assertGreaterEqual(contrast_ratio("#12344d", "#ffffff"), 4.5)

    def test_focus_color_is_distinguishable_from_white(self):
        self.assertGreaterEqual(contrast_ratio("#075fc7", "#ffffff"), 3.0)

    def test_accessible_descriptions_exist_in_every_language(self):
        required = ("skip_to_content", "message_help", "ocr_language_help")
        for language, data in self.translations.items():
            with self.subTest(language=language):
                for key in required:
                    self.assertTrue(data.get(key, "").strip(), f"Missing {key}")
        self.assertIn('help=T["message_help"]', self.app)
        self.assertIn('help=T["ocr_language_help"]', self.app)

    def test_direction_is_set_for_arabic_and_latin_languages(self):
        self.assertIn('direction = "rtl" if lang == "ar" else "ltr"', self.app)


if __name__ == "__main__":
    unittest.main()
