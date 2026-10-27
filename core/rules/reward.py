import re
from .base import Rule
from .keyword_dictionary import keyword_pattern

_EXISTING_PATTERNS = r"\b(gagné|gagnez|vous avez gagné|lotterie|prix exclusif|cadeau gratuit|récompense|winner|you won|claim your prize|free gift|cash prize|congratulations|ربحت|مبروك|جائزة|هدية مجانية)\b"
PATTERN = re.compile(_EXISTING_PATTERNS + "|" + keyword_pattern("reward").pattern, re.I)

RULES = [Rule(
    "reward", "reward", PATTERN,
    {"fr": "Gain inattendu", "en": "Unexpected prize", "ar": "جائزة غير متوقعة"},
    {
        "fr": "Une récompense non sollicitée peut servir d’appât, surtout si elle exige un clic, un paiement ou des données.",
        "en": "An unsolicited reward can be bait, especially if it asks for clicks, payment, or data.",
        "ar": "قد تكون المكافأة غير المطلوبة طعماً إذا طلبت نقراً أو دفعاً أو بيانات."
    },
    {
        "fr": "Ne payez pas pour réclamer un gain inattendu. Vérifiez l’organisateur indépendamment.",
        "en": "Do not pay to claim a prize; verify the organizer independently.",
        "ar": "لا تدفع لاستلام جائزة وتحقق من الجهة المنظمة."
    },
    "medium"
)]
