function formatWon(value) {
  return new Intl.NumberFormat('ko-KR', {
    style: 'currency',
    currency: 'KRW',
    maximumFractionDigits: 0,
  }).format(Math.max(0, Math.round(Number(value || 0))))
}

function buildReason(recommendation) {
  if (recommendation.reason) return recommendation.reason

  const details = recommendation.benefit_details || []
  const topBenefit = details[0]
  if (topBenefit) {
    const category = topBenefit.category || '주요 소비'
    const rate = Number(topBenefit.discount_rate || 0)
    const monthlySavings = formatWon(topBenefit.monthly_savings || 0)
    return `${category} 영역에서 ${rate}% 혜택을 받을 수 있어 월 ${monthlySavings} 수준의 절감이 기대됩니다.`
  }

  if (recommendation.net_benefit !== undefined) {
    return `연회비를 반영한 예상 순혜택은 연 ${formatWon(recommendation.net_benefit)}입니다.`
  }

  return '소비 패턴과 카드 혜택 조건을 기준으로 추천된 카드입니다.'
}

function buildExpectedMonthlyBenefit(recommendation) {
  if (recommendation.expected_monthly_benefit) {
    return recommendation.expected_monthly_benefit
  }

  const monthly =
    recommendation.expected_monthly_savings ??
    recommendation.monthly_savings ??
    (recommendation.net_benefit !== undefined ? Number(recommendation.net_benefit) / 12 : null) ??
    (recommendation.total_annual_savings !== undefined
      ? Number(recommendation.total_annual_savings) / 12
      : 0)

  return formatWon(monthly)
}

function buildScore(recommendation, index) {
  if (recommendation.score) return recommendation.score

  const netBenefit = Number(recommendation.net_benefit || 0)
  if (netBenefit > 0) return Math.min(99, Math.max(80, Math.round(netBenefit / 10000) + 80))

  return index === 0 ? 98 : index === 1 ? 92 : 85
}

export function normalizeRecommendation(recommendation = {}, index = 0) {
  return {
    ...recommendation,
    rank: recommendation.rank || index + 1,
    card_id: recommendation.card_id,
    card_name: recommendation.card_name || '추천 카드',
    reason: buildReason(recommendation),
    expected_monthly_benefit: buildExpectedMonthlyBenefit(recommendation),
    score: buildScore(recommendation, index),
  }
}

export function normalizeRecommendations(recommendations = []) {
  return recommendations.map((recommendation, index) =>
    normalizeRecommendation(recommendation, index),
  )
}
