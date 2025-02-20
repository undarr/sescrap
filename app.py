import streamlit as st
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re

# ------------- Settings for Pages -----------
st.set_page_config(layout="wide")

# Keep text only
def get_minc_content():
    driver = None
    try:
        # Using on Local
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=options)
        driver.get("https://www.minutecryptic.com")
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-sentry-component="SerifVariant"]'))
        )
        # Click the button
        button.click()
        # Retrieve local storage data
        puzzle_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-sentry-component="PuzzlePiece"]'))
        )
        # Click the second button
        puzzle_button.click()
        puzzle_button.send_keys('a')
        local_storage = driver.execute_script("return window.localStorage;")
        mcp=json.loads(local_storage['mc-puzzle'])
        driver.quit()
        a=mcp['answer'].lower()
        q=' '.join([i['text'] for i in mcp['clue']])+' ('+str(len(a))+')'
        return ({'q':q,'a':a})
    except Exception as e:
        st.write(f"DEBUG:INIT_DRIVER:ERROR:{e}")
    finally:
        if driver is not None: driver.quit()
    return None

# ---------------- Page & UI/UX Components ------------------------
if __name__ == "__main__":
    st.write(get_minc_content()['q'],'$minc$',get_minc_content()['a'])
