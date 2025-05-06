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
def get_clues():
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
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.bg-mc-pink'))
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
        a=mcp['answer'].lower()
        q=' '.join([i['text'] for i in mcp['clue']])+' ('+','.join([str(len(j)) for j in a.split()])+')'
        h1=mcp['hints'][0]['text']
        h2=mcp['hints'][1]['text']
        h3=mcp['hints'][2]['text']
        ht1=mcp['hints'][0]['type']
        ht2=mcp['hints'][1]['type']
        ht3=mcp['hints'][2]['type']
        v=mcp['explainerVideo']
        driver.get("https://dailycrypticle.com/dailyclue.html")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        dc=['','','','']
        while '' in dc:
            dc[0]=driver.execute_script("return targetWord;")
            dc[1]=driver.execute_script("return clueData;")
            dc[2]=driver.execute_script("return urlData;")
            dc[3]=driver.execute_script("return definitionData;")
        dc[1]+=" ("+str(len(dc[0]))+")"
        driver.quit()
        return (' ()minc() '.join([q,a,h1,h2,h3,ht1,ht2,ht3,v])+' ()big() '+' ()dc() '.join(dc))
    except Exception as e:
        st.write(f"DEBUG:INIT_DRIVER:ERROR:{e}")
    finally:
        if driver is not None: driver.quit()
    return None

# ---------------- Page & UI/UX Components ------------------------
if __name__ == "__main__":
    d=get_clues()
    st.write(d)
