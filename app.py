import requests
import json
import streamlit as st
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.firefox import GeckoDriverManager
import re

def process_clue(s):
    clean_s = re.sub(r'<[^>]+>', '', s)
    nums_str = re.search(r'$', clean_s).group(1)
    return [clean_s, sum(int(n.strip()) for n in nums_str.split(',')), nums_str]

def get_driver():
    options = Options()
    options.add_argument("--headless")  # Standard headless mode
    
    # Firefox is much more stable in containers and 
    # usually doesn't need the 'no-sandbox' or 'no-zygote' hacks.
    
    service = Service(GeckoDriverManager(version="v0.34.0").install())
    return webdriver.Firefox(service=service, options=options)

# Keep text only
def get_clues():
    try:
        driver = get_driver()
        driver.get("https://www.minutecryptic.com")
        wait = WebDriverWait(driver, 10)

        # 1. Dismiss "not now" popup if it appears
        try:
            not_now = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//p[contains(text(), 'not now')]]"))
            )
            not_now.click()
        except (NoSuchElementException, TimeoutException):
            pass

        # 2. Click "Play" pink button
        play_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.bg-mc-pink"))
        )
        play_btn.click()

        # 3. Click the main "Hints" entry button
        hint_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-sentry-component='ShadowButton']"))
        )
        driver.execute_script("arguments[0].click();", hint_button)

        # 4. Find the first hint category button
        all_buttons = wait.until(
            lambda d: [
                btn for btn in d.find_elements(By.TAG_NAME, "button")
                if btn.text.strip().lower() not in ["", "hints", "check", "back"]
            ]
        )
        if not all_buttons:
            raise RuntimeError("No hint categories found.")

        first_hint_title = all_buttons[0].text.strip()

        # 5. Click the first hint button to populate localStorage
        h_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//button[.//p[text()='{first_hint_title}']]"))
        )
        driver.execute_script("arguments[0].click();", h_btn)

        # 6. Retrieve data from localStorage
        puzzle_raw = None
        for _ in range(25):
            puzzle_raw = driver.execute_script("return window.localStorage.getItem('mc-puzzle');")
            if puzzle_raw:
                break
            time.sleep(0.2)

        if not puzzle_raw:
            raise RuntimeError("localStorage.getItem('mc-puzzle') is empty.")

        puzzle_data = json.loads(puzzle_raw)

        # --- Variable Mapping ---
        # q: Full clue text + length annotation
        clue_words = " ".join([c["text"] for c in puzzle_data.get("clue", []) if "text" in c])
        config_lengths = puzzle_data.get("config", [])
        config_str = ",".join(str(n) for n in config_lengths)
        q = f"{clue_words} ({config_str})" if config_str else clue_words

        # a: Answer
        a = puzzle_data.get("answer", "")

        # Hints: h1..h3 (text) and ht1..ht3 (types/titles)
        raw_hints = puzzle_data.get("hints", [])
        h1 = raw_hints[0].get("text", "No hint") if len(raw_hints) > 0 else "No hint"
        ht1 = raw_hints[0].get("type", "No hint") if len(raw_hints) > 0 else "No hint"

        h2 = raw_hints[1].get("text", "No hint") if len(raw_hints) > 1 else "No hint"
        ht2 = raw_hints[1].get("type", "No hint") if len(raw_hints) > 1 else "No hint"

        h3 = raw_hints[2].get("text", "No hint") if len(raw_hints) > 2 else "No hint"
        ht3 = raw_hints[2].get("type", "No hint") if len(raw_hints) > 2 else "No hint"

        # v: Explainer video link
        v = puzzle_data.get("explainerVideo", "")

        # sn: Setter name
        sn = puzzle_data.get("setterName", "")

        # --- Output formatting ---
        minute_cryptic_output_list = [q, a, h1, h2, h3, ht1, ht2, ht3, v, sn]
        #driver.get("https://dailycrypticle.com")
        response = requests.get("https://dailycrypticle.com/patent-stats")
        data = response.json()
        dc = [data[1], data[0], data[2], data[3]]
        dc[1]+=" ("+str(len(dc[0]))+")"
        #new dcrypt
        driver.get("https://dailycryptic.co/play/daily")
        element = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "p.font-serif.text-balance.text-ink")
            )
        )
        dq,dlooptime,dastr=process_clue(element.text)
        button_locator = (By.CSS_SELECTOR, "button[aria-label='Reveal hint']")
        button_locator2 = (By.CSS_SELECTOR, "button[aria-label='Reveal a letter']")
        c=0
        while True:
            button = wait.until(EC.presence_of_element_located(button_locator))
            if not button.is_enabled() or button.get_attribute("disabled") is not None:
                break
            button.click()
            c+=1
        dh1="no hint"
        dh2="no hint"
        dh3="no hint"
        dh4="no hint"
        if (c>=1):
            dh1 = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "div[style*='var(--hint-1)']")
                )
            ).text
        if (c>=2):
            dh2 = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "div[style*='var(--hint-2)']")
                )
            ).text
        if (c>=3):
            dh3 = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "div[style*='var(--hint-3)']")
                )
            ).text
        if (c>=4):
            dh4 = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "div[style*='var(--hint-3)']")
                )
            ).text
        for i in range(dlooptime):
            button = wait.until(EC.presence_of_element_located(button_locator2))
            if not button.is_enabled() or button.get_attribute("disabled") is not None:
                break
            button.click()
        letter_buttons = driver.find_elements(
            By.CSS_SELECTOR, "div.rounded-\\[var\\(--radius-md\\)\\] button"
        )
        word = "".join([btn.text.strip().lower() for btn in letter_buttons if btn.text.strip()])
        dc2 = [word, dq, "https://dailycryptic.co/play/daily", dh1, dh2, dh3, dh4]
        
        #dailylogic
        urlday = 'https://btulehndzikuesmrzmhd.supabase.co/functions/v1/get-server-day'
        payload={}
        response = requests.post(urlday, json=payload)
        data = response.json()['day']
        url = "https://btulehndzikuesmrzmhd.supabase.co/functions/v1/get-daily-puzzle"
        payload = {
            "type": "logic",
            "day": response.json()['day']
        }
        response = requests.post(url, json=payload)
        data = response.json()
        dlq=data['puzzle']['latex'].replace("\n","(dlnewline)")
        dl=[dlq]
        driver.quit()
        return (' ()minc() '.join(minute_cryptic_output_list)+' ()big() '+' ()dc() '.join(dc2)+' ()big() '+' ()dl() '.join(dl))
    except Exception as e:
        st.write(f"DEBUG:INIT_DRIVER:ERROR:{e}")
        st.text(' ()minc() '.join(minute_cryptic_output_list)+' ()big() '+' ()dc() '.join(dc2))
    finally:
        if driver is not None: driver.quit()
    return None

# ---------------- Page & UI/UX Components ------------------------
if __name__ == "__main__":
    d=get_clues()
    st.text(d)
