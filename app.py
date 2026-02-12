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

st.set_page_config(layout="wide")

# Keep text only
def get_clues():
    driver = None
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage") # Overcomes limited resource problems
        options.add_argument("--remote-debugging-port=9222")
        options.binary_location = "/usr/bin/google-chrome"
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=options)
        driver.get("https://www.minutecryptic.com")
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.bg-mc-pink'))
        )
        driver.execute_script("arguments[0].click();", button)
        css_selector = "div[data-testid='visible-content']"

        sn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'p.text-\\[12px\\].text-black'))
        ).get_attribute("innerHTML")[3:].replace("&amp;","&")
        wait = WebDriverWait(driver, 10) # Wait up to 10 seconds
        visible_content_div = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
        def process_clue(s):
            clean_s = re.sub(r'<[^>]+>', '', s)
            nums_str = re.search(r'\(([\d,\s]+)\)$', clean_s).group(1)
            return [clean_s, sum(int(n.strip()) for n in nums_str.split(',')), nums_str]
        q,looptime,astr=process_clue(visible_content_div.text)
        hint_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-sentry-component='ShadowButton']"))
        )
        driver.execute_script("arguments[0].click();", hint_button)
        all_buttons_in_div = [i for i in driver.find_elements(By.TAG_NAME, "button") if i.text not in ["","hints","check"]]
        #print(all_buttons_in_div, [i.text for i in all_buttons_in_div])
        ht1="No hint"
        ht2="No hint"
        ht3="No hint"
        h1="No hint"
        h2="No hint"
        h3="No hint"
        if (len(all_buttons_in_div)>=2):
            ht1=all_buttons_in_div[0].text
        if (len(all_buttons_in_div)>=3):
            ht2=all_buttons_in_div[1].text
        if (len(all_buttons_in_div)>=4):
            ht3=all_buttons_in_div[2].text
        if (len(all_buttons_in_div)>=2):
            hint1_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//p[text()='"+ht1+"']]"))
            )
            driver.execute_script("arguments[0].click();", hint1_button)
            paragraph_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "p[data-sentry-component='PuzzleHintContent']"
            )))
            h1=paragraph_element.text
            clickable_element_selector = "div.text-\\[32px\\].cursor-pointer.active\\:opacity-60.transition-opacity.duration-200"
            clickable_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                clickable_element_selector
            )))
            driver.execute_script("arguments[0].click();", clickable_element)
        if (len(all_buttons_in_div)>=3):
            hint2_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//p[text()='"+ht2+"']]"))
            )
            driver.execute_script("arguments[0].click();", hint2_button)
            paragraph_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "p[data-sentry-component='PuzzleHintContent']"
            )))
            h2=paragraph_element.text
            clickable_element_selector = "div.text-\\[32px\\].cursor-pointer.active\\:opacity-60.transition-opacity.duration-200"
            clickable_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                clickable_element_selector
            )))
            driver.execute_script("arguments[0].click();", clickable_element)
        if (len(all_buttons_in_div)>=4):
            hint3_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//p[text()='"+ht3+"']]"))
            )
            driver.execute_script("arguments[0].click();", hint3_button)
            paragraph_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "p[data-sentry-component='PuzzleHintContent']"
            )))
            h3=paragraph_element.text
            clickable_element_selector = "div.text-\\[32px\\].cursor-pointer.active\\:opacity-60.transition-opacity.duration-200"
            clickable_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                clickable_element_selector
            )))
            driver.execute_script("arguments[0].click();", clickable_element)
        for i in range(looptime):
            show_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//p[text()='show letter']]"))
            )
            driver.execute_script("arguments[0].click();", show_button)
        apiece = [
            el.get_attribute("innerHTML")
            for el in WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.-translate-y-1'))
            )
        ]
        def getanswer(chars: list, lengths_str: str) -> str:
            segment_lengths = [int(length) for length in lengths_str.split(',')]
            result_segments = []
            current_char_index = 0
            for length in segment_lengths:
                segment_chars = chars[current_char_index : current_char_index + length]
                result_segments.append("".join(segment_chars))
                current_char_index += length
            return "-".join(result_segments)
        a=getanswer(apiece,astr)
        img_alt_selector = "img[alt='Daily explainer video thumbnail']"
        xpath_to_parent_link = "./ancestor::a"
        image_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, img_alt_selector)))
        link_element = image_element.find_element(By.XPATH, xpath_to_parent_link)
        v = link_element.get_attribute('href')
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
        return (' ()minc() '.join([q,a,h1,h2,h3,ht1,ht2,ht3,v,sn])+' ()big() '+' ()dc() '.join(dc))
    except Exception as e:
        st.write(f"DEBUG:INIT_DRIVER:ERROR:{e}")
    finally:
        if driver is not None: driver.quit()
    return None

# ---------------- Page & UI/UX Components ------------------------
if __name__ == "__main__":
    d=get_clues()
    st.text(d)
