"""Dictionnaire multilingue de signaux lexicaux à intégrer aux règles explicables.

Les mots-clés sont des indices contextuels, jamais une preuve à eux seuls.
Ajoutez les termes par langue et catégorie sans modifier le moteur d'analyse.
"""
import re

SCAM_KEYWORDS = {
    "fr": {
        "urgency": [
            "immédiatement", "urgent", "dans les 24h", "dans les 24 heures",
            "dernière chance", "compte suspendu", "cliquez ici",
            "dernier délai", "agissez maintenant",
        ],
        "reward": [
            "gagné", "félicitations", "cadeau", "lot", "tirage au sort",
            "remboursement", "récompense", "cadeau gratuit", "prix exclusif",
        ],
    },
    "en": {
        "urgency": [
            "immediately", "urgent", "within 24 hours", "last chance",
            "account suspended", "click here", "act now", "final warning",
        ],
        "reward": [
            "won", "congratulations", "gift", "prize", "lottery", "refund",
            "free gift", "cash prize", "claim your prize",
        ],
    },
    "ar": {
        "urgency": [
            "عاجل", "فورا", "فوراً", "حالاً", "حساب موقوف",
            "الفرصة الأخيرة", "اضغط هنا", "آخر إنذار",
        ],
        "reward": [
            "مبروك", "ربحت", "جائزة", "هدية", "مسابقة",
            "هدية مجانية", "استرداد الأموال",
        ],
    },
}


def keyword_pattern(category: str) -> re.Pattern[str]:
    """Compile all supported language terms into one Unicode-aware regex."""
    terms = [
        term
        for language_rules in SCAM_KEYWORDS.values()
        for term in language_rules.get(category, [])
    ]
    alternatives = "|".join(re.escape(term) for term in sorted(set(terms), key=len, reverse=True))
    return re.compile(rf"(?<!\w)(?:{alternatives})(?!\w)", re.IGNORECASE)
