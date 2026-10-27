import json
import sqlite3
from pathlib import Path

import streamlit as st

from core.detector import analyze_message
from core.language import detect_language
from core.explain import LIBRARY
from core.prevention import get_guides
from db.storage import init_db, save_analysis, list_history, clear_history

ROOT = Path(__file__).parent
ERRORS = {
    "fr": {
        "storage": "Le stockage local est indisponible. L’analyse reste possible, mais l’historique ne peut pas être utilisé.",
        "saved": "Analyse enregistrée dans l’historique local.",
        "analysis": "Une erreur a empêché l’analyse. Réessayez avec un autre message.",
        "history": "Impossible de lire ou modifier l’historique local. Vérifiez les permissions du dossier.",
    },
    "en": {
        "storage": "Local storage is unavailable. Analysis can still run, but history cannot be used.",
        "saved": "Analysis saved to local history.",
        "analysis": "An error prevented the analysis. Please try another message.",
        "history": "Unable to read or update local history. Check the folder permissions.",
    },
    "ar": {
        "storage": "التخزين المحلي غير متاح. يمكن إجراء التحليل، لكن لا يمكن استخدام السجل.",
        "saved": "تم حفظ التحليل في السجل المحلي.",
        "analysis": "حدث خطأ أثناء التحليل. حاول برسالة أخرى.",
        "history": "تعذرت قراءة السجل المحلي أو تعديله. تحقق من صلاحيات المجلد.",
    },
}
HISTORY_LABELS = {
    "fr": {"language": "Langue du rapport", "alerts": "Indices détectés", "message": "Message analysé", "details": "Détails"},
    "en": {"language": "Report language", "alerts": "Signals detected", "message": "Analyzed message", "details": "Details"},
    "ar": {"language": "لغة التقرير", "alerts": "المؤشرات المكتشفة", "message": "الرسالة التي تم تحليلها", "details": "التفاصيل"},
}
try:
    init_db()
    DB_READY = True
except (sqlite3.Error, OSError):
    DB_READY = False

st.set_page_config(page_title="SafeSignal", page_icon="🛡️", layout="wide")
LANGS = {"Français": "fr", "English": "en", "العربية": "ar"}
label = st.sidebar.selectbox("Interface language / لغة الواجهة", list(LANGS))
lang = LANGS[label]
T = json.loads((ROOT / "i18n" / f"{lang}.json").read_text(encoding="utf-8"))
E = ERRORS[lang]
HL = HISTORY_LABELS[lang]
direction = "rtl" if lang == "ar" else "ltr"
text_align = "right" if lang == "ar" else "left"
st.markdown(f"""<style>
html, body, [data-testid="stAppViewContainer"] {{ direction: {direction}; }}
.block-container {{ max-width:1200px; padding-top:2rem; padding-bottom:3rem; }}
.stTextArea textarea, .stTextInput input {{ direction: {direction}; text-align: {text_align}; }}
[data-testid="stTabs"] [role="tablist"] {{ direction: {direction}; gap:.35rem; }}
[data-testid="stMarkdownContainer"], [data-testid="stCaptionContainer"] {{ text-align: {text_align}; }}
.trust {{ padding:1rem 1.15rem; border-radius:14px; background:#eaf5ff; border:1px solid #b7dcfa; color:#12344d; text-align:{text_align}; margin:.6rem 0 1.2rem; }}
div[data-testid="stVerticalBlockBorderWrapper"] {{ border-color:#d7e7f5; border-radius:14px; }}
.guide-example {{ border-radius:10px; padding:.8rem; }}
</style>""", unsafe_allow_html=True)
st.title("🛡️ SafeSignal")
st.caption(T["tagline"])
st.markdown(f'<div class="trust">🔒 <b>{T["privacy_title"]}</b><br>{T["privacy_text"]}</div>', unsafe_allow_html=True)
if not DB_READY:
    st.error(E["storage"])

a, b, p, c, d = st.tabs([T["analyze"], T["library"], T["prevention"], T["history"], T["about"]])
with a:
    st.subheader(T["paste_title"])
    message = st.text_area(T["paste_label"], height=190, max_chars=20000, placeholder=T["placeholder"])
    consent = st.checkbox(T["save_option"], value=False, help=T["save_help"])
    if st.button(T["analyze_button"], type="primary", use_container_width=True):
        if not message.strip():
            st.warning(T["empty_warning"])
        else:
            try:
                report = analyze_message(message, lang)
                report["detected_language"] = detect_language(message)
                st.session_state["report"] = report
                if consent:
                    if DB_READY:
                        save_analysis(report, message, consent=True)
                        st.success(E["saved"])
                    else:
                        st.warning(E["storage"])
                else:
                    st.info(T["not_saved"])
            except (ValueError, TypeError, KeyError, sqlite3.Error):
                st.error(E["analysis"])
                st.session_state.pop("report", None)
    report = st.session_state.get("report")
    if report:
        st.divider()
        st.subheader(T["report_title"])
        st.info(T["report_intro"].format(language=report["language"].upper()))
        if not report["findings"]:
            st.success(T["no_signals"])
        for x in report["findings"]:
            icon = {"low": "🟢", "medium": "🟠", "high": "🔴"}.get(x["severity"], "🔎")
            with st.expander(f'{icon} {x["title"]} · {T["confidence"]}: {T[x["confidence"]]}'):
                st.write(x["explanation"])
                st.markdown(f'**{T["why"]}** {x["evidence"]}')
                st.markdown(f'**{T["advice"]}** {x["advice"]}')
                st.caption(f'{T["category"]}: {x["category"]}')
        st.warning(T["limits"])
        st.markdown(f'**{T["next_steps"]}**')
        for tip in report["general_advice"]:
            st.write("• " + tip)
with b:
    st.subheader(T["library"])
    for item in LIBRARY[lang]:
        with st.expander(item["title"]):
            st.write(item["description"])
            st.markdown(f'**{T["how_to_spot"]}** {item["spot"]}')
            st.markdown(f'**{T["what_to_do"]}** {item["action"]}')
with p:
    st.subheader(T["prevention"])
    st.caption(T["prevention_intro"])
    guides = get_guides(lang)
    columns = st.columns(2)
    for index, guide in enumerate(guides):
        with columns[index % 2]:
            with st.container(border=True):
                st.markdown(f'### {guide["icon"]} {guide["title"]}')
                st.write(guide["summary"])
                with st.expander(T["checklist_title"], expanded=False):
                    for item_index, item in enumerate(guide["checklist"]):
                        st.checkbox(
                            item,
                            key=f'guide_{lang}_{guide["id"]}_{item_index}',
                        )
                left, right = st.columns(2)
                with left:
                    st.markdown(f'**{guide["legit_label"]}**')
                    st.success(guide["legit"], icon="✅")
                with right:
                    st.markdown(f'**{guide["scam_label"]}**')
                    st.warning(guide["scam"], icon="⚠️")
    st.info(T["prevention_reminder"])
with c:
    st.subheader(T["history"])
    st.caption(T["history_local"])
    if not DB_READY:
        st.warning(E["storage"])
    else:
        try:
            rows = list_history()
            if not rows:
                st.write(T["history_empty"])
            for row in rows:
                with st.expander(f'{row["created_at"]} · {row["summary"]}'):
                    saved_report = json.loads(row["report"])
                    st.caption(
                        f'{HL["language"]}: {saved_report.get("language", "fr").upper()} · '
                        f'{HL["alerts"]}: {len(saved_report.get("findings", []))}'
                    )
                    if row.get("original_text"):
                        st.markdown(f'**{HL["message"]}**')
                        st.text(row["original_text"])
                    st.markdown(f'**{HL["details"]}**')
                    findings = saved_report.get("findings", [])
                    if not findings:
                        st.success(T["no_signals"])
                    for finding in findings:
                        with st.expander(finding.get("title", finding.get("rule_id", "Signal"))):
                            st.write(finding.get("explanation", ""))
                            if finding.get("advice"):
                                st.markdown(f'**{T["advice"]}** {finding["advice"]}')
            if rows and st.button(T["clear_history"]):
                clear_history()
                st.rerun()
        except (sqlite3.Error, ValueError, TypeError, KeyError):
            st.error(E["history"])
with d:
    st.subheader(T["about"])
    st.write(T["about_text"])
    st.warning(T["safety_note"])
