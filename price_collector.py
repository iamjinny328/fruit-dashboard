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
        print("🚀 브라우저 시작 (최적화 모드)...")
        
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--start-maximized')
        prefs = {
            'profile.managed_default_content_settings.images': 2,
            'profile.default_content_setting_values.notifications': 2
        }
        options.add_experimental_option('prefs', prefs)
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.results = []
        
    def login(self, site_name, login_url, username, password, username_selector, password_selector, login_button_selector):
        try:
            print(f"\n🔐 [{site_name}] 로그인 시도...")
            self.driver.get(login_url)
            time.sleep(1)
            
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
            import traceback
            traceback.print_exc()
            return False
    
    def collect_product_list(self, site_name, list_url, selectors):
        try:
            print(f"\n📦 [{site_name}] 상품 리스트 수집 시작...")
            
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
                time.sleep(1)
                
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
                        
                        # 관심 키워드 체크
                        if FILTER_KEYWORDS:
                            if not any(keyword in product_name for keyword in FILTER_KEYWORDS):
                                continue
                        
                        from config import SITES
                        detail_url_pattern = SITES[site_name].get('detail_url_pattern', '')
                        
                        if detail_url_pattern:
                            url_type = 'grp' if grp == '2' else ''
                            detail_url = detail_url_pattern.format(type=url_type, pcode=pcode)
                        else:
                            if grp == '2':
                                detail_url = f"https://hwanggs3.adminplus.co.kr/partner/product/prt.grp.detail.pop.php?pcode={pcode}"
                            else:
                                detail_url = f"https://hwanggs3.adminplus.co.kr/partner/product/prt.detail.pop.php?pcode={pcode}"
                        
                        print(f"🔍 [{page}페이지-{idx}/{len(items)}] {product_name} 상세정보 수집 중... (누적: {total_collected})")
                        
                        self.driver.execute_script(f"window.open('{detail_url}','_blank');")
                        self.driver.switch_to.window(self.driver.window_handles[-1])
                        time.sleep(1)
                        
                        option_rows = self.driver.find_elements(By.CSS_SELECTOR, ".list_table tr")[1:]
                        
                        for row in option_rows:
                            try:
                                cells = row.find_elements(By.TAG_NAME, "td")
                                if len(cells) >= 6:
                                    option_name = cells[0].text.strip()
                                    stock = cells[1].text.strip()
                                    price = cells[2].text.strip()
                                    sale_price = cells[3].text.strip()
                                    tax = cells[4].text.strip()
                                    shipping = cells[5].text.strip()
                                    
                                    matched_keyword = ''
                                    if FILTER_KEYWORDS:
                                        for keyword in FILTER_KEYWORDS:
                                            if keyword in product_name:
                                                matched_keyword = keyword
                                                break
                                    
                                    self.results.append({
                                        '수집날짜': datetime.now().strftime('%Y-%m-%d %H:%M'),
                                        '사이트명': site_name,
                                        '키워드': matched_keyword,
                                        '상품명': product_name,
                                        '옵션명': option_name,
                                        '재고': stock,
                                        '공급가': price,
                                        '판매가': sale_price,
                                        '과세여부': tax,
                                        '배송비': shipping.split('\n')[0],
                                        '상세URL': detail_url
                                    })
                                    print(f"   ✓ {option_name}: {price}")
                                    total_collected += 1
                            except:
                                continue
                        
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])
                        time.sleep(0.5)
                        
                    except Exception as e:
                        print(f"   ⚠️ 상품 처리 중 오류: {e}")
                        if len(self.driver.window_handles) > 1:
                            self.driver.close()
                            self.driver.switch_to.window(self.driver.window_handles[0])
                        continue
                
                print(f"✅ [{page}페이지] 완료!")
                page += 1
            
            print(f"\n🎉 [{site_name}] 전체 수집 완료! 총 {total_collected}개 옵션 수집!")
            
        except Exception as e:
            print(f"❌ [{site_name}] 수집 실패: {e}")
            import traceback
            traceback.print_exc()
    
    def save_excel(self, filename='가격비교.xlsx'):
        if self.results:
            df = pd.DataFrame(self.results)
            df.to_excel(filename, index=False, engine='openpyxl')
            print(f"\n💾 {filename} 저장 완료! (총 {len(self.results)}개 항목)")
        else:
            print("\n⚠️ 저장할 데이터가 없습니다!")
    
    def load_price_history(self, filename):
        if os.path.exists(filename):
            try:
                df = pd.read_excel(filename, engine='openpyxl')
                print(f"📂 이전 가격 데이터 로드: {len(df)}개 항목")
                return df
            except:
                print("⚠️ 이전 가격 데이터를 읽을 수 없습니다.")
                return None
        else:
            print("📌 첫 수집입니다. 이전 데이터가 없습니다.")
            return None
    
    def compare_prices(self, old_df, new_df):
        if old_df is None or len(old_df) == 0:
            print("📌 비교할 이전 데이터가 없습니다.")
            return new_df, []
        
        changes = []
        old_dict = {}
        for _, row in old_df.iterrows():
            key = f"{row['상품명']}_{row.get('옵션명', '')}"
            old_dict[key] = row['공급가'] if '공급가' in row else row.get('가격', '')
        
        for _, row in new_df.iterrows():
            key = f"{row['상품명']}_{row.get('옵션명', '')}"
            new_price = row['공급가'] if '공급가' in row else row.get('가격', '')
            
            if key in old_dict:
                old_price = old_dict[key]
            if key in old_dict:
                old_price = old_dict[key]
                if old_price != new_price:
                    changes.append({
                        '사이트명': row.get('사이트명', ''),
                        '키워드': row.get('키워드', ''),
                        '상품명': row['상품명'],
                        '옵션명': row.get('옵션명', ''),
                        '이전가격': old_price,
                        '현재가격': new_price,
                        '변동': '📈 인상' if self._price_to_int(new_price) > self._price_to_int(old_price) else '📉 인하',
                        '차액': self._price_to_int(new_price) - self._price_to_int(old_price),
                        '변동일': datetime.now().strftime('%Y-%m-%d %H:%M'),
                        '상세URL': row.get('상세URL', '')
                    })
            else:
                changes.append({
                    '사이트명': row.get('사이트명', ''),
                    '키워드': row.get('키워드', ''),
                    '상품명': row['상품명'],
                    '옵션명': row.get('옵션명', ''),
                    '이전가격': '-',
                    '현재가격': new_price,
                    '변동': '🆕 신규',
                    '차액': 0,
                    '변동일': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    '상세URL': row.get('상세URL', '')
                })        
        return new_df, changes
    
    def _price_to_int(self, price_str):
        try:
            price_str = str(price_str).replace('￦', '').replace(',', '').replace('~', '').split()[0]
            return int(price_str)
        except:
            return 0
    
    def save_with_change_detection(self, current_filename, history_filename):
        if not self.results:
            print("\n⚠️ 저장할 데이터가 없습니다!")
            return
        
        new_df = pd.DataFrame(self.results)
        old_df = self.load_price_history(history_filename)
        updated_df, changes = self.compare_prices(old_df, new_df)
        
        updated_df.to_excel(history_filename, index=False, engine='openpyxl')
        print(f"\n💾 가격 이력 저장: {history_filename}")
        
        if changes:
            change_df = pd.DataFrame(changes)
            change_filename = f"가격변동_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
            
            with pd.ExcelWriter(change_filename, engine='openpyxl') as writer:
                change_df.to_excel(writer, index=False, sheet_name='가격변동')
                updated_df.to_excel(writer, index=False, sheet_name='전체데이터')
            
            print(f"\n🔔 가격 변동 감지! {len(changes)}개 항목")
            print(f"💾 변동 내역 저장: {change_filename}")
            print("\n📊 변동 내역:")
            for change in changes[:10]:
                print(f"   {change['변동']} {change['상품명']} {change['옵션명']}")
                print(f"      {change['이전가격']} → {change['현재가격']}")
            
            if len(changes) > 10:
                print(f"   ... 외 {len(changes)-10}개")
        else:
            print("\n✅ 가격 변동 없음!")
            updated_df.to_excel(current_filename, index=False, engine='openpyxl')
            print(f"💾 현재 데이터 저장: {current_filename}")
    
    def close(self):
        self.driver.quit()
        print("\n🏁 작업 종료!")

