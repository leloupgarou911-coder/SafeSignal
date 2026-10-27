import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts" / "streamlit"
URL = "http://127.0.0.1:8501"
EXPECTED = {
    "Français": {
        "heading": "Examinez un message",
        "ocr_tab": "🖼️ OCR local", "about_tab": "À propos", "skip_link": "Aller au contenu principal",
        "prevention_tab": "Conseils & Prévention",
        "guide": "Phishing / hameçonnage",
        "rules_tab": "⚙️ Mes règles", "rules_heading": "Gérer mes règles d’alerte personnalisées",
        "quiz_tab": "🎮 Quiz réflexes", "quiz_heading": "Testez vos réflexes anti-arnaque",
        "quiz_example": "Alerte sécurité : votre accès sera suspendu ce soir. Confirmez vos identifiants via ce lien inconnu.",
    },
    "English": {
        "heading": "Check a message",
        "ocr_tab": "🖼️ Local OCR", "about_tab": "About", "skip_link": "Skip to main content",
        "prevention_tab": "Advice & Prevention",
        "guide": "Phishing and credential theft",
        "rules_tab": "⚙️ My rules", "rules_heading": "Manage my custom alert rules",
        "quiz_tab": "🎮 Scam-awareness quiz", "quiz_heading": "Test your scam-awareness reflexes",
        "quiz_example": "Security alert: your access will be suspended tonight. Confirm your login through this unfamiliar link.",
    },
    "العربية": {
        "heading": "افحص رسالة",
        "ocr_tab": "🖼️ استخراج النص محلياً", "about_tab": "حول التطبيق", "skip_link": "انتقل إلى المحتوى الرئيسي",
        "prevention_tab": "النصائح والوقاية",
        "guide": "التصيد الاحتيالي وسرقة بيانات الدخول",
        "rules_tab": "⚙️ قواعدي", "rules_heading": "إدارة قواعد التنبيه المخصصة",
        "quiz_tab": "🎮 اختبار اليقظة", "quiz_heading": "اختبر قدرتك على تمييز الاحتيال",
        "quiz_example": "تنبيه أمني: سيتم تعليق دخولك الليلة. أكد بيانات الدخول عبر هذا الرابط غير المعروف.",
    },
}


def wait_for_server(process):
    for _ in range(60):
        if process.poll() is not None:
            raise RuntimeError("Streamlit exited before becoming ready")
        try:
            urllib.request.urlopen(URL, timeout=1).read(32)
            return
        except Exception:
            time.sleep(1)
    raise RuntimeError("Streamlit did not become ready")


def main():
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", str(ROOT / "app.py"),
         "--server.headless=true", "--server.address=127.0.0.1",
         "--server.port=8501", "--browser.gatherUsageStats=false"],
        cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True,
    )
    try:
        wait_for_server(process)
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
            page.goto(URL, wait_until="networkidle")
            page.wait_for_timeout(900)
            for index, (language, expected) in enumerate(EXPECTED.items()):
                if index:
                    selector = page.locator('[data-testid="stSidebar"] [data-testid="stSelectbox"]')
                    selector.click()
                    page.get_by_text(language, exact=True).last.click()
                    page.wait_for_timeout(900)
                assert page.get_by_text(expected["heading"], exact=True).count() > 0, (
                    f'Expected translated heading not found for {language}'
                )
                assert page.get_by_role("link", name=expected["skip_link"]).count() == 1, (
                    f'Skip-to-content link is missing or untranslated for {language}'
                )
                assert page.get_by_role("tab", name=expected["ocr_tab"]).count() == 1, (
                    f'OCR tab has no accessible translated name for {language}'
                )
                assert page.get_by_role("tab", name=expected["about_tab"]).count() == 1, (
                    f'About tab has no accessible translated name for {language}'
                )
                direction = page.locator("html").evaluate("(node) => getComputedStyle(node).direction")
                assert direction == ("rtl" if language == "العربية" else "ltr"), (
                    f'Unexpected text direction for {language}: {direction}'
                )
                tabs = page.get_by_role("tab")
                selected_tabs = page.locator('[role="tab"][aria-selected="true"]')
                before_selected = selected_tabs.first.inner_text()
                tabs.nth(0).focus()
                page.keyboard.press("ArrowRight")
                page.wait_for_timeout(150)
                selected_tabs = page.locator('[role="tab"][aria-selected="true"]')
                assert selected_tabs.count() == 1, f'Keyboard tab navigation failed for {language}'
                assert selected_tabs.first.get_attribute("aria-selected") == "true"
                assert selected_tabs.first.inner_text() != before_selected, (
                    f'Arrow-key navigation did not change the active tab for {language}'
                )
                page.screenshot(path=str(ARTIFACTS / f"{index+1}-{('fr','en','ar')[index]}-analysis.png"), full_page=True)
                tab = page.get_by_role("tab", name=expected["prevention_tab"])
                tab.click()
                page.wait_for_timeout(400)
                assert page.get_by_text(expected["guide"], exact=False).count() > 0, (
                    f'Prevention guide did not render in {language}'
                )
                page.screenshot(path=str(ARTIFACTS / f"{index+1}-{('fr','en','ar')[index]}-prevention.png"), full_page=True)
                rules_tab = page.get_by_role("tab", name=expected["rules_tab"])
                rules_tab.click()
                page.wait_for_timeout(300)
                assert page.get_by_text(expected["rules_heading"], exact=True).count() > 0, (
                    f'Custom rules tab did not render in {language}'
                )
                quiz_tab = page.get_by_role("tab", name=expected["quiz_tab"])
                quiz_tab.click()
                page.wait_for_timeout(300)
                assert page.get_by_text(expected["quiz_heading"], exact=True).count() > 0, (
                    f'Quiz tab did not render in {language}'
                )
                assert page.get_by_text(expected["quiz_example"], exact=True).count() > 0, (
                    f'Quiz question did not render in {language}'
                )
                page.screenshot(path=str(ARTIFACTS / f"{index+1}-{('fr','en','ar')[index]}-quiz.png"), full_page=True)
                print(f"PASS {language}: analysis, prevention, custom rules and quiz rendered")
            browser.close()
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
    print(f"Screenshots: {ARTIFACTS}")


if __name__ == "__main__":
    main()
