import csv
import io
from datetime import datetime


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
    lower = merchant_name.lower()
    for keyword, category in MERCHANT_CATEGORY_MAP.items():
        if keyword.lower() in lower:
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
