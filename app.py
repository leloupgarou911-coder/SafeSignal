import json
from pathlib import Path
import streamlit as st
from core.detector import analyze_message
from core.language import detect_language
from core.explain import LIBRARY
from db.storage import init_db, save_analysis, list_history, clear_history

ROOT=Path(__file__).parent
init_db()
st.set_page_config(page_title="SafeSignal",page_icon="🛡️",layout="centered")
LANGS={"Français":"fr","English":"en","العربية":"ar"}
label=st.sidebar.selectbox("Interface language / لغة الواجهة",list(LANGS))
lang=LANGS[label]
T=json.loads((ROOT/"i18n"/f"{lang}.json").read_text(encoding="utf-8"))
direction = "rtl" if lang == "ar" else "ltr"
st.markdown(f"""<style>
html, body, [data-testid="stAppViewContainer"] {{ direction: {direction}; }}
.block-container {{ max-width:900px; padding-top:2rem; }}
.trust {{ padding:1rem; border-radius:12px; background:#eaf5ff; border:1px solid #b7dcfa; color:#12344d; text-align:{'right' if lang == 'ar' else 'left'}; }}
</style>""",unsafe_allow_html=True)
st.title("🛡️ SafeSignal")
st.caption(T["tagline"])
st.markdown(f'<div class="trust">🔒 <b>{T["privacy_title"]}</b><br>{T["privacy_text"]}</div>',unsafe_allow_html=True)
a,b,c,d=st.tabs([T["analyze"],T["library"],T["history"],T["about"]])
with a:
 st.subheader(T["paste_title"])
 message=st.text_area(T["paste_label"],height=190,max_chars=20000,placeholder=T["placeholder"])
 consent=st.checkbox(T["save_option"],value=False,help=T["save_help"])
 if st.button(T["analyze_button"],type="primary",use_container_width=True):
  if not message.strip(): st.warning(T["empty_warning"])
  else:
   report=analyze_message(message,detect_language(message))
   st.session_state["report"]=report
   if consent: save_analysis(report,message,consent=True)
   else: st.info(T["not_saved"])
 report=st.session_state.get("report")
 if report:
  st.divider(); st.subheader(T["report_title"])
  st.info(T["report_intro"].format(language=report["language"].upper()))
  if not report["findings"]: st.success(T["no_signals"])
  for x in report["findings"]:
   icon={"low":"🟢","medium":"🟠","high":"🔴"}.get(x["severity"],"🔎")
   with st.expander(f'{icon} {x["title"]} · {T["confidence"]}: {T[x["confidence"]]}'):
    st.write(x["explanation"]); st.markdown(f'**{T["why"]}** {x["evidence"]}'); st.markdown(f'**{T["advice"]}** {x["advice"]}')
    st.caption(f'{T["category"]}: {x["category"]}')
  st.warning(T["limits"])
  st.markdown(f'**{T["next_steps"]}**')
  for tip in report["general_advice"]: st.write("• "+tip)
with b:
 st.subheader(T["library"])
 for item in LIBRARY[lang]:
  with st.expander(item["title"]):
   st.write(item["description"]); st.markdown(f'**{T["how_to_spot"]}** {item["spot"]}'); st.markdown(f'**{T["what_to_do"]}** {item["action"]}')
with c:
 st.subheader(T["history"]); st.caption(T["history_local"])
 rows=list_history()
 if not rows: st.write(T["history_empty"])
 for row in rows:
  with st.expander(f'{row["created_at"]} · {row["summary"]}'): st.write(row["report"])
 if rows and st.button(T["clear_history"]): clear_history(); st.rerun()
with d:
 st.subheader(T["about"]); st.write(T["about_text"]); st.warning(T["safety_note"])
