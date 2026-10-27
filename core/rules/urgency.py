import re
from .base import Rule
RULES=[Rule("urgency","urgency",re.compile(r"\b(urgent|immédiatement|dans les? \d+ minutes?|dernier avertissement|aujourd'hui seulement|agissez maintenant|expire aujourd'hui|act now|within \d+ hours?|final warning|عاجل|فوراً|تحرك الآن)\b",re.I),
{"fr":"Urgence artificielle","en":"Artificial urgency","ar":"استعجال مصطنع"},
{"fr":"Le message impose un délai court. La pression peut empêcher de vérifier calmement.","en":"A short deadline can pressure you into acting before checking.","ar":"قد تدفع المهلة القصيرة إلى التصرف قبل التحقق."},
{"fr":"Vérifiez par un canal officiel indépendant, sans utiliser les liens du message.","en":"Verify through an independent official channel, not message links.","ar":"تحقق عبر قناة رسمية مستقلة ولا تستخدم روابط الرسالة."},"high")]
