# -*- coding: utf-8 -*-
"""
B2B 가격 수집 설정 파일
"""

# 공통 계정 정보
COMMON_USERNAME = 'friendship160930'
COMMON_PASSWORD = 'qkr80521!'

# AdminPlus 계열 사이트 설정
SITES = {
    '팡이농장': {
        'login_url': 'https://jaehwan0330.adminplus.co.kr/partner/?mod=member&actpage=login',
        'list_url': 'https://jaehwan0330.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
        'username': COMMON_USERNAME,
        'password': COMMON_PASSWORD,
        'selectors': {
            'username': 'input[name="id"]',
            'password': 'input[name="pw"]',
            'login_button': 'button[type="submit"]'
        },
        'product_selectors': {
            'item_container': 'tr[onclick*="detail.pop"]',
            'product_name': 'td:nth-child(3)',
            'price': 'td:nth-child(7)',
            'shipping': 'td:nth-child(8)'
        },
        'detail_url_pattern': 'https://jaehwan0330.adminplus.co.kr/partner/product/prt.{type}.detail.pop.php?pcode={pcode}'
    },
    
    '최고집': {
        'login_url': 'https://zain0401.adminplus.co.kr/partner/?mod=member&actpage=login',
        'list_url': 'https://zain0401.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
        'username': COMMON_USERNAME,
        'password': COMMON_PASSWORD,
        'selectors': {
            'username': 'input[name="id"]',
            'password': 'input[name="pw"]',
            'login_button': 'button[type="submit"]'
        },
        'product_selectors': {
            'item_container': 'tr[onclick*="detail.pop"]',
            'product_name': 'td:nth-child(3)',
            'price': 'td:nth-child(7)',
            'shipping': 'td:nth-child(8)'
        },
        'detail_url_pattern': 'https://zain0401.adminplus.co.kr/partner/product/prt.{type}.detail.pop.php?pcode={pcode}'
    },
    
    '늘푸른우리': {
        'login_url': 'https://hwanggs3.adminplus.co.kr/partner/?mod=member&actpage=login',
        'list_url': 'https://hwanggs3.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
        'username': COMMON_USERNAME,
        'password': COMMON_PASSWORD,
        'selectors': {
            'username': 'input[name="id"]',
            'password': 'input[name="pw"]',
            'login_button': 'button[type="submit"]'
        },
        'product_selectors': {
            'item_container': 'tr[onclick*="detail.pop"]',
            'product_name': 'td:nth-child(3)',
            'price': 'td:nth-child(7)',
            'shipping': 'td:nth-child(8)'
        },
        'detail_url_pattern': 'https://hwanggs3.adminplus.co.kr/partner/product/prt.{type}.detail.pop.php?pcode={pcode}'
    },
    
    '팜허브': {
        'login_url': 'https://priceit.adminplus.co.kr/partner/?mod=member&actpage=login',
        'list_url': 'https://priceit.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
        'username': COMMON_USERNAME,
        'password': COMMON_PASSWORD,
        'selectors': {
            'username': 'input[name="id"]',
            'password': 'input[name="pw"]',
            'login_button': 'button[type="submit"]'
        },
        'product_selectors': {
            'item_container': 'tr[onclick*="detail.pop"]',
            'product_name': 'td:nth-child(3)',
            'price': 'td:nth-child(7)',
            'shipping': 'td:nth-child(8)'
        },
        'detail_url_pattern': 'https://priceit.adminplus.co.kr/partner/product/prt.{type}.detail.pop.php?pcode={pcode}'
    },
    
    '덤덤몰': {
        'login_url': 'https://dumdummall.adminplus.co.kr/partner/?mod=member&actpage=login',
        'list_url': 'https://dumdummall.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
        'username': COMMON_USERNAME,
        'password': COMMON_PASSWORD,
        'selectors': {
            'username': 'input[name="id"]',
            'password': 'input[name="pw"]',
            'login_button': 'button[type="submit"]'
        },
        'product_selectors': {
            'item_container': 'tr[onclick*="detail.pop"]',
            'product_name': 'td:nth-child(3)',
            'price': 'td:nth-child(7)',
            'shipping': 'td:nth-child(8)'
        },
        'detail_url_pattern': 'https://dumdummall.adminplus.co.kr/partner/product/prt.{type}.detail.pop.php?pcode={pcode}'
    },
    
    '제주농산물(마니팜)': {
        'login_url': 'https://mp3462.adminplus.co.kr/partner/?mod=member&actpage=login',
        'list_url': 'https://mp3462.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
        'username': COMMON_USERNAME,
        'password': COMMON_PASSWORD,
        'selectors': {
            'username': 'input[name="id"]',
            'password': 'input[name="pw"]',
            'login_button': 'button[type="submit"]'
        },
        'product_selectors': {
            'item_container': 'tr[onclick*="detail.pop"]',
            'product_name': 'td:nth-child(3)',
            'price': 'td:nth-child(7)',
            'shipping': 'td:nth-child(8)'
        },
        'detail_url_pattern': 'https://mp3462.adminplus.co.kr/partner/product/prt.{type}.detail.pop.php?pcode={pcode}'
    },
    
    '산지이음': {
        'login_url': 'https://orangec.adminplus.co.kr/partner/?mod=member&actpage=login',
        'list_url': 'https://orangec.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
        'username': COMMON_USERNAME,
        'password': COMMON_PASSWORD,
        'selectors': {
            'username': 'input[name="id"]',
            'password': 'input[name="pw"]',
            'login_button': 'button[type="submit"]'
        },
        'product_selectors': {
            'item_container': 'tr[onclick*="detail.pop"]',
            'product_name': 'td:nth-child(3)',
            'price': 'td:nth-child(7)',
            'shipping': 'td:nth-child(8)'
        },
        'detail_url_pattern': 'https://orangec.adminplus.co.kr/partner/product/prt.{type}.detail.pop.php?pcode={pcode}'
    },
    
    '캄뮤유통': {
        'login_url': 'https://ehrtnfl20002.adminplus.co.kr/partner/?mod=member&actpage=login',
        'list_url': 'https://ehrtnfl20002.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
        'username': COMMON_USERNAME,
        'password': COMMON_PASSWORD,
        'selectors': {
            'username': 'input[name="id"]',
            'password': 'input[name="pw"]',
            'login_button': 'button[type="submit"]'
        },
        'product_selectors': {
            'item_container': 'tr[onclick*="detail.pop"]',
            'product_name': 'td:nth-child(3)',
            'price': 'td:nth-child(7)',
            'shipping': 'td:nth-child(8)'
        },
        'detail_url_pattern': 'https://ehrtnfl20002.adminplus.co.kr/partner/product/prt.{type}.detail.pop.php?pcode={pcode}'
    },
    
    '농부를 찾아서': {
        'login_url': 'https://ongreen.adminplus.co.kr/partner/?mod=member&actpage=login',
        'list_url': 'https://ongreen.adminplus.co.kr/partner/?mod=product&actpage=prt.list',
        'username': COMMON_USERNAME,
        'password': COMMON_PASSWORD,
        'selectors': {
            'username': 'input[name="id"]',
            'password': 'input[name="pw"]',
            'login_button': 'button[type="submit"]'
        },
        'product_selectors': {
            'item_container': 'tr[onclick*="detail.pop"]',
            'product_name': 'td:nth-child(3)',
            'price': 'td:nth-child(7)',
            'shipping': 'td:nth-child(8)'
        },
        'detail_url_pattern': 'https://ongreen.adminplus.co.kr/partner/product/prt.{type}.detail.pop.php?pcode={pcode}'
    }
}

# 가격 수집 옵션
FILTER_KEYWORDS = ['감귤', '한라봉', '천혜향', '레드향', '황금향', '진귤', '백년초', '사과', '배', '곶감', '딸기', '바나나', '오렌지']
EXCLUDE_KEYWORDS = []
MAX_PAGES = None  # None = 전체, 숫자 = 해당 페이지까지만
ENABLE_PRICE_CHANGE_ALERT = True
PRICE_HISTORY_FILE = '가격이력.xlsx'
