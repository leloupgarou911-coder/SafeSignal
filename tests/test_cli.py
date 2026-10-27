import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def run_cli(self, *args, input_text=None):
        return subprocess.run(
            [sys.executable, "-m", "safesignal", *args],
            cwd=ROOT,
            input=input_text,
            text=True,
            capture_output=True,
            timeout=15,
            env={**os.environ, "PYTHONPATH": str(ROOT)},
            check=False,
        )

    def test_text_json_output(self):
        result = self.run_cli("--text", "URGENT act now", "--language", "en", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(report["findings"])
        self.assertEqual(report["language"], "en")

    def test_stdin_input(self):
        result = self.run_cli("--language", "fr", input_text="Bonjour, rendez-vous demain.")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Rappel", result.stdout)

    def test_empty_message_returns_friendly_error(self):
        result = self.run_cli("--text", "   ")
        self.assertEqual(result.returncode, 2)
        self.assertIn("vide", result.stderr.lower())

    def test_file_input(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "message.txt"
            path.write_text("URGENT act now", encoding="utf-8")
            result = self.run_cli("--file", str(path), "--language", "en", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["findings"])

    def test_missing_file_returns_error_without_traceback(self):
        result = self.run_cli("--file", str(ROOT / "does-not-exist.txt"))
        self.assertEqual(result.returncode, 2)
        self.assertIn("Impossible de lire le fichier", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
