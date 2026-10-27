"""Evaluate the fixed, synthetic message corpus; this is not a real-world accuracy estimate."""
import json
from pathlib import Path
from core.detector import analyze_message

CASES = json.loads((Path(__file__).parent / "fixtures" / "messages.json").read_text(encoding="utf-8"))

def main():
    tp = fp = tn = fn = 0
    by_language = {}
    for case in CASES:
        lang = "ar" if case["language"] == "ar-DZ" else case["language"]
        report = analyze_message(case["text"], lang)
        predicted = bool(report["findings"])
        actual = case["label"] == "suspicious"
        tp += actual and predicted
        fp += (not actual) and predicted
        tn += (not actual) and (not predicted)
        fn += actual and (not predicted)
        row = by_language.setdefault(case["language"], {"tp":0,"fp":0,"tn":0,"fn":0})
        key = "tp" if actual and predicted else "fn" if actual else "fp" if predicted else "tn"
        row[key] += 1
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    specificity = tn / (tn + fp) if tn + fp else 0
    print("SYNTHETIC FIXED-CORPUS METRICS — not a real-world accuracy claim")
    print(f"Total={len(CASES)} TP={tp} FP={fp} TN={tn} FN={fn}")
    print(f"Precision={precision:.1%} Recall={recall:.1%} Specificity={specificity:.1%}")
    for lang, counts in sorted(by_language.items()):
        print(f"{lang}: {counts}")
    if fp:
        print("False positives:")
        for case in CASES:
            if case["label"] == "benign":
                lang = "ar" if case["language"] == "ar-DZ" else case["language"]
                if analyze_message(case["text"], lang)["findings"]:
                    print(f'  {case["id"]}: {case["text"]}')
    if fn:
        print("False negatives:")
        for case in CASES:
            if case["label"] == "suspicious":
                lang = "ar" if case["language"] == "ar-DZ" else case["language"]
                if not analyze_message(case["text"], lang)["findings"]:
                    print(f'  {case["id"]}: {case["text"]}')

if __name__ == "__main__":
    main()
