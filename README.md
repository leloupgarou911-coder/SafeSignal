# SafeSignal 🛡️

SafeSignal est une application Streamlit qui analyse localement des SMS, e-mails et messages copiés-collés afin d'expliquer les indices pouvant évoquer une arnaque. Elle ne rend jamais un verdict définitif.

## Fonctionnalités V1
- Moteur local et explicable, sans API externe obligatoire.
- Règles modulaires : urgence, récompense inattendue, liens raccourcis/présents, données sensibles, organismes connus, menaces/pression, typographie inhabituelle, services de paiement locaux (ex. BaridiMob/Edahabia/CCP) et frais de livraison suspects.
- Interface et fiches pédagogiques en français, anglais et arabe.
- Historique SQLite désactivé par défaut ; le texte original n'est stocké qu'après consentement explicite.
- Historique effaçable et tests automatisés.

## Prérequis et lancement
Python 3.11+ et pip.

1. Clonez le dépôt puis entrez dans le dossier SafeSignal.
2. Créez un environnement virtuel : \`python -m venv .venv\`
3. Activez-le : Windows PowerShell \`.\\.venv\\Scripts\\Activate.ps1\`, Linux/macOS \`source .venv/bin/activate\`.
4. Installez les dépendances : \`python -m pip install -r requirements.txt\`
5. Lancez : \`streamlit run app.py\`

## Tests
Exécutez à la racine : \`python -m unittest discover -s tests -v\`

## Structure
- \`app.py\` : interface Streamlit
- \`core/detector.py\` : orchestration des règles
- \`core/rules/\` : règles séparées par catégorie
- \`core/language.py\` : détection de langue heuristique
- \`core/explain.py\` : bibliothèque pédagogique
- \`i18n/\` : textes d'interface JSON
- \`db/\` : schéma et persistance SQLite
- \`tests/\` : tests unitaires

## Ajouter une règle
Créez un fichier dans \`core/rules/\` avec une liste \`RULES\` d'objets \`Rule\` (définis dans \`core/rules/base.py\`). Fournissez un identifiant, catégorie, regex compilée, titres, explications et conseils pour fr/en/ar, ainsi qu'une sévérité low/medium/high. Importez ensuite cette liste et ajoutez-la à \`RULES\` dans \`core/detector.py\`. Ajoutez un test et exécutez la suite.

## Ajouter une langue
Créez \`i18n/<code>.json\`, traduisez toutes les chaînes, ajoutez le libellé dans \`LANGS\` au début de \`app.py\`, puis complétez la langue dans chaque règle et dans \`core/explain.py\`. Ajoutez des tests. La détection de langue actuelle est lexicale et peut se tromper ; une bibliothèque locale peut la remplacer.

## Confidentialité et limites
Le moteur n'envoie aucun texte sur Internet et n'ouvre pas les liens. Si la case d'historique est cochée, le rapport et le texte original sont écrits dans \`db/safesignal.sqlite3\` sur la machine qui exécute l'application. Ne l'activez pas pour des messages que vous ne souhaitez pas conserver. La suppression efface les lignes de cette base applicative, pas d'éventuelles sauvegardes système.

La détection repose sur des motifs textuels et peut manquer des variantes, de l'argot ou des tentatives nouvelles. La mention d'une marque n'indique pas qu'elle est usurpée. Aucun DNS, certificat ou service de réputation n'est interrogé. La détection linguistique est simplifiée ; l'analyse de fautes d'orthographe n'est pas encore implémentée. Un signal n'est pas une preuve : une arnaque peut passer inaperçue et un message légitime peut déclencher une alerte. En cas de doute, contactez l'organisme par un canal officiel trouvé indépendamment.
