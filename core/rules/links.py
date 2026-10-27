import re
from .base import Rule
RULES=[
Rule("short_link","links",re.compile(r"(?i)\b(?:bit\.ly|tinyurl\.com|t\.co|is\.gd|cutt\.ly|rb\.gy)/?\S*"),
{"fr":"Lien raccourci","en":"Shortened link","ar":"رابط مختصر"},
{"fr":"Le raccourcisseur masque la destination finale. Ce n’est pas une preuve, mais la destination est moins visible.","en":"A shortener hides the destination. This is not proof of fraud, but the destination is less visible.","ar":"يخفي الرابط المختصر وجهته. هذا ليس دليلاً قاطعاً لكنه يقلل وضوح الوجهة."},
{"fr":"N’ouvrez pas le lien ; saisissez vous-même l’adresse officielle.","en":"Avoid opening it; type the official address yourself.","ar":"لا تفتح الرابط واكتب العنوان الرسمي بنفسك."},"high"),
Rule("url_present","links",re.compile(r"(?:https?://|www\.)[^\s<>]+",re.I),
{"fr":"Lien présent","en":"Link present","ar":"رابط موجود"},
{"fr":"Un lien peut être légitime ou malveillant. L’application ne l’ouvre pas et ne vérifie pas sa réputation.","en":"A link can be legitimate or malicious. This app does not open it or check its reputation.","ar":"قد يكون الرابط سليماً أو ضاراً. لا يفتحه التطبيق ولا يتحقق من سمعته."},
{"fr":"Vérifiez le domaine et préférez le site officiel connu.","en":"Check the domain and prefer the known official site.","ar":"تحقق من النطاق واستخدم الموقع الرسمي المعروف."},"medium")]
