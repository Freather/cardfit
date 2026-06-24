const spendingKeyByCategory = {
  food: 'food_monthly',
  transport: 'transport_monthly',
  transportation: 'transport_monthly',
  fuel: 'fuel_monthly',
  shopping: 'shopping_monthly',
  entertainment: 'entertainment_monthly',
  leisure: 'entertainment_monthly',
  culture: 'entertainment_monthly',
  communication: 'communication_monthly',
  health: 'health_monthly',
  medical: 'health_monthly',
  hospital: 'health_monthly',
  other: 'other_monthly',
  etc: 'other_monthly',
}

export function calculateMonthlyBenefit(card, spending = {}) {
  return (card?.benefits || []).reduce((total, benefit) => {
    const spendingKey = spendingKeyByCategory[benefit.benefit_category]
    const monthlySpending = Number(spending[spendingKey] || 0)
    const discountRate = Number(benefit.discount_rate || 0) / 100
    const estimated = monthlySpending * discountRate
    const limited = benefit.monthly_limit ? Math.min(estimated, benefit.monthly_limit) : estimated

    return total + limited
  }, 0)
}

export function calculateAnnualNetBenefit(card, spending = {}) {
  const annualBenefit = calculateMonthlyBenefit(card, spending) * 12
  return annualBenefit - Number(card?.annual_fee || 0)
}
