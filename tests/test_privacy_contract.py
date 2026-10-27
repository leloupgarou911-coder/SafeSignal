"""Privacy contract tests: no persistence without consent and no image storage."""
import json
import tempfile
import unittest
from pathlib import Path

from db import storage

class PrivacyContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        storage.DB_PATH = Path(self.tmp.name) / "safesignal.sqlite3"
        storage.init_db()
        self.report = {"findings": [], "language": "fr"}

    def tearDown(self):
        self.tmp.cleanup()

    def test_no_consent_does_not_persist_text_or_report(self):
        for consent in (False, None, 0):
            with self.subTest(consent=consent):
                self.assertFalse(storage.save_analysis(self.report, "PRIVATE MESSAGE", consent=consent))
        self.assertEqual(storage.list_history(), [])
        with storage._connect() as connection:
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM analyses").fetchone()[0], 0)

    def test_database_has_no_image_or_upload_column(self):
        with storage._connect() as connection:
            columns = {row["name"].casefold() for row in connection.execute("PRAGMA table_info(analyses)")}
        self.assertFalse(any(token in column for column in columns for token in ("image", "upload", "blob", "screenshot")))

    def test_explicit_consent_is_the_only_path_to_persist_message_text(self):
        self.assertTrue(storage.save_analysis(self.report, "CONSENTED MESSAGE", consent=True))
        rows = storage.list_history()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["original_text"], "CONSENTED MESSAGE")
        self.assertEqual(json.loads(rows[0]["report"]), self.report)

if __name__ == "__main__":
    unittest.main()
