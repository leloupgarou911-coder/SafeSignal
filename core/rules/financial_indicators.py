"""Financial and identifier patterns that warrant careful verification.

A match is only a clue. These patterns do not establish that a message is fraudulent.
"""
import re

from .base import Rule

# Bitcoin legacy/SegWit and Ethereum address-shaped strings. Deliberately avoid
# validating checksum/network rules: this is a warning heuristic, not a wallet parser.
CRYPTO_ADDRESS = re.compile(
    r"(?<![A-Za-z0-9])(?:"
    r"bc1[ac-hj-np-z02-9]{11,71}|"
    r"[13][a-km-zA-HJ-NP-Z1-9]{25,34}|"
    r"0x[a-fA-F0-9]{40}"
    r")(?![A-Za-z0-9])",
    re.IGNORECASE,
)

MONEY_REQUEST = re.compile(
    r"(?<!\w)(?:"
    r"virement(?:\s bancaire)?|rib|iban|western\s+union|"
    r"envoyez?\s+(?:de\s+)?l['’]?argent|transférez?\s+(?:de\s+)?l['’]?argent|"
    r"frais\s+(?:de\s+)?dossier|payer\s+(?:maintenant|des\s+frais)|"
    r"wire\s+transfer|bank\s+transfer|send\s+money|money\s+transfer|"
    r"payment\s+required|pay\s+(?:now|a\s+fee)|credit\s+card|"
    r"تحويل(?:\s+بنكي)?|حساب\s+بنكي|أرسل\s+المال|ارسل\s+المال|"
    r"ادفع\s+الآن|رسوم\s+الملف|بيتكوين|عملات\s+رقمية"
    r")(?!\w)",
    re.IGNORECASE,
)

# 13–19 digits, optionally separated by spaces/hyphens, can resemble a card or
# account identifier. It may also be a legitimate reference number.
LONG_NUMBER = re.compile(r"(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)")

RULES = [
    Rule(
        "crypto_address",
        "financial",
        CRYPTO_ADDRESS,
        {
            "fr": "Adresse de cryptomonnaie détectée",
            "en": "Cryptocurrency address detected",
            "ar": "تم اكتشاف عنوان عملة رقمية",
        },
        {
            "fr": "Le message contient une chaîne qui ressemble à une adresse de portefeuille crypto. Cela ne prouve pas une arnaque, mais les transferts peuvent être difficiles à annuler.",
            "en": "The message contains a string resembling a crypto wallet address. This does not prove fraud, but transfers can be difficult to reverse.",
            "ar": "تحتوي الرسالة على نص يشبه عنوان محفظة رقمية. هذا لا يثبت الاحتيال، لكن قد يصعب إلغاء التحويلات.",
        },
        {
            "fr": "Ne transférez rien avant d’avoir vérifié indépendamment le destinataire et la demande.",
            "en": "Do not transfer funds until you independently verify the recipient and request.",
            "ar": "لا تحوّل الأموال قبل التحقق بشكل مستقل من المستلم والطلب.",
        },
        "medium",
    ),
    Rule(
        "money_request",
        "financial",
        MONEY_REQUEST,
        {
            "fr": "Demande ou référence financière",
            "en": "Financial request or reference",
            "ar": "طلب أو إشارة مالية",
        },
        {
            "fr": "Le texte mentionne un moyen de paiement, un transfert ou une demande d’argent. Ce contexte peut être légitime ; vérifiez surtout l’identité et le motif.",
            "en": "The text mentions a payment method, transfer, or request for money. This can be legitimate; verify the sender and reason.",
            "ar": "تذكر الرسالة وسيلة دفع أو تحويلاً أو طلباً للمال. قد يكون ذلك مشروعاً؛ تحقق من هوية المرسل والسبب.",
        },
        {
            "fr": "Confirmez la demande auprès du destinataire par un canal officiel indépendant avant tout paiement.",
            "en": "Confirm the request with the recipient through an independent official channel before paying.",
            "ar": "تأكد من الطلب عبر قناة رسمية مستقلة قبل الدفع.",
        },
        "medium",
    ),
    Rule(
        "long_number",
        "sensitive_data",
        LONG_NUMBER,
        {
            "fr": "Longue suite de chiffres à vérifier",
            "en": "Long number sequence to verify",
            "ar": "تسلسل رقمي طويل يستحق التحقق",
        },
        {
            "fr": "Une longue suite de chiffres peut ressembler à un numéro de carte ou à un identifiant. Il peut aussi s’agir d’une référence ordinaire : le contexte compte.",
            "en": "A long digit sequence may resemble a card number or identifier. It may also be an ordinary reference number; context matters.",
            "ar": "قد يشبه تسلسل الأرقام الطويل رقم بطاقة أو معرّفاً، وقد يكون أيضاً رقم مرجع عادي؛ السياق مهم.",
        },
        {
            "fr": "Évitez de partager publiquement des numéros de carte, codes ou identifiants personnels.",
            "en": "Avoid publicly sharing card numbers, codes, or personal identifiers.",
            "ar": "تجنب نشر أرقام البطاقات أو الرموز أو المعرّفات الشخصية علناً.",
        },
        "low",
    ),
]
