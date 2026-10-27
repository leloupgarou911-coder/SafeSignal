import re
from .base import Rule
RULES=[Rule("sensitive_data","sensitive_data",re.compile(r"\b(mot de passe|code de vérification|code sms|numéro de carte|carte bancaire|cryptogramme|password|one[- ]time code|verification code|bank details|credit card|كلمة المرور|رمز التحقق|بطاقة بنكية)\b",re.I),
{"fr":"Données sensibles évoquées","en":"Sensitive data mentioned","ar":"ذُكرت بيانات حساسة"},
{"fr":"La demande évoque des identifiants, codes ou données financières. Les partager avec un contact non vérifié peut compromettre un compte.","en":"Credentials, codes, or financial details may compromise an account if shared with an unverified contact.","ar":"قد يؤدي مشاركة بيانات الدخول أو الرموز أو المعلومات المالية مع جهة غير موثوقة إلى اختراق الحساب."},
{"fr":"Ne communiquez jamais un mot de passe ou code à usage unique. Contactez l’organisme officiellement.","en":"Never share passwords or one-time codes. Contact the organization through official channels.","ar":"لا تشارك كلمة المرور أو رمز الاستخدام الواحد. تواصل عبر القنوات الرسمية."},"high")]
