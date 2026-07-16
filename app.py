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

def get_driver():
    options = Options()
    options.add_argument("--headless")  # Standard headless mode
    
    # Firefox is much more stable in containers and 
    # usually doesn't need the 'no-sandbox' or 'no-zygote' hacks.
    
    service = Service(GeckoDriverManager().install())
    return webdriver.Firefox(service=service, options=options)

# Keep text only
def get_clues():
    try:
        driver = get_driver()
        driver.get("https://www.minutecryptic.com")
        button_xpath = "//button[.//p[contains(text(), 'not now')]]"
        try:
            button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, button_xpath))
            )
            button.click()
        except (NoSuchElementException, TimeoutException):
            pass
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.bg-mc-pink'))
        )
        button.click()
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
            clickable_element_selector = "button[aria-label='Back']"
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
            clickable_element_selector = "button[aria-label='Back']"
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
            clickable_element_selector = "button[aria-label='Back']"
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
        #driver.get("https://dailycrypticle.com")
        response = requests.get("https://dailycrypticle.com/patent-stats")
        data = response.json()
        dc = [data[1], data[0], data[2], data[3]]
        dc[1]+=" ("+str(len(dc[0]))+")"
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
        return (' ()minc() '.join([q,a,h1,h2,h3,ht1,ht2,ht3,v,sn])+' ()big() '+' ()dc() '.join(dc)+' ()big() '+' ()dl() '.join(dl))
    except Exception as e:
        st.write(f"DEBUG:INIT_DRIVER:ERROR:{e}")
        st.text(' ()minc() '.join([q,a,h1,h2,h3,ht1,ht2,ht3,v,sn])+' ()big() '+' ()dc() '.join(dc))
    finally:
        if driver is not None: driver.quit()
    return None

# ---------------- Page & UI/UX Components ------------------------
if __name__ == "__main__":
    d=get_clues()
    st.text(d)
