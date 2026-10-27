"""Context-aware indicators for fake tech support and authority impersonation.

Brand or organization names alone are not suspicious. Each rule requires a second
social-engineering cue such as a claimed problem, fee, urgent action, or payment.
"""
import re

from .base import Rule

TECH_SUPPORT = re.compile(
    r"(?is)(?=.*(?:virus|support technique|assistance technique|ordinateur infecté|"
    r"ordinateur bloque|ordinateur bloqué|appareil infecté|numéro vert|"
    r"tech support|technical support|infected computer|computer is locked|"
    r"device is infected|call support|call this number|remote access|"
    r"virus|دعم فني|فيروس|جهاز مخترق|حاسوب مصاب|اتصل بالدعم|رقم الدعم))"
    r"(?=.*(?:appelez|appeler|téléphonez|contactez|bloqué|bloqué|infecté|"
    r"call now|call immediately|call this number|contact support|pay|payment|"
    r"download|install|remote access|blocked|infected|"
    r"اتصل|اتصل الآن|ادفع|دفع|مخترق|مصاب|محظور|مغلق)).+",
    re.I,
)

OFFICIAL_IMPERSONATION = re.compile(
    r"(?is)(?=.*(?:colis|livraison|frais de douane|amende|impôts|impot|"
    r"administration|banque|compte bancaire|organisme officiel|"
    r"package|parcel|delivery|customs fee|unpaid fine|tax(?:es)?|bank account|"
    r"government|official agency|"
    r"طرد|توصيل|رسوم الجمارك|غرامة|الضرائب|البنك|حساب بنكي|جهة رسمية))"
    r"(?=.*(?:payez|payer|régler|frais|impayé|impayée|suspendu|bloqué|"
    r"cliquez|vérifiez|confirmez|paiement|pay now|pay immediately|fee|"
    r"payment|unpaid|suspended|blocked|click here|verify now|confirm now|"
    r"ادفع|دفع|رسوم|غير مسدد|موقوف|محظور|اضغط|تحقق|أكد|تأكيد)).+",
    re.I,
)

RULES = [
    Rule(
        "fake_tech_support",
        "tech_support",
        TECH_SUPPORT,
        {
            "fr": "Possible faux support technique",
            "en": "Possible fake technical support",
            "ar": "احتمال وجود دعم فني وهمي",
        },
        {
            "fr": "Le message associe un problème technique à une action demandée. Des fraudeurs utilisent parfois de fausses alertes pour pousser à appeler, payer ou installer un logiciel. Ce signal seul ne prouve pas une fraude.",
            "en": "The message combines a technical problem with a requested action. Scammers sometimes use fake alerts to pressure people into calling, paying, or installing software. This signal alone does not prove fraud.",
            "ar": "تربط الرسالة مشكلة تقنية بإجراء مطلوب. قد يستخدم المحتالون تنبيهات مزيفة لدفع الأشخاص إلى الاتصال أو الدفع أو تثبيت برنامج. هذا المؤشر وحده لا يثبت الاحتيال.",
        },
        {
            "fr": "Ne téléphonez pas au numéro du message et n’installez aucun outil d’accès à distance. Contactez le fabricant depuis son site officiel.",
            "en": "Do not call the number in the message or install remote-access tools. Contact the vendor through its official website.",
            "ar": "لا تتصل بالرقم الوارد في الرسالة ولا تثبّت أدوات التحكم عن بُعد. تواصل مع الشركة عبر موقعها الرسمي.",
        },
        "high",
    ),
    Rule(
        "official_impersonation_request",
        "impersonation",
        OFFICIAL_IMPERSONATION,
        {
            "fr": "Possible usurpation d’un organisme ou service",
            "en": "Possible impersonation of an organization or service",
            "ar": "احتمال انتحال صفة مؤسسة أو خدمة",
        },
        {
            "fr": "Le message associe un organisme, un colis, une banque ou une administration à une demande de paiement, de vérification ou à une menace. Vérifiez indépendamment : la mention seule ne prouve pas une usurpation.",
            "en": "The message links an organization, parcel, bank, or authority to a payment, verification request, or threat. Verify independently: a mention alone does not prove impersonation.",
            "ar": "تربط الرسالة مؤسسة أو طرداً أو بنكاً أو جهة رسمية بطلب دفع أو تحقق أو تهديد. تحقق بشكل مستقل؛ فالذكر وحده لا يثبت الانتحال.",
        },
        {
            "fr": "N’utilisez pas le lien reçu. Ouvrez vous-même l’application ou le site officiel, ou contactez le service avec des coordonnées vérifiées.",
            "en": "Do not use the message link. Open the official app or website yourself, or contact the service using independently verified details.",
            "ar": "لا تستخدم الرابط الوارد. افتح التطبيق أو الموقع الرسمي بنفسك، أو تواصل مع الخدمة عبر بيانات اتصال موثوقة.",
        },
        "high",
    ),
]
