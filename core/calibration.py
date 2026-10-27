"""Transparent evaluation against SafeSignal's fixed synthetic message corpus.

These metrics describe only the checked-in examples, not real-world performance.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from core.detector import analyze_message

FIXTURE_PATH = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "messages.json"


def evaluate_synthetic_corpus(cases: Iterable[dict] | None = None) -> dict:
    """Return aggregate and per-language confusion-matrix metrics."""
    if cases is None:
        cases = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    totals = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}
    per_language: dict[str, dict[str, int]] = {}
    count = 0
    for case in cases:
        language = "ar" if case["language"] == "ar-DZ" else case["language"]
        actual_suspicious = case["label"] == "suspicious"
        predicted_suspicious = bool(analyze_message(case["text"], language)["findings"])
        key = (
            "tp" if actual_suspicious and predicted_suspicious
            else "fn" if actual_suspicious
            else "fp" if predicted_suspicious
            else "tn"
        )
        totals[key] += 1
        per_language.setdefault(case["language"], {"tp": 0, "fp": 0, "tn": 0, "fn": 0})[key] += 1
        count += 1

    def ratio(numerator: int, denominator: int) -> float | None:
        return numerator / denominator if denominator else None

    return {
        "total": count,
        **totals,
        "precision": ratio(totals["tp"], totals["tp"] + totals["fp"]),
        "recall": ratio(totals["tp"], totals["tp"] + totals["fn"]),
        "specificity": ratio(totals["tn"], totals["tn"] + totals["fp"]),
        "by_language": {
            language: {
                **counts,
                "precision": ratio(counts["tp"], counts["tp"] + counts["fp"]),
                "recall": ratio(counts["tp"], counts["tp"] + counts["fn"]),
                "specificity": ratio(counts["tn"], counts["tn"] + counts["fp"]),
            }
            for language, counts in sorted(per_language.items())
        },
    }
