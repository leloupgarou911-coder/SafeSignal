"""Détection de langue locale et heuristique (aucun appel réseau).

Le résultat reste une estimation : les messages courts, multilingues ou en dialecte
peuvent être mal classés. Le script arabe est un indice fort, pas une preuve.
"""
import re
from collections import Counter

ARABIC_SCRIPT = re.compile(r"[\u0600-\u06FF]")
TOKENS = {
    "fr": set("""le la les un une des du de et est votre vos vous urgent cliquez compte livraison cadeau gagné gagnez banque paiement colis remboursement amende vérifier vérifiez mot passe confirmer confirmez facture sécurité immédiatement bonjour merci svp svp veuillez votre compte bloqué poste algérie algerie baridimob edahabia ccp""".split()),
    "en": set("""the a an and is your you urgent click account delivery gift prize winner bank payment parcel refund fine verify password confirm invoice security immediately hello please suspended claim free update""".split()),
    "ar": set("""من في على إلى الى هذا هذه حساب عاجل اضغط تحقق كلمة المرور رمز البنك جائزة هدية ربح فزت ربحت مبروك توصيل طرد بريد الجزائر بريدي موب الذهبية الحساب غرامة دفع الآن فوراً مجانا مجاني تحديث تأكيد""".split()),
}
def detect_language(text: str) -> str:
    """Return fr/en/ar using script and vocabulary clues; default to French if uncertain."""
    if not text or not text.strip():
        return "fr"
    if ARABIC_SCRIPT.search(text):
        return "ar"
    words = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]+", text.casefold())
    if not words:
        return "fr"
    counts = Counter()
    for word in words:
        for language in ("fr", "en"):
            if word in TOKENS[language]:
                counts[language] += 1
    # Local French/Algerian vocabulary is explicitly represented in the French lexicon.
    if counts["fr"] == counts["en"] == 0:
        return "fr"
    return "fr" if counts["fr"] >= counts["en"] else "en"
