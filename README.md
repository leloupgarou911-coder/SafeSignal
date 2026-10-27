# SafeSignal 🛡️

[![SafeSignal checks](https://github.com/leloupgarou911-coder/SafeSignal/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/leloupgarou911-coder/SafeSignal/actions/workflows/tests.yml)

**SafeSignal est un outil pédagogique qui aide à examiner un SMS, un e-mail ou un message copié-collé en repérant des indices textuels associés à certaines arnaques.** Il explique les indices détectés ; il ne déclare jamais qu'un message est définitivement frauduleux ou sûr.

Interface disponible en français, anglais et arabe (avec mise en page RTL en arabe). Le moteur de règles fonctionne localement et ne nécessite aucune API externe.

## Aperçu visuel

Le workflow GitHub Actions exécute un test navigateur Chromium sur les trois langues et publie les captures d'écran sous l'artefact **`safesignal-streamlit-screenshots`** pour chaque exécution. Pour les consulter : ouvrez l'onglet [Actions](https://github.com/leloupgarou911-coder/SafeSignal/actions/workflows/tests.yml), choisissez une exécution terminée, puis téléchargez l'artefact. Les captures sont des preuves de rendu automatisé, pas une certification d'accessibilité.

## Accessibilité et navigation

- Les champs interactifs ont des libellés et des aides descriptives.
- Le lien « aller au contenu principal » permet de sauter les éléments de navigation.
- Les contrôles clavier disposent d’un indicateur de focus visible et contrasté ; les onglets peuvent être parcourus au clavier.
- Les textes secondaires et la bannière de confidentialité utilisent des couleurs vérifiées par des tests de contraste WCAG AA pour les combinaisons déclarées.
- Les tests navigateur contrôlent les noms accessibles des onglets, la navigation par flèches, la direction LTR/RTL et la disposition à 720, 375 et 320 pixels en français, anglais et arabe. Le test à 720 px simule une fenêtre CSS plus étroite comparable à un zoom important, sans remplacer un test de zoom réel.

Ces contrôles automatisés sont une base de régression, pas une certification complète WCAG. Le pipeline ne lance pas de lecteur d’écran : il vérifie des noms accessibles et la navigation clavier, mais une vérification manuelle avec NVDA ou Orca, un zoom réel à 200 % et un essai utilisateur restent nécessaires.

## Fonctionnalités

- Analyse locale par règles explicables : urgence, récompenses, liens, données sensibles, usurpation, pression, formatage et motifs régionaux.
- Prise en compte de formulations et services algériens comme BaridiMob, Edahabia, CCP et les frais de livraison suspects — leur simple mention ne prouve pas une fraude.
- Conseils pédagogiques en français, anglais et arabe.
- Historique SQLite local, désactivé par défaut ; le texte original n'est enregistré qu'avec consentement explicite.
- Suppression de l'historique.
- Corpus synthétique multilingue et calcul de faux positifs/faux négatifs pour aider à surveiller les régressions.
- Tests unitaires et contrôle navigateur automatisés sur GitHub Actions.

## Prérequis

- Python 3.11 ou plus récent
- pip
- Un navigateur moderne pour l'interface. Le navigateur Chromium de test est installé automatiquement par le workflow CI.

Aucune clé API ni variable d'environnement n'est requise pour la version actuelle.

## Installation locale

### Windows PowerShell

```powershell
git clone https://github.com/leloupgarou911-coder/SafeSignal.git
cd SafeSignal
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
streamlit run app.py
```

### Linux / macOS

```bash
git clone https://github.com/leloupgarou911-coder/SafeSignal.git
cd SafeSignal
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
streamlit run app.py
```

Streamlit affiche une adresse locale (généralement `http://localhost:8501`). Ouvrez-la dans votre navigateur. Pour arrêter le serveur, utilisez `Ctrl+C` dans le terminal.

## Utilisation en ligne de commande

Après l'installation en mode éditable (`python -m pip install -e .`), analysez un message depuis le terminal :

```bash
python -m safesignal --text "URGENT: verify your account now" --language en
```

Vous pouvez aussi utiliser `python -m safesignal --file message.txt`, transmettre un fichier via l'entrée standard (`cat message.txt | python -m safesignal`), ou demander du JSON avec `--json`. La commande `safesignal --help` liste les options. `--verbose` active les journaux de diagnostic. Le code de sortie est non nul si l'entrée est invalide ou si une erreur empêche l'analyse.

Pour déplacer la base SQLite, définissez `SAFESIGNAL_DB_PATH` avant de lancer l'application. Aucun secret ou service distant n'est nécessaire.

## Utilisation hors ligne et données

Après l'installation des dépendances, le moteur d'analyse ne fait aucun appel réseau externe et peut analyser des messages sans connexion Internet, tant que l'application Streamlit locale est démarrée. Il ne s'agit pas d'une application mobile avec une file d'envoi différé : SafeSignal analyse le texte présent dans la session et ne transmet pas de signalement à un service distant.

L'historique est conservé dans `db/safesignal.sqlite3` sur la machine qui exécute SafeSignal. Il est désactivé par défaut. Si vous activez la case d'enregistrement, le rapport et le texte original sont stockés localement. Ne l'activez pas pour des messages que vous ne souhaitez pas conserver. La suppression vide les entrées de la base applicative, mais ne supprime pas d'éventuelles sauvegardes système.

Les captures d’écran envoyées à l’outil OCR sont traitées en mémoire par l’instance SafeSignal qui exécute l’application ; elles ne sont pas ajoutées à la base SQLite et aucun fichier image n’est écrit par le module OCR. Comme toute application web, l’instance reçoit temporairement le fichier pendant le traitement et la session Streamlit peut conserver temporairement le téléversement ou le texte extrait en mémoire. Cela n’équivaut pas à une conservation permanente ; si l’application est hébergée sur un serveur distant, l’image transite vers ce serveur. N’utilisez pas une instance hébergée dont vous ne connaissez pas l’exploitant pour des messages ou images confidentiels. Les boutons « Réinitialiser » suppriment le texte et le rapport de l’état de session affiché et recréent le composant de téléversement OCR ; ils ne peuvent toutefois pas garantir l’effacement physique instantané de toutes les copies temporaires gérées par le navigateur, Python ou le système d’exploitation. Le test de confidentialité distingue donc explicitement la présence temporaire en mémoire de l’écriture persistante dans SQLite ou dans un fichier.

## Vérifications et tests

Tests unitaires :

```bash
python -m unittest discover -s tests -v
```

Évaluation du corpus synthétique :

```bash
python tests/evaluate_corpus.py
```

Test de rendu navigateur (nécessite Playwright et Chromium) :

```bash
python -m pip install playwright
python -m playwright install chromium
python tests/browser_smoke.py
```

Le corpus synthétique comporte maintenant davantage de messages légitimes (dont des mentions ordinaires de marques, banques et colis) et suspects en français, anglais et arabe algérien. Les métriques servent à comparer les changements sur ces exemples seulement ; elles **ne représentent pas la précision réelle** sur les messages reçus dans la vie quotidienne. Chaque faux positif doit être examiné avant d'ajouter de nouvelles règles.

## Architecture

- `app.py` : interface Streamlit et parcours utilisateur
- `core/detector.py` : orchestration des règles et rapport d'analyse
- `core/rules/` : règles de détection par catégorie
- `core/language.py` : estimation heuristique de la langue
- `core/explain.py` : bibliothèque pédagogique
- `i18n/` : textes de l'interface au format JSON
- `db/models.py`, `db/storage.py` : schéma et stockage SQLite local
- `tests/` : tests unitaires, corpus synthétique et test navigateur
- `.github/workflows/tests.yml` : tests automatiques sur chaque push vers `main`, pull request et lancement manuel

## Variables d'environnement et secrets

SafeSignal V1 n'utilise aucune clé API. Le fichier `.env.example` documente ce choix. Si une intégration externe est ajoutée plus tard, ses secrets devront être fournis via les secrets de GitHub Actions ou l'environnement local, jamais commités dans le dépôt. Le fichier `.env` est ignoré par Git.

## Contribuer

Consultez [CONTRIBUTING.md](CONTRIBUTING.md) avant d'ajouter une règle, une langue ou un exemple de test.

## Limites et sécurité

- Une alerte est un indice, pas une preuve. Des messages légitimes peuvent déclencher des alertes et des arnaques peuvent passer inaperçues.
- La détection repose sur des motifs textuels ; elle peut manquer l'argot, les variantes orthographiques ou de nouvelles tactiques.
- La mention d'une marque ne signifie pas qu'elle est usurpée.
- Aucun lien n'est ouvert ; aucune réputation DNS, de certificat ou de domaine n'est vérifiée.
- La détection linguistique est heuristique et peut se tromper.
- En cas de doute, ne cliquez pas et ne transmettez pas de code ou de données bancaires. Contactez l'organisme par un canal officiel trouvé indépendamment.

## Licence

Ce projet est distribué sous licence MIT. Consultez [LICENSE](LICENSE).
