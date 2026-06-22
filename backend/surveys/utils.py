import csv
import io
from datetime import datetime


CATEGORY_KEYWORDS = {
    'food': [
        '음식', '음식점', '식당', '한식', '중식', '일식', '양식', '분식', '뷔페',
        '카페', '커피', '베이커리', '제과', '제빵', '치킨', '피자', '버거',
        '족발', '보쌈', '김밥', '국밥', '갈비', '삼겹살', '고기', '회', '초밥',
        '떡볶이', '도시락', '샐러드', '디저트', '아이스크림', '배달',
        '반점', '반찬', '포차', '호프', '맥주', '곱창', '닭갈비', '찜닭',
        '냉면', '국수', '라멘', '돈까스', '돈가스', '스시', '샤브',
        '스타벅스', '이디야', '메가커피', '컴포즈', '투썸', '빽다방',
        '파리바게뜨', '뚜레쥬르', '맥도날드', '롯데리아', '버거킹', '맘스터치',
        '교촌', 'bhc', 'bbq', '굽네', '도미노', '피자헛',
    ],
    'transport': [
        '버스', '지하철', '택시', '철도', '기차', '고속버스', '시외버스',
        '코레일', 'ktx', 'srt', '티머니', '캐시비', '카카오택시', '카카오 t',
        't머니', '공항철도', '공항버스', '하이패스', '통행료', '주차',
    ],
    'fuel': [
        '주유', '주유소', '충전소', 'lpg', 'sk에너지', 'sk energy', 'sk주유소',
        'gs칼텍스', 'gs caltex', 'gs주유소', 's-oil', 'soil', '에쓰오일',
        '에스오일', '현대오일뱅크', '현대오일', 'hd현대오일뱅크',
        '알뜰주유소', '농협주유소', 'ex-oil', 'ex oil', 'ev충전',
        '전기차충전', '차지비', '환경부전기차',
    ],
    'shopping': [
        '마트', '슈퍼', '편의점', '백화점', '아울렛', '쇼핑', '몰', '스토어',
        '쿠팡', '네이버페이', '카카오페이', '11번가', 'g마켓', '옥션',
        'ssg', '이마트', '홈플러스', '롯데마트', '코스트코', '트레이더스',
        '다이소', '올리브영', '무신사', '지그재그', '에이블리',
        'gs25', 'cu', '세븐일레븐', '이마트24',
    ],
    'communication': [
        '통신', '휴대폰', '인터넷', '모바일', '요금', 'kt', 'skt', 'sk텔레콤',
        'lg유플러스', '유플러스', '알뜰폰', '헬로모바일', '스카이라이프',
    ],
    'entertainment': [
        '영화', '극장', '시네마', 'cgv', '롯데시네마', '메가박스', '공연',
        '전시', '뮤지컬', '콘서트', '티켓', '놀이공원', '테마파크',
        '넷플릭스', '유튜브', '디즈니', '티빙', '웨이브', '왓챠', '멜론',
        '게임', 'pc방', '노래방', '볼링',
    ],
    'health': [
        '병원', '의원', '치과', '한의원', '약국', '의료', '검진', '안과',
        '피부과', '내과', '정형외과', '이비인후과', '산부인과', '소아과',
        '동물병원', '헬스', '피트니스', '필라테스', '요가',
    ],
}


MERCHANT_CATEGORY_MAP = {
    '스타벅스': 'food', '이디야': 'food', '메가mgc': 'food', '파리바게뜨': 'food',
    '맥도날드': 'food', '롯데리아': 'food', '우아한형제들': 'food', '배달의민족': 'food',
    'gs25': 'food', '씨유': 'food', '이마트24': 'food', '세븐일레븐': 'food',
    '홈플러스': 'shopping', '이마트': 'shopping', '롯데마트': 'shopping',
    '다이소': 'shopping', '올리브영': 'shopping', '무신사': 'shopping',
    '네이버페이': 'shopping', '카카오페이': 'shopping',
    '카카오t': 'transport', '티머니': 'transport', '한국철도': 'transport',
    '지하철': 'transport', '버스': 'transport',
    'kt': 'communication', 'skt': 'communication', 'sk텔레콤': 'communication',
    'lg유플': 'communication',
    'cgv': 'entertainment', '롯데시네마': 'entertainment', '메가박스': 'entertainment',
    '정형외과': 'health', '내과': 'health', '약국': 'health',
}

def classify_merchant(merchant_name: str) -> str:
    lower = merchant_name.lower().replace(' ', '')

    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword.lower().replace(' ', '') in lower for keyword in keywords):
            return category

    for keyword, category in MERCHANT_CATEGORY_MAP.items():
        if keyword.lower().replace(' ', '') in lower:
            return category
    return 'other'


def parse_samsung_csv(file) -> list[dict]:
    content = file.read()
    try:
        text = content.decode('utf-8-sig')
    except UnicodeDecodeError:
        text = content.decode('euc-kr')

    reader = csv.DictReader(io.StringIO(text))
    transactions = []

    for row in reader:
        try:
            amount_str = row.get('승인금액(원)', '0').replace(',', '')
            amount = int(float(amount_str))
            if amount <= 0:
                continue

            cancel = row.get('취소여부', '-').strip()
            if cancel and cancel != '-':
                continue

            date_str = row.get('승인일자', '').replace('.', '-')
            transaction_date = datetime.strptime(date_str, '%Y-%m-%d').date()

            merchant = row.get('가맹점명', '').strip()
            category = classify_merchant(merchant)

            transactions.append({
                'merchant': merchant,
                'amount': amount,
                'transaction_date': transaction_date,
                'category': category,
            })
        except (ValueError, KeyError):
            continue

    return transactions
