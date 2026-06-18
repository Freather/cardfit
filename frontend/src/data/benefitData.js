export const benefitCategories = [
  { key: 'food', label: '식비' },
  { key: 'transport', label: '교통' },
  { key: 'shopping', label: '쇼핑' },
  { key: 'communication', label: '통신' },
  { key: 'entertainment', label: '여가' },
  { key: 'travel', label: '여행' },
  { key: 'health', label: '의료/건강' },
  { key: 'other', label: '기타' },
]

export const benefitTypes = [
  { key: 'discount', label: '할인' },
  { key: 'cashback', label: '캐시백' },
  { key: 'point', label: '포인트' },
  { key: 'mileage', label: '마일리지' },
]

export function getBenefitCategoryLabel(key) {
  return benefitCategories.find((category) => category.key === key)?.label || key
}
