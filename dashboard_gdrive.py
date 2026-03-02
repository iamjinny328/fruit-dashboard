"""
구글 드라이브 연동 대시보드
- 구글 드라이브에서 최신 Excel 파일 자동 다운로드
- 여러 사람이 동시에 접근 가능
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import tempfile
from datetime import datetime

# 구글 드라이브 업로더 임포트
from google_drive_uploader import GoogleDriveUploader

# 페이지 설정
st.set_page_config(page_title="B2B 가격 비교 대시보드", page_icon="🍎", layout="wide")

# 캐시: 구글 드라이브 파일 목록
@st.cache_data(ttl=300)  # 5분마다 갱신
def get_drive_files():
    """구글 드라이브에서 파일 목록 가져오기"""
    try:
        uploader = GoogleDriveUploader()
        folder_id = uploader.find_folder('과일가격수집_데이터')
        if folder_id:
            files = uploader.list_files(folder_id, max_results=50)
            # Excel 파일만 필터링
            excel_files = [f for f in files if f['name'].endswith('.xlsx')]
            return excel_files, uploader, folder_id
        return [], None, None
    except Exception as e:
        st.error(f"❌ 구글 드라이브 연결 실패: {e}")
        return [], None, None

# 캐시: 파일 다운로드 및 로드
@st.cache_data(ttl=600)  # 10분마다 갱신
def load_data_from_drive(file_id, file_name):
    """구글 드라이브에서 파일 다운로드 후 로드"""
    try:
        uploader = GoogleDriveUploader()
        
        # 임시 파일로 다운로드
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
            uploader.download_file(file_id, tmp.name)
            
            # Excel 읽기
            try:
                df = pd.read_excel(tmp.name, sheet_name='전체데이터')
            except:
                df = pd.read_excel(tmp.name)
            
            
           # 임시 파일 삭제 (에러 무시)
            try:
                tmp.close()
                os.unlink(tmp.name)
            except:
                pass

            
            return df, file_name
    except Exception as e:
        st.error(f"❌ 파일 로드 실패: {e}")
        return None, None

# 사이트 메인 URL 매핑
SITE_MAIN_URLS = {
    '팡이농장': 'https://jaehwan0330.adminplus.co.kr/partner/',
    '최고집': 'https://zain0401.adminplus.co.kr/partner/',
    '늘푸른우리': 'https://hwanggs3.adminplus.co.kr/partner/',
    '팜허브': 'https://priceit.adminplus.co.kr/partner/',
    '덤덤몰': 'https://dumdummall.adminplus.co.kr/partner/',
    '제주농산물(마니팜)': 'https://mp3462.adminplus.co.kr/partner/',
    '산지이음': 'https://orangec.adminplus.co.kr/partner/',
    '캄뮤유통': 'https://ehrtnfl20002.adminplus.co.kr/partner/',
    '농부를 찾아서': 'https://ongreen.adminplus.co.kr/partner/'
}

# 타이틀
st.title("🍎 B2B 가격 비교 대시보드 (구글 드라이브 연동)")

# 사이드바: 구글 드라이브 파일 선택
with st.sidebar:
    st.header("📂 데이터 소스")
    
    # 새로고침 버튼
    if st.button("🔄 파일 목록 새로고침"):
        st.cache_data.clear()
        st.rerun()
    
    # 파일 목록 가져오기
    excel_files, uploader, folder_id = get_drive_files()
    
    if not excel_files:
        st.warning("⚠️  구글 드라이브에 파일이 없습니다.")
        st.info("💡 먼저 `python run_quick_with_upload.py`를 실행하세요.")
        st.stop()
    
    # 파일 선택
    file_names = [f['name'] for f in excel_files]
    selected_file_name = st.selectbox(
        "📊 파일 선택",
        file_names,
        index=0  # 최신 파일 (맨 위)
    )
    
    # 선택된 파일 ID
    selected_file_id = next(f['id'] for f in excel_files if f['name'] == selected_file_name)
    
    st.success(f"✅ 선택된 파일: {selected_file_name}")

# 데이터 로드
df, loaded_file = load_data_from_drive(selected_file_id, selected_file_name)

if df is None or df.empty:
    st.error("❌ 데이터를 불러올 수 없습니다.")
    st.stop()

# 가격 숫자 변환
if '공급가' in df.columns:
    df['공급가_숫자'] = df['공급가'].astype(str).str.replace(r'[^\d]', '', regex=True)
    df['공급가_숫자'] = pd.to_numeric(df['공급가_숫자'], errors='coerce')

# 메트릭 카드
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📦 총 상품 수", f"{len(df):,}개")
with col2:
    if '사이트명' in df.columns:
        st.metric("🏪 사이트 수", f"{df['사이트명'].nunique()}개")
    else:
        st.metric("🏪 사이트 수", "해당 없음")
with col3:
    if '공급가_숫자' in df.columns:
        avg_price = df['공급가_숫자'].mean()
        st.metric("💰 평균 가격", f"₩{avg_price:,.0f}" if pd.notna(avg_price) else "해당 없음")
    else:
        st.metric("💰 평균 가격", "해당 없음")
with col4:
    if '공급가_숫자' in df.columns:
        min_price = df['공급가_숫자'].min()
        st.metric("🔻 최저 가격", f"₩{min_price:,.0f}" if pd.notna(min_price) else "해당 없음")
    else:
        st.metric("🔻 최저 가격", "해당 없음")

# 사이드바 필터
with st.sidebar:
    st.header("🔍 필터")
    
    # 사이트 선택
    if '사이트명' in df.columns:
        sites = ['전체'] + sorted(df['사이트명'].dropna().unique().tolist())
        selected_site = st.selectbox("🏪 사이트 선택", sites)
    else:
        selected_site = '전체'
    
    # 키워드 선택
    if '키워드' in df.columns:
        keywords = ['전체'] + sorted(df['키워드'].dropna().unique().tolist())
        selected_keyword = st.selectbox("🔍 키워드 선택", keywords)
    else:
        selected_keyword = '전체'
    
    # 가격 범위
    if '공급가_숫자' in df.columns and df['공급가_숫자'].notna().any():
        min_val = int(df['공급가_숫자'].min())
        max_val = int(df['공급가_숫자'].max())
        price_range = st.slider("💰 가격 범위", min_val, max_val, (min_val, max_val))
    else:
        price_range = None

# 필터 적용
filtered_df = df.copy()
if selected_site != '전체' and '사이트명' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['사이트명'] == selected_site]
if selected_keyword != '전체' and '키워드' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['키워드'] == selected_keyword]
if price_range and '공급가_숫자' in filtered_df.columns:
    filtered_df = filtered_df[
        (filtered_df['공급가_숫자'] >= price_range[0]) &
        (filtered_df['공급가_숫자'] <= price_range[1])
    ]

# 탭 생성
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 가격 비교", 
    "📈 사이트별 분석", 
    "🏆 최저가 TOP 10",
    "📉 가격 변동",
    "📋 전체 데이터"
])

# 탭 1: 가격 비교
with tab1:
    st.subheader("📊 키워드별 도매처 가격 비교")
    
    if selected_keyword == '전체':
        st.info("💡 왼쪽 사이드바에서 키워드를 선택하세요.")
    else:
        keyword_df = filtered_df[filtered_df['키워드'] == selected_keyword] if '키워드' in filtered_df.columns else filtered_df
        
        if not keyword_df.empty and '사이트명' in keyword_df.columns and '공급가_숫자' in keyword_df.columns:
            site_avg = keyword_df.groupby('사이트명')['공급가_숫자'].mean().reset_index()
            site_avg = site_avg.sort_values('공급가_숫자')
            
            fig = px.bar(
                site_avg,
                x='사이트명',
                y='공급가_숫자',
                title=f"'{selected_keyword}' 도매처별 평균 가격",
                labels={'공급가_숫자': '평균 가격 (원)', '사이트명': '도매처'},
                color='공급가_숫자',
                color_continuous_scale='RdYlGn_r'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # 최저가 강조
            min_site = site_avg.iloc[0]
            st.success(f"🏆 최저가: **{min_site['사이트명']}** - ₩{min_site['공급가_숫자']:,.0f}")
        else:
            st.warning("⚠️  해당 키워드의 데이터가 없습니다.")

# 탭 2: 사이트별 분석
with tab2:
    st.subheader("📈 사이트별 상품 수 & 평균 가격")
    
    if '사이트명' in filtered_df.columns and '공급가_숫자' in filtered_df.columns:
        site_stats = filtered_df.groupby('사이트명').agg({
            '상품명': 'count',
            '공급가_숫자': 'mean'
        }).reset_index()
        site_stats.columns = ['사이트명', '상품 수', '평균 가격']
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=site_stats['사이트명'], y=site_stats['상품 수'], name='상품 수', yaxis='y'))
        fig.add_trace(go.Scatter(x=site_stats['사이트명'], y=site_stats['평균 가격'], name='평균 가격', yaxis='y2', mode='lines+markers'))
        
        fig.update_layout(
            title="사이트별 상품 수 & 평균 가격",
            yaxis=dict(title='상품 수'),
            yaxis2=dict(title='평균 가격 (원)', overlaying='y', side='right')
        )
        st.plotly_chart(fig, use_container_width=True)

# 탭 3: 최저가 TOP 10
with tab3:
    st.subheader("🏆 최저가 TOP 10")
    
    if '공급가_숫자' in filtered_df.columns:
        top10 = filtered_df.nsmallest(10, '공급가_숫자')
        
        for idx, row in top10.iterrows():
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"### {row.get('상품명', '이름 없음')}")
                    st.markdown(f"**장소:** {row.get('사이트명', '해당 없음')}")
                    st.markdown(f"**옵션:** {row.get('옵션명', '옵션 없음')}")
                with col2:
                    st.metric("가격", f"₩{row['공급가_숫자']:,.0f}")
                
                # 링크
                col_link1, col_link2 = st.columns(2)
                with col_link1:
                    if '상세URL' in row and pd.notna(row['상세URL']):
                        st.markdown(f"🔗 [상세 페이지 보기]({row['상세URL']})")
                with col_link2:
                    site_name = row.get('사이트명', '')
                    if site_name in SITE_MAIN_URLS:
                        st.markdown(f"🏠 [사이트 메인]({SITE_MAIN_URLS[site_name]})")
                
                st.divider()

# 탭 4: 가격 변동
with tab4:
    st.subheader("📉 가격 변동 내역")
    st.info("💡 가격 변동 파일이 있으면 여기에 표시됩니다.")
    # TODO: 가격 변동 시트 읽기 추가

# 탭 5: 전체 데이터
with tab5:
    st.subheader("📋 전체 데이터")
    
    # 검색
    search_term = st.text_input("🔍 검색 (모든 컬럼)", "")
    
    display_df = filtered_df.copy()
    
    if search_term:
        mask = display_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        display_df = display_df[mask]
    
    st.dataframe(display_df, use_container_width=True, height=600)
    
    # CSV 다운로드
    csv = display_df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 CSV 다운로드",
        data=csv,
        file_name=f"가격데이터_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# 푸터
st.markdown("---")
st.caption(f"📊 데이터 소스: 구글 드라이브 - {loaded_file} | 마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
