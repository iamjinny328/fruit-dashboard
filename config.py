# ========================================
# 공통 로그인 정보 (모든 사이트 동일)
# ========================================
COMMON_USERNAME = 'friendship160930'
COMMON_PASSWORD = 'kmgss11ss!@'

# ========================================
# AdminPlus 계열 B2B 사이트 설정
# ========================================

SITES = {
    '팡이농장': {
        'login_url': 'https://jaehwan0330.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
        'username': COMMON_USERNAME,
        'password': COMMON_PASSWORD,
        'selectors': {
            'username': '#memid',
            'password': '#admpwd',
            'login_button': 'button[type="submit"]'
        },
        'list_url': 'https://jaehwan0330.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
        'product_selectors': {
            'item_container': 'div[onclick^="prtView"]',
            'product_name': '.pname',
            'price': '.sp_tbl tr:nth-child(1) td',
            'shipping': '.sp_tbl tr:nth-child(2) td'
        },
        'detail_url_pattern': 'https://jaehwan0330.adminplus.co.kr/partner/product/prt.{type}.detail.pop.php?pcode={pcode}'
    },

    '최고집': {
        'login_url': 'https://zain0401.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
        'username': COMMON_USERNAME,
        'password': COMMON_PASSWORD,
        'selectors': {
            'username': '#memid',
            'password': '#admpwd',
            'login_button': 'button[type="submit"]'
        },
        'list_url': 'https://zain0401.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
        'product_selectors': {
            'item_container': 'div[onclick^="prtView"]',
            'product_name': '.pname',
            'price': '.sp_tbl tr:nth-child(1) td',
            'shipping': '.sp_tbl tr:nth-child(2) td'
        },
        'detail_url_pattern': 'https://zain0401.adminplus.co.kr/partner/product/prt.{type}.detail.pop.php?pcode={pcode}'
    },

    '늘푸른우리': {
        'login_url': 'https://hwanggs3.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
        'username': COMMON_USERNAME,
        'password': COMMON_PASSWORD,
        'selectors': {
            'username': '#memid',
            'password': '#admpwd',
            'login_button': 'button[type="submit"]'
        },
        'list_url': 'https://hwanggs3.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
        'product_selectors': {
            'item_container': 'div[onclick^="prtView"]',
            'product_name': '.pname',
            'price': '.sp_tbl tr:nth-child(1) td',
            'shipping': '.sp_tbl tr:nth-child(2) td'
        },
        'detail_url_pattern': 'https://hwanggs3.adminplus.co.kr/partner/product/prt.{type}.detail.pop.php?pcode={pcode}'
    },

    '팜허브': {
        'login_url': 'https://priceit.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
        'username': COMMON_USERNAME,
        'password': COMMON_PASSWORD,
        'selectors': {
            'username': '#memid',
            'password': '#admpwd',
            'login_button': 'button[type="submit"]'
        },
        'list_url': 'https://priceit.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
        'product_selectors': {
            'item_container': 'div[onclick^="prtView"]',
            'product_name': '.pname',
            'price': '.sp_tbl tr:nth-child(1) td',
            'shipping': '.sp_tbl tr:nth-child(2) td'
        },
        'detail_url_pattern': 'https://priceit.adminplus.co.kr/partner/product/prt.{type}.detail.pop.php?pcode={pcode}'
    },

    '덤덤몰': {
        'login_url': 'https://dumdummall.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
        'username': COMMON_USERNAME,
        'password': COMMON_PASSWORD,
        'selectors': {
            'username': '#memid',
            'password': '#admpwd',
            'login_button': 'button[type="submit"]'
        },
        'list_url': 'https://dumdummall.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
        'product_selectors': {
            'item_container': 'div[onclick^="prtView"]',
            'product_name': '.pname',
            'price': '.sp_tbl tr:nth-child(1) td',
            'shipping': '.sp_tbl tr:nth-child(2) td'
        },
        'detail_url_pattern': 'https://dumdummall.adminplus.co.kr/partner/product/prt.{type}.detail.pop.php?pcode={pcode}'
    },

    '마니팜': {
        'login_url': 'https://mp3462.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
        'username': COMMON_USERNAME,
        'password': COMMON_PASSWORD,
        'selectors': {
            'username': '#memid',
            'password': '#admpwd',
            'login_button': 'button[type="submit"]'
        },
        'list_url': 'https://mp3462.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
        'product_selectors': {
            'item_container': 'div[onclick^="prtView"]',
            'product_name': '.pname',
            'price': '.sp_tbl tr:nth-child(1) td',
            'shipping': '.sp_tbl tr:nth-child(2) td'
        },
        'detail_url_pattern': 'https://mp3462.adminplus.co.kr/partner/product/prt.{type}.detail.pop.php?pcode={pcode}'
    },

    '산지이음': {
        'login_url': 'https://orangec.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
        'username': COMMON_USERNAME,
        'password': COMMON_PASSWORD,
        'selectors': {
            'username': '#memid',
            'password': '#admpwd',
            'login_button': 'button[type="submit"]'
        },
        'list_url': 'https://orangec.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
        'product_selectors': {
            'item_container': 'div[onclick^="prtView"]',
            'product_name': '.pname',
            'price': '.sp_tbl tr:nth-child(1) td',
            'shipping': '.sp_tbl tr:nth-child(2) td'
        },
        'detail_url_pattern': 'https://orangec.adminplus.co.kr/partner/product/prt.{type}.detail.pop.php?pcode={pcode}'
    },

    '농부를 찾아서': {
        'login_url': 'https://ongreen.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
        'username': COMMON_USERNAME,
        'password': COMMON_PASSWORD,
        'selectors': {
            'username': '#memid',
            'password': '#admpwd',
            'login_button': 'button[type="submit"]'
        },
        'list_url': 'https://ongreen.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
        'product_selectors': {
            'item_container': 'div[onclick^="prtView"]',
            'product_name': '.pname',
            'price': '.sp_tbl tr:nth-child(1) td',
            'shipping': '.sp_tbl tr:nth-child(2) td'
        },
        'detail_url_pattern': 'https://ongreen.adminplus.co.kr/partner/product/prt.{type}.detail.pop.php?pcode={pcode}'
    },

    '캄뮤유통': {
        'login_url': 'https://ehrtnfl20002.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
        'username': COMMON_USERNAME,
        'password': COMMON_PASSWORD,
        'selectors': {
            'username': '#memid',
            'password': '#admpwd',
            'login_button': 'button[type="submit"]'
        },
        'list_url': 'https://ehrtnfl20002.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
        'product_selectors': {
            'item_container': 'div[onclick^="prtView"]',
            'product_name': '.pname',
            'price': '.sp_tbl tr:nth-child(1) td',
            'shipping': '.sp_tbl tr:nth-child(2) td'
        },
        'detail_url_pattern': 'https://ehrtnfl20002.adminplus.co.kr/partner/product/prt.{type}.detail.pop.php?pcode={pcode}'
    }
}

# ========================================
# 가격 수집 설정
# ========================================

# 관심 상품 키워드 (과일 위주)
# 키워드 파일에서 읽어오기
try:
    # 'utf-8-sig'는 한글 깨짐을 방지하는 가장 확실한 열쇠입니다.
    with open('keywords.txt', 'r', encoding='utf-8-sig') as f:
        FILTER_KEYWORDS = f.read().splitlines() # 이 줄을 안으로 한 칸 들여써야 합니다.
        print(f"✅ 키워드 {len(FILTER_KEYWORDS)}개 로드됨")
except FileNotFoundError:
    FILTER_KEYWORDS = ['감귤', '한라봉', '사과']
    print("⚠️ keywords.txt 파일을 찾을 수 없어 기본 키워드를 사용합니다.")


# 제외 키워드 (채소, 반찬류)
EXCLUDE_KEYWORDS = []

# 수집 페이지 제한 (None이면 전체)
MAX_PAGES = None

# 가격 변동 감지 설정
ENABLE_PRICE_CHANGE_ALERT = True
PRICE_HISTORY_FILE = '가격이력.xlsx'


