# ========================================
# 1. 공통 로그인 정보
# ========================================
COMMON_USERNAME = 'friendship160930'
COMMON_PASSWORD = 'kmgss11ss!@'

# ========================================
# 2. B2B 사이트 설정 (SITES 딕셔너리)
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
} # 여기서 괄호가 꼭 닫혀야 합니다!

# ========================================
# 3. 가격 수집 설정
# ========================================
try:
    with open('keywords.txt', 'r', encoding='utf-8-sig') as f:
        FILTER_KEYWORDS = f.read().splitlines()
except Exception:
    FILTER_KEYWORDS = ['감귤', '한라봉', '사과']

# 대시보드가 필요로 하는 필수 변수들
EXCLUDE_KEYWORDS = []
MAX_PAGES = None
ENABLE_PRICE_CHANGE_ALERT = True
PRICE_HISTORY_FILE = '가격이력.xlsx'
