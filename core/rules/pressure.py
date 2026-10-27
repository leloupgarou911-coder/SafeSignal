import re
from .base import Rule
RULES=[Rule("threat","pressure",re.compile(r"\b(compte sera bloqué|compte sera suspendu|vous serez poursuivi|amende immédiate|sous peine de|suspended account|legal action|you will be fined|account will be closed|pay immediately|سيتم إيقاف حسابك|إجراء قانوني|غرامة|آخر إنذار)\b",re.I),
{"fr":"Menace ou pression","en":"Threat or pressure","ar":"تهديد أو ضغط"},
{"fr":"La peur d’une sanction peut pousser à agir sans vérifier. Le contexte reste important.","en":"Fear of a penalty can push people to act without checking; context matters.","ar":"قد يدفع الخوف من العقوبة إلى التصرف دون تحقق، ويبقى السياق مهماً."},
{"fr":"Ne répondez pas sous pression. Vérifiez directement auprès de l’organisme.","en":"Do not act under pressure; verify directly with the organization.","ar":"لا تتصرف تحت الضغط وتحقق مباشرة لدى المؤسسة."},"high")]
