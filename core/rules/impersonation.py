import re
from .base import Rule
RULES=[Rule("organization_mentioned","impersonation",re.compile(r"\b(banque|impôts|administration|police|douane|colissimo|chronopost|laposte|paypal|microsoft|apple|bank|tax office|customs|delivery service|government|البنك|الضرائب|الجمارك|البريد|الشرطة|الإدارة)\b",re.I),
{"fr":"Organisme connu mentionné","en":"Known organization mentioned","ar":"ذُكرت مؤسسة معروفة"},
{"fr":"Des fraudeurs peuvent usurper une banque, une administration ou une marque. La mention seule ne prouve rien.","en":"Scammers may impersonate a bank, authority, or brand. Mention alone proves nothing.","ar":"قد ينتحل المحتالون صفة بنك أو إدارة أو علامة تجارية. ذكر الاسم وحده لا يثبت شيئاً."},
{"fr":"Vérifiez l’expéditeur et contactez l’organisme via son site officiel trouvé indépendamment.","en":"Check the sender and use the official website found independently.","ar":"تحقق من المرسل واتصل بالمؤسسة عبر موقعها الرسمي الذي تجده بنفسك."},"medium")]
