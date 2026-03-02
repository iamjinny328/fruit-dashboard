"""
수집 후 구글 드라이브에 직접 저장
- 로컬 저장 없음
- 바로 구글 드라이브 업로드
"""

from price_collector import B2BPriceCollector
from config import SITES, MAX_PAGES, FILTER_KEYWORDS, ENABLE_PRICE_CHANGE_ALERT, PRICE_HISTORY_FILE
from datetime import datetime
import traceback
import os
import tempfile

# 구글 드라이브 업로더 임포트
from google_drive_uploader import GoogleDriveUploader

def main():
    collector = B2BPriceCollector()
    uploaded_files = []
    
    try:
        print("=" * 50)
        print("🍎 B2B 가격 수집 → 구글 드라이브 직접 저장")
        print("=" * 50)
        print(f"🔍 관심 키워드: {', '.join(FILTER_KEYWORDS) if FILTER_KEYWORDS else '전체'}")
        print(f"📄 페이지 제한: {MAX_PAGES}페이지" if MAX_PAGES else "📄 페이지 제한: 전체")
        print(f"📊 가격 변동 감지: {'ON ✅' if ENABLE_PRICE_CHANGE_ALERT else 'OFF'}")
        print("=" * 50)
        print()

        # 로그인 및 수집
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
                collector.collect_product_list(
                    site_name=site_name,
                    list_url=site_config['list_url'],
                    selectors=site_config['product_selectors']
                )

        # 결과 저장 (임시 파일로)
        if collector.results:
            # 임시 파일명
            temp_filename = f"다중사이트_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
            
            print(f"\n💾 임시 파일 생성: {temp_filename}")
            
            if ENABLE_PRICE_CHANGE_ALERT:
                collector.save_with_change_detection(temp_filename, PRICE_HISTORY_FILE)
            else:
                collector.save_excel(temp_filename)
            
            # 🚀 구글 드라이브 업로드
            if os.path.exists(temp_filename):
                print("\n" + "=" * 50)
                print("📤 구글 드라이브 업로드 중...")
                print("=" * 50)
                
                try:
                    # 업로더 초기화
                    uploader = GoogleDriveUploader()
                    
                    # 폴더 확인/생성
                    folder_id = uploader.find_folder('과일가격수집_데이터')
                    if not folder_id:
                        print("📁 폴더 생성 중...")
                        folder_id = uploader.create_folder('과일가격수집_데이터')
                    
                    # 파일 업로드
                    file_info = uploader.upload_file(
                        temp_filename, 
                        folder_id, 
                        share_with_anyone=True
                    )
                    
                    uploaded_files.append(file_info)
                    
                    print("\n✅ 구글 드라이브 저장 완료!")
                    print(f"🔗 공유 링크: {file_info['webViewLink']}")
                    
                    # 로컬 임시 파일 삭제
                    os.remove(temp_filename)
                    print(f"🗑️  로컬 임시 파일 삭제: {temp_filename}")
                    
                except Exception as e:
                    print(f"\n⚠️  구글 드라이브 업로드 실패: {e}")
                    print(f"📁 로컬 파일 유지: {temp_filename}")
                    traceback.print_exc()
        else:
            print("\n⚠️  수집된 데이터가 없습니다!")
            print("🔍 keywords.txt 파일을 확인해주세요!")
    
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        traceback.print_exc()
    
    finally:
        collector.close()
        
        # 업로드 요약
        if uploaded_files:
            print("\n" + "=" * 50)
            print("📊 구글 드라이브 저장 완료")
            print("=" * 50)
            for file in uploaded_files:
                print(f"✅ {file['name']}")
                print(f"   🔗 {file['webViewLink']}")
            print("=" * 50)
            print("\n💡 대시보드 실행: streamlit run dashboard_gdrive.py")

if __name__ == "__main__":
    main()