"""Détection de langue heuristique, sans appel réseau."""
import re
AR=re.compile(r"[\u0600-\u06FF]")
FR=re.compile(r"\b(le|la|les|vous|votre|urgent|cliquez|compte|livraison|cadeau|gagné|gagnez|banque|paiement)\b",re.I)
EN=re.compile(r"\b(the|your|urgent|click|account|delivery|prize|winner|bank|payment|verify|password)\b",re.I)
def detect_language(text:str)->str:
 if AR.search(text): return "ar"
 f,e=len(FR.findall(text)),len(EN.findall(text))
 return "fr" if f>=e else "en"
