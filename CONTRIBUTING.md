# Contribuer à SafeSignal

Merci de contribuer à SafeSignal. Le projet est un outil pédagogique : privilégiez des explications transparentes et évitez de présenter une détection comme une preuve de fraude.

## Préparer l'environnement

1. Installez Python 3.11 ou plus récent.
2. Clonez le dépôt et créez un environnement virtuel (voir le README).
3. Installez les dépendances avec `python -m pip install -r requirements.txt`.

## Avant d'envoyer une modification

- Ajoutez ou adaptez des tests pour chaque changement de comportement.
- Lancez `python -m unittest discover -s tests -v`.
- Si vous modifiez les règles, exécutez `python tests/evaluate_corpus.py` et vérifiez les faux positifs autant que les faux négatifs.
- Si vous touchez à l'interface, exécutez `python tests/browser_smoke.py` après avoir installé Playwright et Chromium.
- Gardez les trois traductions (`fr`, `en`, `ar`) synchronisées.
- N'ajoutez jamais de vrais messages contenant des noms, numéros, liens personnels, codes ou données bancaires. Utilisez des exemples synthétiques et anonymisés.
- Ne commitez ni fichier `.env`, ni base SQLite, ni données utilisateur, ni secrets.

## Ajouter une règle de détection

1. Ajoutez une règle ciblée dans le module approprié de `core/rules/`.
2. Expliquez ce qui a été repéré et fournissez un conseil prudent dans les trois langues.
3. Ajoutez des exemples suspects **et** des exemples légitimes proches dans `tests/fixtures/messages.json`.
4. Mesurez les faux positifs et faux négatifs avant d'élargir une expression régulière.
5. N'utilisez pas la seule mention d'une marque ou d'un service comme preuve d'usurpation.

## Pull requests

Décrivez le problème, les fichiers modifiés, les tests exécutés et les limites connues. Les changements importants de détection doivent inclure des exemples démontrant que les messages légitimes restent correctement traités.
