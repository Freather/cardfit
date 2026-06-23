import csv
import io
from datetime import datetime


# 알려진 가맹점 → 카테고리 (키워드 매칭보다 우선 적용)
MERCHANT_CATEGORY_MAP = {
    # 식비 - 커피/카페
    '스타벅스': 'food', '이디야': 'food', '메가mgc': 'food', '메가커피': 'food',
    '컴포즈': 'food', '투썸': 'food', '빽다방': 'food', '할리스': 'food',
    '폴바셋': 'food', '커피빈': 'food', '탐앤탐스': 'food',
    # 식비 - 베이커리
    '파리바게뜨': 'food', '뚜레쥬르': 'food', '성심당': 'food',
    # 식비 - 패스트푸드
    '맥도날드': 'food', '롯데리아': 'food', '버거킹': 'food', '맘스터치': 'food',
    '서브웨이': 'food', '노브랜드버거': 'food',
    # 식비 - 치킨/피자
    '교촌': 'food', 'bhc': 'food', 'bbq': 'food', '굽네': 'food',
    '도미노': 'food', '피자헛': 'food', '피자알볼로': 'food',
    # 식비 - 한식/일반 음식점
    '우아한형제들': 'food', '배달의민족': 'food', '본죽': 'food', '죽이야기': 'food',
    '오봉집': 'food', '한솥': 'food', '김밥천국': 'food', '이삭토스트': 'food',
    '편의점_식품': 'food',
    # 식비 - 일식/초밥
    '스시로': 'food', '스시': 'food',
    # 쇼핑 - 마트
    '홈플러스': 'shopping', '이마트': 'shopping', '롯데마트': 'shopping',
    '코스트코': 'shopping', '트레이더스': 'shopping',
    # 쇼핑 - 편의점 (편의점은 쇼핑으로 분류)
    'gs25': 'shopping', '씨유': 'shopping', 'cu': 'shopping',
    '세븐일레븐': 'shopping', '이마트24': 'shopping', '미니스톱': 'shopping',
    # 쇼핑 - 온라인/기타
    '쿠팡': 'shopping', '네이버페이': 'shopping', '카카오페이': 'shopping',
    '11번가': 'shopping', 'g마켓': 'shopping', '옥션': 'shopping',
    '무신사': 'shopping', '에이블리': 'shopping', '지그재그': 'shopping',
    '올리브영': 'shopping', '다이소': 'shopping', '아성다이소': 'shopping',
    # 교통
    '카카오t': 'transport', '카카오택시': 'transport', '티머니': 'transport',
    '한국철도': 'transport', '코레일': 'transport',
    # 통신
    '에스케이텔레콤': 'communication', 'sk텔레콤': 'communication',
    'skt': 'communication', 'kt': 'communication',
    'lg유플': 'communication', '엘지유플러스': 'communication',
    # 문화/여가
    'cgv': 'entertainment', '롯데시네마': 'entertainment', '메가박스': 'entertainment',
    '넷플릭스': 'entertainment', '유튜브': 'entertainment', '디즈니플러스': 'entertainment',
    '티빙': 'entertainment', '웨이브': 'entertainment', '왓챠': 'entertainment',
    '멜론': 'entertainment', '스포티파이': 'entertainment', '플로': 'entertainment',
    '네이버웹툰': 'entertainment', '카카오웹툰': 'entertainment',
    '피트니스247': 'entertainment', '헬스': 'entertainment',
    # 의료/건강
    '삼성서울병원': 'health', '서울대병원': 'health', '세브란스': 'health',
    '아산병원': 'health',
}

CATEGORY_KEYWORDS = {
    'food': [
        '음식', '식당', '한식', '중식', '일식', '양식', '분식', '뷔페',
        '카페', '커피', '베이커리', '제과', '제빵', '치킨', '피자', '버거',
        '족발', '보쌈', '김밥', '국밥', '갈비', '삼겹살', '고기', '회', '초밥',
        '떡볶이', '도시락', '샐러드', '디저트', '아이스크림', '배달',
        '반찬', '포차', '호프', '맥주', '곱창', '닭갈비', '찜닭',
        '냉면', '국수', '라멘', '돈까스', '돈가스', '샤브',
    ],
    'transport': [
        '버스', '지하철', '택시', '철도', '기차', '고속버스', '시외버스',
        'ktx', 'srt', '캐시비', '공항철도', '공항버스',
        '하이패스', '통행료', '주차',
    ],
    'fuel': [
        '주유', '주유소', '충전소', 'lpg', 'sk에너지', 'sk주유소',
        'gs칼텍스', 'gs주유소', 's-oil', 'soil', '에쓰오일',
        '에스오일', '현대오일뱅크', '현대오일', 'hd현대오일뱅크',
        '알뜰주유소', '농협주유소', 'ev충전', '전기차충전', '차지비',
    ],
    'shopping': [
        '마트', '슈퍼', '백화점', '아울렛', '쇼핑',
        'ssg', '홈쇼핑',
    ],
    'communication': [
        '통신', '이동통신', '인터넷요금', '알뜰폰', '헬로모바일', '스카이라이프',
        '에스케이텔레콤', '엘지유플러스',
    ],
    'entertainment': [
        '영화', '극장', '시네마', '공연', '뮤지컬', '콘서트',
        '놀이공원', '테마파크', '게임', 'pc방', '노래방', '볼링',
        '피트니스', '필라테스', '요가', '헬스장', '스크린',
        '웹툰', '스트리밍',
    ],
    'health': [
        '병원', '의원', '치과', '한의원', '약국', '의료', '검진',
        '안과', '피부과', '내과', '정형외과', '이비인후과', '산부인과',
        '소아과', '동물병원',
    ],
}


def classify_merchant(merchant_name: str) -> str:
    lower = merchant_name.lower().replace(' ', '')

    # 1순위: 알려진 가맹점 정확 매핑
    for keyword, category in MERCHANT_CATEGORY_MAP.items():
        if keyword.lower().replace(' ', '') in lower:
            return category

    # 2순위: 키워드 기반 분류
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword.lower().replace(' ', '') in lower for keyword in keywords):
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
