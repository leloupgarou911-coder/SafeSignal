from .rules.urgency import RULES as URGENCY
from .rules.reward import RULES as REWARD
from .rules.links import RULES as LINKS
from .rules.sensitive_data import RULES as DATA
from .rules.pressure import RULES as PRESSURE
from .rules.formatting import RULES as FORMATTING
from .rules.regional import RULES as REGIONAL
from .rules.financial_indicators import RULES as FINANCIAL
from .rules.social_engineering import RULES as SOCIAL_ENGINEERING
from .rules.domain_similarity import analyze_suspicious_domains

# Ajouter une famille de règles ici sans modifier l'algorithme d'analyse.
RULES = (
    # Do not flag an organization name alone; contextual impersonation rules
    # live in social_engineering.py and require an associated suspicious action.
    URGENCY + REWARD + LINKS + DATA + PRESSURE + FORMATTING
    + REGIONAL + FINANCIAL + SOCIAL_ENGINEERING
)

# A local brand name alone is not a warning sign. Require a social-engineering cue.
import re
REGIONAL_RISK_CUE = re.compile(
    r"(urgent|immediately|verify|verification|confirm|blocked|suspend|suspended|"
    r"click|pay now|payment required|code|otp|mot de passe|confirmez|confirmer|"
    r"bloqu[eé]|suspendu|vérifi|verifi|cliquez|payer|paiement|code secret|"
    r"رمز|تحقق|أكد|تأكيد|موقوف|محظور|مغلق|عاجل|اضغط|ادفع|دفع|كلمة السر|"
    r"compte.{0,20}(?:bloqu|suspend)|account.{0,20}(?:blocked|suspended))",
    re.I,
)


def analyze_message(text: str, language: str = "fr", custom_rules=None) -> dict:
    """Apply transparent rules. 'language' controls report translations, not detection."""
    language = language if language in {"fr", "en", "ar"} else "fr"
    findings = []
    normalized_text = text.casefold()
    # Custom rules are supplied by the UI/storage layer so the detector remains
    # usable in tests and command-line contexts without requiring a database.
    for custom_rule in custom_rules or ():
        try:
            rule_id, keyword, label, explanation = custom_rule
        except (TypeError, ValueError):
            continue
        keyword = str(keyword).strip()
        if keyword and keyword.casefold() in normalized_text:
            findings.append({
                "rule_id": f"custom_rule_{rule_id}",
                "category": "custom",
                "title": str(label),
                "explanation": (
                    f"Mot-clé personnalisé détecté (« {keyword} ») : {explanation}"
                    if language == "fr" else
                    f"Custom keyword detected (“{keyword}”): {explanation}"
                    if language == "en" else
                    f"تم اكتشاف كلمة مخصصة (« {keyword} »): {explanation}"
                ),
                "advice": {
                    "fr": "Vérifiez ce signal avec une source indépendante avant d'agir.",
                    "en": "Verify this signal independently before taking action.",
                    "ar": "تحقق من هذا المؤشر عبر مصدر مستقل قبل اتخاذ أي إجراء.",
                }[language],
                "severity": "low",
                "confidence": "low",
                "evidence": "« " + keyword[:100] + " »",
            })
    # Local domain lookalike checks; no DNS lookup or network request is made.
    findings.extend(analyze_suspicious_domains(text, language))
    for rule in RULES:
        match = rule.pattern.search(text)
        if match:
            if rule.id == "regional_payment_impersonation" and not REGIONAL_RISK_CUE.search(text):
                continue
            findings.append({
                "rule_id": rule.id,
                "category": rule.category,
                "title": rule.title[language],
                "explanation": rule.explanation[language],
                "advice": rule.advice[language],
                "severity": rule.severity,
                # Confidence describes a pattern match, not probability of fraud.
                "confidence": "low" if rule.severity == "low" else "medium",
                "evidence": "« " + match.group(0)[:100] + " »",
            })
    tips = {
        "fr": ["Ne cliquez pas et ne payez pas dans la précipitation.", "Vérifiez via un canal officiel que vous trouvez vous-même.", "Ne partagez ni mot de passe, ni code de validation, ni données bancaires."],
        "en": ["Do not click or pay in a hurry.", "Verify through an official channel you find independently.", "Never share passwords, verification codes, or banking details."],
        "ar": ["لا تنقر ولا تدفع على عجل.", "تحقق عبر قناة رسمية تجدها بنفسك.", "لا تشارك كلمات المرور أو رموز التحقق أو البيانات المصرفية."],
    }
    return {"language": language, "findings": findings, "general_advice": tips[language], "rule_count": len(RULES)}
