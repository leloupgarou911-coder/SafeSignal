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
    "Français": "Examinez un message",
    "English": "Check a message",
    "العربية": "افحص رسالة",
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
            for index, (language, expected_text) in enumerate(EXPECTED.items()):
                if index:
                    selector = page.locator('[data-testid="stSidebar"] [data-testid="stSelectbox"]')
                    selector.click()
                    page.get_by_text(language, exact=True).last.click()
                    page.wait_for_timeout(900)
                assert page.get_by_text(expected_text, exact=True).count() > 0, (
                    f"Expected translated heading not found for {language}"
                )
                page.screenshot(path=str(ARTIFACTS / f"{index+1}-{('fr','en','ar')[index]}.png"), full_page=True)
                print(f"PASS {language}: heading rendered; screenshot saved")
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
