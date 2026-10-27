import re
from .base import Rule
RULES=[Rule("odd_formatting","formatting",re.compile(r"(?:!!!+|\?{3,}|\b[A-ZÀÂÇÉÈÊËÎÏÔÛÙÜŸ]{5,}\b)"),
{"fr":"Mise en forme inhabituelle","en":"Unusual formatting","ar":"تنسيق غير معتاد"},
{"fr":"Majuscules insistantes ou ponctuation excessive peuvent chercher à capter l’attention. Signal faible seulement.","en":"Excessive capitals or punctuation may grab attention. This is only a weak signal.","ar":"قد تجذب الأحرف الكبيرة أو علامات الترقيم المفرطة الانتباه. إنها إشارة ضعيفة فقط."},
{"fr":"Cherchez d’autres indices ; la typographie seule ne suffit pas.","en":"Look for other clues; formatting alone is not enough.","ar":"ابحث عن مؤشرات أخرى؛ التنسيق وحده لا يكفي."},"low")]
