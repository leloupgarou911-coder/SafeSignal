"""Tests for safe, optional local OCR handling."""
import unittest
from io import BytesIO

from PIL import Image

from core.ocr import (
    MAX_IMAGE_BYTES,
    InvalidImageError,
    extract_text,
)


def png_bytes(size=(12, 12), color="white"):
    image = Image.new("RGB", size, color=color)
    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


class OCRInputTests(unittest.TestCase):
    def test_rejects_empty_input(self):
        with self.assertRaises(InvalidImageError):
            extract_text(b"")

    def test_rejects_oversized_upload_before_ocr(self):
        with self.assertRaises(InvalidImageError):
            extract_text(b"x" * (MAX_IMAGE_BYTES + 1))

    def test_rejects_invalid_image_bytes(self):
        with self.assertRaises(InvalidImageError):
            extract_text(b"not an image")

    def test_rejects_unsupported_image_format(self):
        image = Image.new("RGB", (12, 12), color="white")
        output = BytesIO()
        image.save(output, format="BMP")
        with self.assertRaises(InvalidImageError):
            extract_text(output.getvalue())

    def test_rejects_dimensions_over_limit(self):
        with self.assertRaises(InvalidImageError):
            extract_text(png_bytes(size=(5001, 1)))


if __name__ == "__main__":
    unittest.main()
