"""Motifs régionaux utiles pour des messages ciblant notamment l'Algérie."""
import re
from .base import Rule

RULES = [
    Rule(
        "regional_payment_impersonation", "regional_impersonation",
        re.compile(r"\b(baridi\s?mob|baridimob|alg[eé]rie\s?poste|poste\s?alg[eé]rienne|edahabia|carte\s+edahabia|ccp|mobilis|djezzy|ooredoo|satim|cib)\b|بريدي\s?موب|الذهبية|بريد الجزائر", re.I),
        {"fr":"Service de paiement ou opérateur cité","en":"Payment service or carrier mentioned","ar":"ذُكرت خدمة دفع أو شركة اتصالات"},
        {"fr":"Des messages frauduleux peuvent reprendre le nom de services de paiement, de cartes ou d'opérateurs utilisés localement. La mention de ce nom ne prouve pas une usurpation.","en":"Fraudulent messages may reuse names of local payment services, cards, or mobile carriers. Mentioning a name does not prove impersonation.","ar":"قد تستخدم الرسائل الاحتيالية أسماء خدمات دفع أو بطاقات أو شركات اتصالات محلية. ذكر الاسم وحده لا يثبت انتحال الهوية."},
        {"fr":"Ne suivez pas le lien reçu. Ouvrez l'application ou le site officiel vous-même et ne partagez aucun code secret.","en":"Do not follow the received link. Open the official app or site yourself and never share secret codes.","ar":"لا تتبع الرابط المرسل. افتح التطبيق أو الموقع الرسمي بنفسك ولا تشارك الرموز السرية."},
        "medium"
    ),
    Rule(
        "delivery_fee", "delivery",
        re.compile(r"\b(frais de livraison|frais de douane|colis bloqu[eé]|confirmer l'adresse|petit paiement|delivery fee|customs fee|parcel on hold|confirm your address|رسوم التوصيل|رسوم جمركية|طردك متوقف|تأكيد العنوان)\b", re.I),
        {"fr":"Frais ou livraison à confirmer","en":"Delivery fee or address confirmation","ar":"رسوم توصيل أو تأكيد عنوان"},
        {"fr":"Les faux avis de livraison peuvent demander un petit paiement ou des données personnelles pour débloquer un colis. Un vrai transporteur peut aussi contacter ses clients : vérifiez le suivi indépendamment.","en":"Fake delivery notices may ask for a small fee or personal data to release a parcel. Real carriers also contact customers, so verify tracking independently.","ar":"قد تطلب رسائل التوصيل المزيفة مبلغاً صغيراً أو بيانات شخصية للإفراج عن طرد. وقد تتواصل شركات حقيقية أيضاً؛ تحقق من التتبع بشكل مستقل."},
        {"fr":"Consultez le suivi depuis le site officiel du transporteur, sans utiliser le lien du message.","en":"Check tracking on the carrier's official site without using the message link.","ar":"تحقق من التتبع عبر الموقع الرسمي لشركة التوصيل دون استخدام رابط الرسالة."},
        "medium"
    ),
]
