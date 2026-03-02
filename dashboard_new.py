import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import glob

# 페이지 설정
st.set_page_config(
    page_title="🍎 B2B 가격 비교 대시보드",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 데이터 로드 함수
@st.cache_data
def load_latest_data():
    """최신 다중사이트 엑셀 파일 로드"""
    try:
        # 다중사이트 파일만 찾기
        files = glob.glob("다중사이트_*.xlsx")
        
        if not files:
            st.error("📂 다중사이트 파일을 찾을 수 없습니다!")
            return None, None
        
        # 가장 최근 파일
        latest_file = max(files, key=os.path.getmtime)
        
        # 엑셀 읽기
        df = pd.read_excel(latest_file)
        
        # 공급가를 숫자로 변환
        if '공급가' in df.columns:
            df['공급가_숫자'] = df['공급가'].astype(str).str.replace('￦', '').str.replace(',', '').str.replace('~', '').str.replace('부터(옵션별차등)', '').str.split().str[0]
            df['공급가_숫자'] = pd.to_numeric(df['공급가_숫자'], errors='coerce')
        
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
    "📊 가격 비교",
    "🏪 사이트별 분석",
    "🔥 최저가 TOP 10",
    "📈 가격 변동",
    "📋 전체 데이터"
])

# 탭 1: 가격 비교
with tab1:
    st.header("📊 키워드별 가격 비교")
    
    if '키워드' in filtered_df.columns and '공급가_숫자' in filtered_df.columns and filtered_df['공급가_숫자'].notna().sum() > 0:
        # 키워드별 평균 가격
        keyword_avg = filtered_df.groupby('키워드')['공급가_숫자'].mean().sort_values(ascending=False)
        
        if len(keyword_avg) > 0:
            fig1 = px.bar(
                x=keyword_avg.values,
                y=keyword_avg.index,
                orientation='h',
                title="키워드별 평균 가격",
                labels={'x': '평균 가격 (원)', 'y': '키워드'},
                color=keyword_avg.values,
                color_continuous_scale='Viridis'
            )
            fig1.update_layout(showlegend=False, height=500)
            st.plotly_chart(fig1, use_container_width=True)
            
            # 가격 분포 박스 플롯
            fig2 = px.box(
                filtered_df,
                x='키워드',
                y='공급가_숫자',
                title="키워드별 가격 분포",
                labels={'공급가_숫자': '가격 (원)', '키워드': '키워드'},
                color='키워드'
            )
            fig2.update_layout(height=500)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("📊 해당 조건의 데이터가 없습니다.")
    else:
        st.warning("⚠️ 가격 비교를 위한 데이터가 부족합니다.")

# 탭 2: 사이트별 분석
with tab2:
    st.header("🏪 사이트별 분석")
    
    if '사이트명' in filtered_df.columns and '공급가_숫자' in filtered_df.columns and filtered_df['공급가_숫자'].notna().sum() > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            # 사이트별 평균 가격
            site_avg = filtered_df.groupby('사이트명')['공급가_숫자'].mean().sort_values(ascending=False)
            
            if len(site_avg) > 0:
                fig3 = px.bar(
                    x=site_avg.values,
                    y=site_avg.index,
                    orientation='h',
                    title="사이트별 평균 가격",
                    labels={'x': '평균 가격 (원)', 'y': '사이트'},
                    color=site_avg.values,
                    color_continuous_scale='Blues'
                )
                fig3.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig3, use_container_width=True)
        
        with col2:
            # 사이트별 상품 비중
            site_count = filtered_df['사이트명'].value_counts()
            
            if len(site_count) > 0:
                fig4 = px.pie(
                    values=site_count.values,
                    names=site_count.index,
                    title="사이트별 상품 비중",
                    hole=0.4
                )
                fig4.update_layout(height=400)
                st.plotly_chart(fig4, use_container_width=True)
    else:
        st.warning("⚠️ 사이트별 분석을 위한 데이터가 부족합니다.")

# 탭 3: 최저가 TOP 10
with tab3:
    st.header("🔥 최저가 TOP 10")
    
    if '키워드' in filtered_df.columns and '공급가_숫자' in filtered_df.columns and filtered_df['공급가_숫자'].notna().sum() > 0:
        # 키워드별 최저가 찾기
        top10_df = filtered_df.sort_values('공급가_숫자').groupby('키워드').first().reset_index()
        top10_df = top10_df.nsmallest(10, '공급가_숫자')
        
        for idx, row in top10_df.iterrows():
            with st.expander(f"🏆 {row['키워드']} - {row['공급가_숫자']:,.0f}원"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    if '상품명' in row:
                        st.write(f"**상품명:** {row['상품명']}")
                    if '사이트명' in row:
                        st.write(f"**사이트:** {row['사이트명']}")
                    if '옵션명' in row and pd.notna(row['옵션명']):
                        st.write(f"**옵션:** {row['옵션명']}")
                with col2:
                    st.metric("가격", f"{row['공급가_숫자']:,.0f}원")
                
                if '상세URL' in row and pd.notna(row['상세URL']):
                    st.markdown(f"[🔗 상세 페이지 보기]({row['상세URL']})")
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
            change_df = pd.read_excel(latest_change_file)
            
            st.markdown(f"**📊 파일:** `{os.path.basename(latest_change_file)}` | **총 {len(change_df):,}개 항목**")
            
            # 변동 유형별 필터
            if '변동유형' in change_df.columns:
                change_types = ['전체'] + change_df['변동유형'].dropna().unique().tolist()
                selected_change = st.selectbox("📊 변동 유형", change_types)
                
                if selected_change != '전체':
                    change_df = change_df[change_df['변동유형'] == selected_change]
            
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
    
    if search_term and '상품명' in display_df.columns:
        display_df = display_df[display_df['상품명'].str.contains(search_term, case=False, na=False)]
    
    # 상세URL을 클릭 가능한 링크로 변환
    if '상세URL' in display_df.columns:
        # 링크 표시용 DataFrame
        display_columns = [col for col in display_df.columns if col != '상세URL'] + ['상세URL']
        display_df = display_df[display_columns]
    
    # 데이터 표시
    st.dataframe(display_df, use_container_width=True, height=600, column_config={
        '상세URL': st.column_config.LinkColumn('상세URL', display_text='🔗 보기')
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
