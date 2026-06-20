export const spendingCategories = [
  { key: 'food_monthly', category: 'food', label: '식비', color: '#2563eb', defaultValue: 300000 },
  { key: 'transport_monthly', category: 'transport', label: '교통', color: '#0f766e', defaultValue: 80000 },
  { key: 'shopping_monthly', category: 'shopping', label: '쇼핑', color: '#7c3aed', defaultValue: 200000 },
  { key: 'communication_monthly', category: 'communication', label: '통신', color: '#0891b2', defaultValue: 55000 },
  { key: 'entertainment_monthly', category: 'entertainment', label: '여가', color: '#db2777', defaultValue: 50000 },
  { key: 'other_monthly', category: 'other', label: '기타', color: '#64748b', defaultValue: 30000 },
]

export const defaultSpendingForm = {
  input_type: 'csv',
  age_group: '30s',
  income_level: 'mid',
  max_annual_fee: 30000,
}
