"""Local, conservative checks for lookalike domains in message text.

This module never resolves DNS, opens a URL, or sends text to a third party.
The small trusted-domain list is illustrative and should be maintained carefully.
"""
import re
from urllib.parse import urlsplit


# Unicode confusables commonly used to imitate Latin letters. Deliberately limited:
# transliterating all Unicode would create too many false positives.
_CONFUSABLES = str.maketrans({
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "х": "x",
    "у": "y", "і": "i", "ј": "j", "к": "k", "м": "m", "т": "t",
    "в": "b", "н": "h", "ѕ": "s", "ԁ": "d", "ɡ": "g",
    "Α": "a", "Β": "b", "Ε": "e", "Ζ": "z", "Η": "h", "Ι": "i",
    "Κ": "k", "Μ": "m", "Ν": "n", "Ο": "o", "Ρ": "p", "Τ": "t",
    "Υ": "y", "Χ": "x",
})

# A deliberately short starter list, not an authoritative registry.
TRUSTED_DOMAINS = {
    "baridimob.dz",
    "poste.dz",
    "edahabia.poste.dz",
}

_URL_RE = re.compile(r"""(?i)(?:https?://|www\.)[^\s<>"']+|(?<![\w@])(?:[a-z0-9\u0080-\uffff-]+\.)+[a-z\u0080-\uffff]{2,}(?:/[^\s<>"']*)?""")


def _host_from_candidate(candidate: str) -> str:
    candidate = candidate.strip(".,;:!?)]}»”’")
    if candidate.lower().startswith("www."):
        candidate = "http://" + candidate
    elif "://" not in candidate:
        candidate = "http://" + candidate
    try:
        host = urlsplit(candidate).hostname or ""
    except ValueError:
        return ""
    return host.rstrip(".").lower()


def _levenshtein_at_most_one(left: str, right: str) -> bool:
    """Return whether two strings differ by at most one edit."""
    if left == right:
        return True
    if abs(len(left) - len(right)) > 1:
        return False
    if len(left) > len(right):
        left, right = right, left
    i = j = edits = 0
    while i < len(left) and j < len(right):
        if left[i] == right[j]:
            i += 1
            j += 1
            continue
        edits += 1
        if edits > 1:
            return False
        if len(left) == len(right):
            i += 1
        j += 1
    if i < len(left) or j < len(right):
        edits += 1
    return edits <= 1


def _domain_signal(host: str):
    if not host or host.startswith("[") or re.fullmatch(r"[0-9.]+", host):
        return None
    try:
        ascii_host = host.encode("idna").decode("ascii").lower()
    except UnicodeError:
        ascii_host = host.lower()
    # Normalize confusables only for comparison; preserve the original evidence.
    normalized = ascii_host.translate(_CONFUSABLES).lower()
    trusted = sorted(TRUSTED_DOMAINS, key=len, reverse=True)
    for official in trusted:
        official_root = official.split(".")[0]
        host_labels = normalized.split(".")
        root_labels = [label for label in host_labels if label]
        # Exact official domain is not suspicious.
        if ascii_host == official:
            continue
        # A near-match to a known service label is a clue, not a verdict.
        for label in root_labels[:-1]:
            if label == official_root:
                return ("domain_suffix_mismatch", official)
            if len(label) >= 6 and _levenshtein_at_most_one(label, official_root):
                return ("lookalike_domain", official)
        # Catch confusable spelling even when IDNA encoded it.
        raw_normalized = host.translate(_CONFUSABLES).lower()
        if raw_normalized != host and official_root in raw_normalized.replace(".", ""):
            return ("homoglyph_domain", official)
    return None


def _finding(rule_id, language, evidence, official):
    titles = {
        "lookalike_domain": {"fr": "Domaine ressemblant à un domaine connu", "en": "Lookalike domain", "ar": "نطاق يشبه نطاقاً معروفاً"},
        "homoglyph_domain": {"fr": "Caractères ressemblants dans le domaine", "en": "Lookalike characters in domain", "ar": "أحرف متشابهة في النطاق"},
        "domain_suffix_mismatch": {"fr": "Extension de domaine inhabituelle", "en": "Unusual domain ending", "ar": "امتداد نطاق غير معتاد"},
    }
    explanations = {
        "fr": f"Le domaine ressemble à un domaine de référence ({official}), mais une différence a été détectée. Cela mérite une vérification indépendante et ne prouve pas une fraude.",
        "en": f"The domain resembles a reference domain ({official}), but a difference was detected. Verify it independently; this alone does not prove fraud.",
        "ar": f"يشبه النطاق نطاقاً مرجعياً ({official}) لكن توجد اختلافات. تحقق منه بشكل مستقل؛ فهذا وحده لا يثبت الاحتيال.",
    }
    advice = {
        "fr": "N'ouvrez pas le lien depuis le message. Saisissez vous-même l'adresse officielle connue.",
        "en": "Do not open the link from the message. Type the known official address yourself.",
        "ar": "لا تفتح الرابط من الرسالة. اكتب العنوان الرسمي المعروف بنفسك.",
    }
    return {
        "rule_id": rule_id,
        "category": "links",
        "title": titles[rule_id][language],
        "explanation": explanations[language],
        "advice": advice[language],
        "severity": "medium",
        "confidence": "low",
        "evidence": "« " + evidence[:100] + " »",
    }


def analyze_suspicious_domains(text: str, language: str = "fr") -> list[dict]:
    """Return conservative local lookalike-domain findings."""
    language = language if language in {"fr", "en", "ar"} else "fr"
    findings = []
    seen = set()
    for match in _URL_RE.finditer(text):
        candidate = match.group(0)
        host = _host_from_candidate(candidate)
        signal = _domain_signal(host)
        if not signal:
            continue
        rule_id, official = signal
        key = (rule_id, host)
        if key in seen:
            continue
        seen.add(key)
        findings.append(_finding(rule_id, language, candidate, official))
    return findings

