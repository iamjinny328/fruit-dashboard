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
        print("🚀 브라우저 시작 (리눅스 서버 최적화 모드)...")
        
        options = Options()
        # --- Streamlit Cloud(리눅스 서버) 필수 옵션 ---
        options.add_argument('--headless=new')             # 화면 없이 실행
        options.add_argument('--no-sandbox')               # 보안 제한 해제
        options.add_argument('--disable-dev-shm-usage')    # 공유 메모리 부족 방지
        options.add_argument('--disable-gpu')              # GPU 가속 끄기
        options.add_argument('--disable-blink-features=AutomationControlled')
        # -------------------------------------------
        
        options.add_argument('--start-maximized')
        prefs = {
            'profile.managed_default_content_settings.images': 2,
            'profile.default_content_setting_values.notifications': 2
        }
        options.add_experimental_option('prefs', prefs)
        
        # 서버 환경에서는 webdriver-manager가 가장 안정적입니다.
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.results = []
        
    def login(self, site_name, login_url, username, password, username_selector, password_selector, login_button_selector):
        try:
            print(f"\n🔐 [{site_name}] 로그인 시도...")
            self.driver.get(login_url)
            time.sleep(2) # 서버 속도를 고려해 대기 시간 소폭 증가
            
            username_input = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, username_selector))
            )
            username_input.clear()
            username_input.send_keys(username)
            print(f"   ✓ 아이디 입력 완료")
            
            password_input = self.driver.find_element(By.CSS_SELECTOR, password_selector)
            password_input.clear()
            password_input.send_keys(password)
            print(f"   ✓ 비밀번호 입력 완료")
            
            login_button = self.driver.find_element(By.CSS_SELECTOR, login_button_selector)
            login_button.click()
            print(f"   ✓ 로그인 버튼 클릭")
            
            time.sleep(2)
            print(f"✅ [{site_name}] 로그인 성공!")
            return True
            
        except Exception as e:
            print(f"❌ [{site_name}] 로그인 실패: {e}")
            return False
    
    def collect_product_list(self, site_name, list_url, selectors):
        try:
            print(f"\n📦 [{site_name}] 상품 리스트 수집 시작...")
            
            # 수집 중에도 필터 키워드를 실시간으로 반영하기 위해 config에서 직접 임포트
            from config import FILTER_KEYWORDS, MAX_PAGES, EXCLUDE_KEYWORDS
            
            page = 1
            total_collected = 0
            
            while True:
                if MAX_PAGES and page > MAX_PAGES:
                    print(f"✅ 페이지 제한 도달! ({MAX_PAGES}페이지)")
                    break
                
                page_url = f"{list_url}&page={page}"
                print(f"\n📄 [{page}페이지] 접속 중...")
                self.driver.get(page_url)
                time.sleep(1.5)
                
                items = self.driver.find_elements(By.CSS_SELECTOR, selectors['item_container'])
                
                if len(items) == 0:
                    print(f"✅ 더 이상 상품이 없습니다! (총 {page-1}페이지)")
                    break
                
                print(f"📊 {len(items)}개 상품 발견!")
                
                for idx, item in enumerate(items, 1):
                    try:
                        onclick = item.get_attribute('onclick')
                        pcode = onclick.split('"')[1]
                        grp = onclick.split('"')[3]
                        
                        product_name = item.find_element(By.CSS_SELECTOR, selectors['product_name']).text
                        
                        # 제외 키워드 체크
                        if EXCLUDE_KEYWORDS:
                            if any(keyword in product_name for keyword in EXCLUDE_KEYWORDS):
                                continue
                        
                        # 관심 키워드 체크 (한글 깨짐이 해결된 FILTER_KEYWORDS 사용)
                        if FILTER_KEYWORDS:
                            if not any(keyword in product_name for keyword in FILTER_KEYWORDS):
                                continue
                        
                        from config import SITES
                        detail_url_pattern = SITES[site_name].get('detail_url
