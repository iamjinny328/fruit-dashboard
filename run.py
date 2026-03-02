from price_collector import B2BPriceCollector
from config import SITES, LIST_PAGE_URL, PRODUCT_SELECTORS
from datetime import datetime
import traceback

def main():
    collector = B2BPriceCollector()
    
    try:
        # 각 사이트 로그인
        for site_name, site_config in SITES.items():
            success = collector.login(
                site_name=site_name,
                login_url=site_config['login_url'],
                username=site_config['username'],
                password=site_config['password'],
                username_selector=site_config['selectors']['username'],
                password_selector=site_config['selectors']['password'],
                login_button_selector=site_config['selectors']['login_button']
            )
            
            if success:
                # 상품 리스트 수집
                collector.collect_product_list(
                    site_name=site_name,
                    list_url=LIST_PAGE_URL,
                    selectors=PRODUCT_SELECTORS
                )
        
        # 엑셀 저장
        if collector.results:
            filename = f"늘푸른우리_전체상품_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
            collector.save_excel(filename)
            print(f"\n✨ 모든 작업 완료! {filename} 파일을 확인하세요!")
        else:
            print("\n⚠️ 수집된 데이터가 없습니다!")
            
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        traceback.print_exc()
    
    finally:
        collector.close()

if __name__ == "__main__":
    main()
