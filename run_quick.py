from price_collector import B2BPriceCollector
from config import SITES, MAX_PAGES, FILTER_KEYWORDS, ENABLE_PRICE_CHANGE_ALERT, PRICE_HISTORY_FILE
from datetime import datetime
import traceback

def main():
    collector = B2BPriceCollector()
    
    try:
        print("=" * 50)
        print("⚡⚡⚡ 빠른 체크 모드 ⚡⚡⚡")
        print("=" * 50)
        print(f"📌 관심 품목: {', '.join(FILTER_KEYWORDS) if FILTER_KEYWORDS else '전체'}")
        print(f"📌 페이지 제한: {MAX_PAGES}페이지" if MAX_PAGES else "📌 페이지 제한: 전체")
        print(f"📌 가격 변동 감지: {'ON ✅' if ENABLE_PRICE_CHANGE_ALERT else 'OFF'}")
        print("=" * 50)
        print()
        
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
                # 상세 수집 모드 (필터링 + 페이지 제한)
                collector.collect_product_list(
                    site_name=site_name,
                    list_url=site_config['list_url'],
                    selectors=site_config['product_selectors']
                )

        
        # 엑셀 저장
        if collector.results:
            if ENABLE_PRICE_CHANGE_ALERT:
                # 가격 변동 감지 모드
                current_filename = f"현재가격_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
                collector.save_with_change_detection(current_filename, PRICE_HISTORY_FILE)
            else:
                # 일반 저장
                filename = f"빠른체크_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
                collector.save_excel(filename)
                print(f"\n✨ 빠른 체크 완료! {filename} 파일을 확인하세요!")
        else:
            print("\n⚠️ 수집된 데이터가 없습니다!")
            print("💡 FILTER_KEYWORDS 설정을 확인해주세요!")
            
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        traceback.print_exc()
    
    finally:
        collector.close()

if __name__ == "__main__":
    main()
