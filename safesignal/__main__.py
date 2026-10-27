"""Run SafeSignal from the terminal with python -m safesignal."""

from __future__ import annotations

import argparse
import json
import logging
import signal
import sys
from pathlib import Path
from typing import Sequence

from core.detector import analyze_message
from core.language import detect_language

LOGGER = logging.getLogger("safesignal")
MAX_MESSAGE_LENGTH = 20_000
SUPPORTED_LANGUAGES = ("fr", "en", "ar")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="safesignal",
        description="Analyse un message pour repérer des indices possibles d'arnaque.",
        epilog="Une alerte est un indice, pas une preuve de fraude.",
    )
    source = parser.add_mutually_exclusive_group()
    source.add_argument("-t", "--text", help="Message à analyser directement.")
    source.add_argument("-f", "--file", type=Path, help="Lire le message depuis un fichier UTF-8.")
    parser.add_argument(
        "-l", "--language", choices=SUPPORTED_LANGUAGES,
        help="Langue des explications (par défaut : détection heuristique).",
    )
    parser.add_argument("--json", action="store_true", help="Afficher le rapport au format JSON.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Activer les journaux de diagnostic.")
    return parser


def _read_message(args: argparse.Namespace, stdin=None) -> str:
    if args.text is not None:
        message = args.text
    elif args.file is not None:
        try:
            message = args.file.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            raise ValueError(f"Impossible de lire le fichier {args.file}: {exc}") from exc
    elif stdin is not None and not stdin.isatty():
        message = stdin.read()
    else:
        raise ValueError("Fournissez --text, --file ou un message via l'entrée standard.")

    if not message.strip():
        raise ValueError("Le message est vide.")
    if len(message) > MAX_MESSAGE_LENGTH:
        raise ValueError(f"Le message dépasse la limite de {MAX_MESSAGE_LENGTH} caractères.")
    return message


def _install_signal_handlers() -> None:
    """Make Ctrl+C and termination exit cleanly; this CLI holds no long-lived resources."""
    def stop(signum, _frame):
        raise KeyboardInterrupt(f"signal système {signum}")

    signal.signal(signal.SIGINT, stop)
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, stop)


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    _install_signal_handlers()

    try:
        message = _read_message(args, sys.stdin)
        language = args.language or detect_language(message)
        LOGGER.debug("Analyse démarrée (langue=%s, caractères=%d)", language, len(message))
        report = analyze_message(message, language)
        report["detected_language"] = detect_language(message)
        if args.json:
            sys.stdout.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        else:
            findings = report["findings"]
            if not findings:
                sys.stdout.write("Aucun indice connu détecté. Cela ne garantit pas que le message soit sûr.\n")
            else:
                sys.stdout.write(f"{len(findings)} indice(s) détecté(s) :\n")
                for item in findings:
                    sys.stdout.write(f"- [{item['severity'].upper()}] {item['title']}\n")
                    sys.stdout.write(f"  Indice : {item['evidence']}\n")
                    sys.stdout.write(f"  Pourquoi : {item['explanation']}\n")
                    sys.stdout.write(f"  Conseil : {item['advice']}\n")
            sys.stdout.write("\nRappel : une alerte est un indice, pas une preuve.\n")
        LOGGER.debug("Analyse terminée (indices=%d)", len(report["findings"]))
        return 0
    except KeyboardInterrupt:
        LOGGER.info("Arrêt demandé ; fermeture propre.")
        return 130
    except (ValueError, OSError) as exc:
        LOGGER.error("%s", exc)
        return 2
    except Exception:
        LOGGER.exception("Erreur inattendue pendant l'analyse.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
