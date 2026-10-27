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
        "paste_label": "Collez le SMS, e-mail ou message ici",
        "save_option": "Enregistrer dans l’historique local (inclut le texte original)",
        "ocr_tab": "🖼️ OCR local", "about_tab": "À propos", "skip_link": "Aller au contenu principal",
        "prevention_tab": "Conseils & Prévention",
        "guide": "Phishing / hameçonnage",
        "rules_tab": "⚙️ Mes règles", "rules_heading": "Gérer mes règles d’alerte personnalisées",
        "quiz_tab": "🎮 Quiz réflexes", "quiz_heading": "Testez vos réflexes anti-arnaque",
        "quiz_example": "Alerte sécurité : votre accès sera suspendu ce soir. Confirmez vos identifiants via ce lien inconnu.",
        "analyze_button": "Analyser le message",
        "report_title": "Rapport d’analyse",
        "clear_message": "Réinitialiser la zone de texte",
        "ocr_clear": "Réinitialiser l’outil OCR",
        "ocr_preview": "Aperçu de l’image",
    },
    "English": {
        "heading": "Check a message",
        "paste_label": "Paste SMS, email, or message here",
        "save_option": "Save to local history (includes original text)",
        "ocr_tab": "🖼️ Local OCR", "about_tab": "About", "skip_link": "Skip to main content",
        "prevention_tab": "Advice & Prevention",
        "guide": "Phishing and credential theft",
        "rules_tab": "⚙️ My rules", "rules_heading": "Manage my custom alert rules",
        "quiz_tab": "🎮 Scam-awareness quiz", "quiz_heading": "Test your scam-awareness reflexes",
        "quiz_example": "Security alert: your access will be suspended tonight. Confirm your login through this unfamiliar link.",
        "analyze_button": "Analyze message",
        "report_title": "Analysis report",
        "clear_message": "Reset message and result",
        "ocr_clear": "Reset OCR image and extracted text",
        "ocr_preview": "Image preview",
    },
    "العربية": {
        "heading": "افحص رسالة",
        "paste_label": "الصق الرسالة أو البريد هنا",
        "save_option": "حفظ في السجل المحلي (يتضمن النص الأصلي)",
        "ocr_tab": "🖼️ استخراج النص محلياً", "about_tab": "حول التطبيق", "skip_link": "انتقل إلى المحتوى الرئيسي",
        "prevention_tab": "النصائح والوقاية",
        "guide": "التصيد الاحتيالي وسرقة بيانات الدخول",
        "rules_tab": "⚙️ قواعدي", "rules_heading": "إدارة قواعد التنبيه المخصصة",
        "quiz_tab": "🎮 اختبار اليقظة", "quiz_heading": "اختبر قدرتك على تمييز الاحتيال",
        "quiz_example": "تنبيه أمني: سيتم تعليق دخولك الليلة. أكد بيانات الدخول عبر هذا الرابط غير المعروف.",
        "analyze_button": "تحليل الرسالة",
        "report_title": "تقرير التحليل",
        "clear_message": "إعادة ضبط حقل الرسالة",
        "ocr_clear": "إعادة ضبط أداة استخراج النص",
        "ocr_preview": "معاينة الصورة",
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
                    selector.get_by_role("combobox").click()
                    page.get_by_role("option", name=language, exact=True).click()
                    page.wait_for_timeout(900)
                assert page.get_by_text(expected["heading"], exact=True).count() > 0, (
                    f'Expected translated heading not found for {language}'
                )
                skip_link = page.locator("a.skip-link")
                assert skip_link.count() == 1, f'Skip-to-content link is missing for {language}'
                assert skip_link.inner_text() == expected["skip_link"], (
                    f'Skip-to-content link is untranslated for {language}: {skip_link.inner_text()}'
                )
                assert page.get_by_role("textbox", name=expected["paste_label"]).count() == 1, (
                    f'Main message field has no accessible name for {language}'
                )
                assert page.get_by_role("checkbox", name=expected["save_option"]).count() == 1, (
                    f'Consent checkbox has no accessible name for {language}'
                )
                # Verify the message reset in the real browser: text, consent, and report are cleared.
                message_box = page.get_by_role("textbox", name=expected["paste_label"])
                consent_box = page.get_by_role("checkbox", name=expected["save_option"])
                message_box.fill("Private reset smoke-test message")
                consent_box.check()
                consent_box.uncheck()
                page.get_by_role("button", name=expected["analyze_button"]).click()
                assert page.get_by_text(expected["report_title"], exact=True).count() == 1, (
                    f'Analysis report was not displayed for {language}'
                )
                page.get_by_role("button", name=expected["clear_message"]).click()
                page.wait_for_timeout(200)
                assert message_box.input_value() == "", f'Message was not cleared for {language}'
                assert not consent_box.is_checked(), f'Consent was not reset for {language}'
                assert page.get_by_text(expected["report_title"], exact=True).count() == 0, (
                    f'Analysis report remained after reset for {language}'
                )

                # Upload a tiny in-memory PNG and verify the OCR reset removes its preview.
                page.get_by_role("tab", name=expected["ocr_tab"]).click()
                page.wait_for_timeout(200)
                upload = page.locator('input[type="file"]').first
                import base64
                upload.set_input_files({
                    "name": "privacy-smoke.png",
                    "mimeType": "image/png",
                    "buffer": base64.b64decode(
                        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/XuoAAAAASUVORK5CYII="
                    ),
                })
                page.wait_for_timeout(250)
                assert page.get_by_text(expected["ocr_preview"], exact=True).count() == 1, (
                    f'OCR image preview did not appear for {language}'
                )
                page.get_by_role("button", name=expected["ocr_clear"]).click()
                page.wait_for_timeout(200)
                assert page.get_by_text(expected["ocr_preview"], exact=True).count() == 0, (
                    f'OCR preview remained after reset for {language}'
                )
                page.get_by_role("tab", name=expected["about_tab"]).click()
                page.wait_for_timeout(150)
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
                # Responsive regression: 720px approximates a 200%-zoom layout on a 1440px display;
                # 375px and 320px cover common narrow mobile widths.
                page.get_by_role("tab").nth(0).click()
                for width in (720, 375, 320):
                    page.set_viewport_size({"width": width, "height": 900})
                    page.wait_for_timeout(250)
                    textarea = page.locator('[data-testid="stTextArea"] textarea').first
                    assert textarea.is_visible(), f'Text input is not visible at {width}px for {language}'
                    box = textarea.bounding_box()
                    assert box and box["width"] <= width, f'Text input exceeds viewport at {width}px for {language}'
                    overflow = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
                    assert overflow <= 12, f'Unexpected horizontal page overflow ({overflow}px) at {width}px for {language}'
                # Basic keyboard-only focus check; a real screen reader still requires manual testing.
                page.set_viewport_size({"width": 1440, "height": 1000})
                page.keyboard.press("Tab")
                focused_tag = page.evaluate("document.activeElement && document.activeElement.tagName")
                assert focused_tag and focused_tag != "BODY", f'Keyboard focus was not exposed for {language}'
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
