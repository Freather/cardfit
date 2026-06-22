export const mockSurvey = {
  id: 'mock-survey-202406',
  input_type: 'csv',
  age_group: '30s',
  income_level: 'mid',
  max_annual_fee: 30000,
  food_monthly: 320000,
  transport_monthly: 86000,
  shopping_monthly: 240000,
  communication_monthly: 62000,
  entertainment_monthly: 118000,
  other_monthly: 74000,
  total_monthly: 900000,
  created_at: '2024-06-22T09:00:00+09:00',
}

export const mockCategoryBreakdown = [
  {
    category: 'food',
    label: '식비',
    total: 320000,
    ratio: 35.6,
    insight: '배달, 카페, 외식 결제가 가장 큰 비중을 차지합니다.',
  },
  {
    category: 'shopping',
    label: '쇼핑',
    total: 240000,
    ratio: 26.7,
    insight: '온라인 쇼핑과 생활용품 구매가 반복적으로 발생합니다.',
  },
  {
    category: 'entertainment',
    label: '문화/여가',
    total: 118000,
    ratio: 13.1,
    insight: 'OTT, 영화, 간편결제 기반 여가 지출이 꾸준합니다.',
  },
  {
    category: 'transport',
    label: '교통',
    total: 86000,
    ratio: 9.6,
    insight: '대중교통과 택시 이용이 함께 나타납니다.',
  },
  {
    category: 'other',
    label: '기타',
    total: 74000,
    ratio: 8.2,
    insight: '생활 잡비성 결제가 소액으로 분산되어 있습니다.',
  },
  {
    category: 'communication',
    label: '통신',
    total: 62000,
    ratio: 6.8,
    insight: '월 고정 통신비가 안정적으로 발생합니다.',
  },
]

export const mockAiRecommendations = [
  {
    rank: 1,
    card_id: 1,
    card_name: '삼성 iD ON 카드',
    reason: '식비와 온라인 쇼핑 비중이 높아 생활 밀착형 할인 혜택을 가장 크게 받을 수 있습니다.',
    expected_monthly_benefit: '월 18,400원',
    tip: '배달앱, 카페, 온라인몰 결제를 이 카드로 모으면 혜택 효율이 높습니다.',
  },
  {
    rank: 2,
    card_id: 5,
    card_name: '삼성 taptap O',
    reason: '쇼핑, 대중교통, 통신비처럼 반복되는 결제 영역이 고르게 분포되어 있습니다.',
    expected_monthly_benefit: '월 14,900원',
    tip: '통신비 자동이체와 교통 결제를 함께 묶는 조합이 좋습니다.',
  },
  {
    rank: 3,
    card_id: 10,
    card_name: '삼성카드 & MILEAGE PLATINUM',
    reason: '월 지출 규모가 충분하고 여가 지출이 있어 포인트/마일리지 적립형 카드도 후보가 됩니다.',
    expected_monthly_benefit: '월 11,700원',
    tip: '고정비보다 큰 금액 결제에 집중해서 적립 효율을 높이세요.',
  },
]

export const mockAiReport = {
  survey: mockSurvey,
  based_on: {
    food_monthly: mockSurvey.food_monthly,
    transport_monthly: mockSurvey.transport_monthly,
    shopping_monthly: mockSurvey.shopping_monthly,
    entertainment_monthly: mockSurvey.entertainment_monthly,
    communication_monthly: mockSurvey.communication_monthly,
    other_monthly: mockSurvey.other_monthly,
    total_monthly: mockSurvey.total_monthly,
    max_annual_fee: mockSurvey.max_annual_fee,
  },
  recommendations: mockAiRecommendations,
  category_breakdown: mockCategoryBreakdown,
  summary:
    '최근 소비는 식비와 쇼핑에 집중되어 있어 생활 할인형 카드가 가장 유리합니다. 고정비는 통신과 교통 중심으로 묶고, 여가 지출은 서브 혜택으로 가져가는 조합을 추천합니다.',
  expected_total_monthly_benefit: '월 18,400원',
}
