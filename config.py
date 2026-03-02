from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from datetime import datetime
import os

class B2BPriceCollector:
    def __init__(self):
        print("🚀 브라우저 시작 (서버 최적화 모드)...")
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            print(f"⚠️ 드라이버 재시도: {e}")
            options.binary_location = "/usr/bin/chromium"
            service = Service("/usr/bin/chromedriver")
            self.driver = webdriver.Chrome(service=service, options=options)
        self.results = []

    def login(self, site_name, login_url, username, password, username_selector, password_selector, login_button_selector):
        try:
            self.driver.get(login_url)
            time.sleep(2)
            u_input = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, username_selector)))
            u_input.clear()
            u_input.send_keys(username)
            p_input = self.driver.find_element(By.CSS_SELECTOR, password_selector)
            p_input.clear()
            p_input.send_keys(password)
            self.driver.find_element(By.CSS_SELECTOR, login_button_selector).click()
            time.sleep(2)
            return True
        except:
            return False

    def collect_product_list(self, site_name, list_url, selectors):
        try:
            from config import FILTER_KEYWORDS, MAX_PAGES, EXCLUDE_KEYWORDS
            page = 1
            while True:
                if MAX_PAGES and page > MAX_PAGES: break
                self.driver.get(f"{list_url}&page={page}")
                time.sleep(1.5)
                items = self.driver.find_elements(By.CSS_SELECTOR, selectors['item_container'])
                if not items: break
                for item in items:
                    try:
                        p_name = item.find_element(By.CSS_SELECTOR, selectors['product_name']).text
                        if FILTER_KEYWORDS and not any(k in p_name for k in FILTER_KEYWORDS): continue
                        onclick = item.get_attribute('onclick')
                        pcode = onclick.split('"')[1]
                        detail_url = f"https://hwanggs3.adminplus.co.kr/partner/product/prt.detail.pop.php?pcode={pcode}"
                        self.driver.execute_script(f"window.open('{detail_url}','_blank');")
                        self.driver.switch_to.window(self.driver.window_handles[-1])
                        time.sleep(1.5)
                        rows = self.driver.find_elements(By.CSS_SELECTOR, ".list_table tr")[1:]
                        for row in rows:
                            cells = row.find_elements(By.TAG_NAME, "td")
                            if len(cells) >= 6:
                                self.results.append({
                                    '수집날짜': datetime.now().strftime('%Y-%m-%d %H:%M'),
                                    '사이트명': site_name,
                                    '상품명': p_name,
                                    '옵션명': cells[0].text.strip(),
                                    '공급가': cells[2].text.strip()
                                })
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])
                    except: continue
                page += 1
        except: pass

    def save_excel(self, filename='가격비교.xlsx'):
        if self.results:
            pd.DataFrame(self.results).to_excel(filename, index=False, engine='openpyxl')

    def close(self):
        if hasattr(self, 'driver'): self.driver.quit()
