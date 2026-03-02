import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import glob
import re

# 페이지 설정
st.set_page_config(
    page_title="🍎 B2B 가격 비교 대시보드",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사이트 메인 URL 매핑
SITE_URLS = {
    '팡이농장': 'https://jaehwan0330.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
    '최고집': 'https://zain0401.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
    '늘푸른우리': 'https://hwanggs3.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
    '팜허브': 'https://priceit.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
    '덤덤몰': 'https://dumdummall.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
    '제주농산물(마니팜)': 'https://mp3462.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
    '산지이음': 'https://orangec.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
    '캄뮤유통': 'https://ehrtnfl20002.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
    '농부를 찾아서': 'https://ongreen.adminplus.co.kr/partner/?mod=product&actpage=prt.list'
}

# 데이터 로드 함수
@st.cache_data
def load_latest_data():
    """최신 데이터 파일 로드"""
    try:
        # 다중사이트 및 가격변동 파일 찾기
        files = glob.glob("다중사이트_*.xlsx") + glob.glob("가격변동_*.xlsx")
        
        if not files:
            st.error("📂 데이터 파일을 찾을 수 없습니다!")
            return None, None
        
        # 가장 최근 파일
        latest_file = max(files, key=os.path.getmtime)
        
        # 시트가 여러 개면 '전체데이터' 시트 읽기
        try:
            df = pd.read_excel(latest_file, sheet_name='전체데이터')
        except:
            df = pd.read_excel(latest_file)
        
        # 공급가를 숫자로 변환
        if '공급가' in df.columns:
            df['공급가_숫자'] = df['공급가'].astype(str).str.replace('￦', '').str.replace(',', '').str.replace('~', '').str.replace('부터(옵션별차등)', '').str.split().str[0]
            df['공급가_숫자'] = pd.to_numeric(df['공급가_숫자'], errors='coerce')
        
        # 사이트 메인 URL 추가
        if '사이트명' in df.columns:
            df['사이트_메인URL'] = df['사이트명'].map(SITE_URLS)
        
        return df, latest_file
        
    except Exception as e:
        st.error(f"❌ 데이터 로드 실패: {e}")
        return None, None

# 데이터 로드
result = load_latest_data()
if result is None or result[0] is None:
    st.stop()

df, latest_file = result

# 메인 타이틀
st.title("🍎 B2B 가격 비교 대시보드")
st.markdown(f"**📊 로드된 파일:** `{os.path.basename(latest_file)}` | **총 {len(df):,}개 항목**")
st.markdown("---")

# 사이드바
st.sidebar.markdown("# 🍎 가격 비교")
st.sidebar.markdown("---")
st.sidebar.header("🔍 필터 옵션")

# 사이트 필터
if '사이트명' in df.columns:
    sites = ['전체'] + sorted(df['사이트명'].dropna().unique().tolist())
    selected_site = st.sidebar.selectbox("📍 사이트 선택", sites)
else:
    selected_site = '전체'

# 키워드 필터
if '키워드' in df.columns:
    keywords = ['전체'] + sorted(df['키워드'].dropna().unique().tolist())
    selected_keyword = st.sidebar.selectbox("🔑 키워드 선택", keywords)
else:
    selected_keyword = '전체'

# 가격 범위 필터
if '공급가_숫자' in df.columns and df['공급가_숫자'].notna().sum() > 0:
    min_price = int(df['공급가_숫자'].min())
    max_price = int(df['공급가_숫자'].max())
    price_range = st.sidebar.slider(
        "💰 가격 범위",
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price),
        step=1000
    )
else:
    price_range = (0, 999999999)

# 데이터 필터링
filtered_df = df.copy()

if selected_site != '전체' and '사이트명' in df.columns:
    filtered_df = filtered_df[filtered_df['사이트명'] == selected_site]

if selected_keyword != '전체' and '키워드' in df.columns:
    filtered_df = filtered_df[filtered_df['키워드'] == selected_keyword]

if '공급가_숫자' in df.columns:
    filtered_df = filtered_df[
        (filtered_df['공급가_숫자'] >= price_range[0]) &
        (filtered_df['공급가_숫자'] <= price_range[1])
    ]

# 새로고침 버튼
if st.sidebar.button("🔄 데이터 새로고침"):
    st.cache_data.clear()
    st.rerun()

# 메트릭 카드
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📦 총 상품 수", f"{len(filtered_df):,}개")

with col2:
    if '사이트명' in filtered_df.columns:
        st.metric("🏪 사이트 수", f"{filtered_df['사이트명'].nunique()}개")
    else:
        st.metric("🏪 사이트 수", "N/A")

with col3:
    if '공급가_숫자' in filtered_df.columns and filtered_df['공급가_숫자'].notna().sum() > 0:
        avg_price = filtered_df['공급가_숫자'].mean()
        st.metric("💰 평균 가격", f"{avg_price:,.0f}원")
    else:
        st.metric("💰 평균 가격", "N/A")

with col4:
    if '공급가_숫자' in filtered_df.columns and filtered_df['공급가_숫자'].notna().sum() > 0:
        min_price_val = filtered_df['공급가_숫자'].min()
        st.metric("🔥 최저 가격", f"{min_price_val:,.0f}원")
    else:
        st.metric("🔥 최저 가격", "N/A")

st.markdown("---")

# 탭 생성
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 키워드별 도매처 가격 비교",
    "🏪 사이트별 분석",
    "🔥 최저가 TOP 10",
    "📈 가격 변동",
    "📋 전체 데이터"
])

# 탭 1: 키워드별 도매처 가격 비교
with tab1:
    st.header("📊 키워드별 도매처 가격 비교")
    
    if selected_keyword == '전체':
        st.info("💡 왼쪽 사이드바에서 키워드를 선택하세요!")
    else:
        keyword_data = filtered_df[filtered_df['키워드'] == selected_keyword] if '키워드' in filtered_df.columns else filtered_df
        
        if len(keyword_data) > 0 and '사이트명' in keyword_data.columns and '공급가_숫자' in keyword_data.columns:
            # 사이트별 평균 가격
            site_avg = keyword_data.groupby('사이트명')['공급가_숫자'].mean().sort_values()
            
            fig1 = px.bar(
                x=site_avg.values,
                y=site_avg.index,
                orientation='h',
                title=f"{selected_keyword} - 도매처별 평균 가격",
                labels={'x': '평균 가격 (원)', 'y': '도매처'},
                color=site_avg.values,
                color_continuous_scale='RdYlGn_r'
            )
            fig1.update_layout(showlegend=False, height=500)
            st.plotly_chart(fig1, use_container_width=True)
            
            # 사이트별 최저가 테이블
            st.subheader(f"💰 {selected_keyword} - 도매처별 최저가")
            
            site_min = keyword_data.groupby('사이트명').apply(
                lambda x: x.nsmallest(1, '공급가_숫자')[['상품명', '옵션명', '공급가_숫자', '상세URL']].iloc[0]
            ).reset_index()
            
            for _, row in site_min.iterrows():
                with st.expander(f"🏪 {row['사이트명']} - {row['공급가_숫자']:,.0f}원"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**상품명:** {row['상품명']}")
                        if pd.notna(row['옵션명']):
                            st.write(f"**옵션:** {row['옵션명']}")
                    with col2:
                        st.metric("가격", f"{row['공급가_숫자']:,.0f}원")
                    
                    if pd.notna(row['상세URL']):
                        st.markdown(f"[🔗 상세 페이지]({row['상세URL']})")
                    
                    # 사이트 메인 URL 추가
                    if row['사이트명'] in SITE_URLS:
                        st.markdown(f"[🏪 {row['사이트명']} 전체 상품 보기]({SITE_URLS[row['사이트명']]})")
        else:
            st.warning(f"⚠️ {selected_keyword}에 대한 데이터가 없습니다.")

# 탭 2: 사이트별 분석
with tab2:
    st.header("🏪 사이트별 분석")
    
    if selected_keyword == '전체':
        st.info("💡 왼쪽 사이드바에서 키워드를 선택하면 해당 키워드의 사이트별 분석을 볼 수 있습니다!")
        
        # 전체 키워드일 때는 상품 개수만 표시
        if '사이트명' in filtered_df.columns:
            site_count = filtered_df['사이트명'].value_counts()
            
            fig = px.pie(
                values=site_count.values,
                names=site_count.index,
                title="사이트별 전체 상품 비중",
                hole=0.4
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
    else:
        keyword_data = filtered_df[filtered_df['키워드'] == selected_keyword] if '키워드' in filtered_df.columns else filtered_df
        
        if len(keyword_data) > 0 and '사이트명' in keyword_data.columns and '공급가_숫자' in keyword_data.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                # 사이트별 평균 가격
                site_avg = keyword_data.groupby('사이트명')['공급가_숫자'].mean().sort_values(ascending=False)
                
                fig3 = px.bar(
                    x=site_avg.values,
                    y=site_avg.index,
                    orientation='h',
                    title=f"{selected_keyword} - 사이트별 평균 가격",
                    labels={'x': '평균 가격 (원)', 'y': '사이트'},
                    color=site_avg.values,
                    color_continuous_scale='Blues'
                )
                fig3.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig3, use_container_width=True)
            
            with col2:
                # 사이트별 상품 비중
                site_count = keyword_data['사이트명'].value_counts()
                
                fig4 = px.pie(
                    values=site_count.values,
                    names=site_count.index,
                    title=f"{selected_keyword} - 사이트별 상품 비중",
                    hole=0.4
                )
                fig4.update_layout(height=400)
                st.plotly_chart(fig4, use_container_width=True)
        else:
            st.warning(f"⚠️ {selected_keyword}에 대한 데이터가 없습니다.")

# 탭 3: 최저가 TOP 10
with tab3:
    st.header("🔥 최저가 TOP 10")
    
    if '키워드' in filtered_df.columns and '공급가_숫자' in filtered_df.columns and filtered_df['공급가_숫자'].notna().sum() > 0:
        # 전체 데이터에서 최저가 10개
        top10_df = filtered_df.nsmallest(10, '공급가_숫자')
        
        for idx, row in top10_df.iterrows():
            with st.expander(f"🏆 {row.get('키워드', 'N/A')} - {row['공급가_숫자']:,.0f}원"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    if '상품명' in row and pd.notna(row['상품명']):
                        st.write(f"**상품명:** {row['상품명']}")
                    if '사이트명' in row and pd.notna(row['사이트명']):
                        st.write(f"**사이트:** {row['사이트명']}")
                    if '옵션명' in row and pd.notna(row['옵션명']):
                        st.write(f"**옵션:** {row['옵션명']}")
                with col2:
                    st.metric("가격", f"{row['공급가_숫자']:,.0f}원")
                
                if '상세URL' in row and pd.notna(row['상세URL']):
                    st.markdown(f"[🔗 상세 페이지]({row['상세URL']})")
                
                # 사이트 메인 URL 추가
                if '사이트명' in row and row['사이트명'] in SITE_URLS:
                    st.markdown(f"[🏪 {row['사이트명']} 전체 상품 보기]({SITE_URLS[row['사이트명']]})")
    else:
        st.warning("⚠️ 최저가 정보를 표시할 데이터가 부족합니다.")

# 탭 4: 가격 변동
with tab4:
    st.header("📈 가격 변동")
    
    # 가격변동 파일 찾기
    change_files = glob.glob("가격변동_*.xlsx")
    
    if change_files:
        latest_change_file = max(change_files, key=os.path.getmtime)
        try:
            # 가격변동 시트 읽기
            change_df = pd.read_excel(latest_change_file, sheet_name='가격변동')
            
            st.markdown(f"**📊 파일:** `{os.path.basename(latest_change_file)}` | **총 {len(change_df):,}개 항목**")
            
            # 사이트명이 없으면 추가 시도
            if '사이트명' not in change_df.columns:
                st.warning("⚠️ 가격변동 파일에 사이트명이 없습니다.")
            else:
                # 변동 유형별 필터
                if '변동유형' in change_df.columns:
                    change_types = ['전체'] + change_df['변동유형'].dropna().unique().tolist()
                    selected_change = st.selectbox("📊 변동 유형", change_types)
                    
                    if selected_change != '전체':
                        change_df = change_df[change_df['변동유형'] == selected_change]
            
            # 컬럼 순서 조정 (사이트명을 앞으로)
            cols = change_df.columns.tolist()
            if '사이트명' in cols:
                cols.remove('사이트명')
                cols = ['사이트명'] + cols
                change_df = change_df[cols]
            
            st.dataframe(change_df, use_container_width=True, height=500)
            
        except Exception as e:
            st.error(f"❌ 가격 변동 파일 로드 실패: {e}")
    else:
        st.info("💡 가격 변동 파일이 없습니다. 두 번째 수집부터 가격 변동이 기록됩니다!")

# 탭 5: 전체 데이터
with tab5:
    st.header("📋 전체 데이터")
    
    # 검색 기능
    search_term = st.text_input("🔍 상품명 검색", "")
    
    display_df = filtered_df.copy()
    
    if search_term:
        # 모든 텍스트 컬럼에서 검색
        mask = display_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        display_df = display_df[mask]
    
    # 컬럼 순서 조정
    cols = display_df.columns.tolist()
    # 사이트_메인URL을 사이트명 바로 뒤로
    if '사이트_메인URL' in cols and '사이트명' in cols:
        cols.remove('사이트_메인URL')
        site_idx = cols.index('사이트명')
        cols.insert(site_idx + 1, '사이트_메인URL')
        display_df = display_df[cols]
    
    # 데이터 표시
    st.dataframe(display_df, use_container_width=True, height=600, column_config={
        '상세URL': st.column_config.LinkColumn('상세URL', display_text='🔗 상세보기'),
        '사이트_메인URL': st.column_config.LinkColumn('사이트 전체상품', display_text='🏪 사이트')
    })
    
    # CSV 다운로드
    csv = display_df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 CSV 다운로드",
        data=csv,
        file_name=f"가격데이터_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv"
    )

# 푸터
st.markdown("---")
st.markdown("**🍎 B2B 가격 비교 대시보드** | Powered by Streamlit")
