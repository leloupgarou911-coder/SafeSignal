import json
import tempfile
import unittest
from pathlib import Path

from db import storage


class StoragePrivacyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        storage.DB_PATH = Path(self.tmp.name) / "test.sqlite3"
        storage.init_db()
        self.report = {"findings": [{"title": "Test clue"}], "language": "fr"}

    def tearDown(self):
        self.tmp.cleanup()

    def test_no_consent_does_not_store_text_or_report(self):
        saved = storage.save_analysis(self.report, "PRIVATE TEST MESSAGE", consent=False)
        self.assertFalse(saved)
        self.assertEqual(storage.list_history(), [])
        with storage._connect() as conn:
            count = conn.execute("SELECT COUNT(*) FROM analyses").fetchone()[0]
        self.assertEqual(count, 0)

    def test_explicit_consent_stores_text_and_history_returns_it(self):
        saved = storage.save_analysis(self.report, "CONSENTED TEXT", consent=True)
        self.assertTrue(saved)
        with storage._connect() as conn:
            row = conn.execute("SELECT original_text, report FROM analyses").fetchone()
        self.assertEqual(row["original_text"], "CONSENTED TEXT")
        self.assertEqual(json.loads(row["report"]), self.report)

        history = storage.list_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["original_text"], "CONSENTED TEXT")
        self.assertEqual(json.loads(history[0]["report"]), self.report)

    def test_clear_history_removes_rows(self):
        storage.save_analysis(self.report, "CONSENTED TEXT", consent=True)
        storage.clear_history()
        self.assertEqual(storage.list_history(), [])


if __name__ == "__main__":
    unittest.main()
