"""Optional offline OCR for screenshots of suspicious messages.

Images are processed in memory only: this module never saves or uploads them.
Install the optional OCR dependencies and the local Tesseract executable to use it.
"""
from __future__ import annotations

from io import BytesIO

MAX_IMAGE_BYTES = 8 * 1024 * 1024
MAX_IMAGE_PIXELS = 16_000_000
MAX_IMAGE_SIDE = 5_000
ALLOWED_FORMATS = {"PNG", "JPEG", "WEBP"}


class OCRUnavailableError(RuntimeError):
    """Raised when local OCR software or language data is unavailable."""


class InvalidImageError(ValueError):
    """Raised when an uploaded image is invalid or exceeds safety limits."""


def extract_text(image_bytes: bytes, language: str = "fra+eng") -> str:
    """Extract text locally from a PNG, JPEG or WebP image.

    Supported Tesseract language codes should be installed locally:
    fra+eng (French), eng (English), ara+eng (Arabic with Latin text).
    """
    if not isinstance(image_bytes, bytes) or not image_bytes:
        raise InvalidImageError("The image is empty or invalid.")
    if len(image_bytes) > MAX_IMAGE_BYTES:
        raise InvalidImageError("The image exceeds the 8 MB limit.")

    try:
        from PIL import Image, UnidentifiedImageError
    except ImportError as exc:
        raise OCRUnavailableError(
            "Install the optional dependencies with: pip install '.[ocr]'"
        ) from exc

    try:
        with Image.open(BytesIO(image_bytes)) as image:
            if image.format not in ALLOWED_FORMATS:
                raise InvalidImageError("Use a PNG, JPEG or WebP image.")
            width, height = image.size
            if width > MAX_IMAGE_SIDE or height > MAX_IMAGE_SIDE:
                raise InvalidImageError("The image dimensions must not exceed 5000 × 5000 pixels.")
            if width * height > MAX_IMAGE_PIXELS:
                raise InvalidImageError("The image contains too many pixels.")
            image.load()
            prepared = image.convert("RGB")
    except InvalidImageError:
        raise
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise InvalidImageError("The uploaded file is not a valid supported image.") from exc

    try:
        import pytesseract
        from pytesseract import TesseractError, TesseractNotFoundError
    except ImportError as exc:
        raise OCRUnavailableError(
            "Install the optional dependencies with: pip install '.[ocr]'"
        ) from exc

    try:
        return pytesseract.image_to_string(prepared, lang=language).strip()
    except TesseractNotFoundError as exc:
        raise OCRUnavailableError(
            "Tesseract is not installed or is not available in PATH."
        ) from exc
    except TesseractError as exc:
        raise OCRUnavailableError(
            "The requested OCR language data is missing. Install the Tesseract language pack."
        ) from exc
