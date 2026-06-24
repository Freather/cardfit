function formatWon(value) {
  return `${Math.max(0, Math.round(Number(value || 0))).toLocaleString('ko-KR')}원`
}

function normalizeWonLabel(value) {
  const raw = String(value || '').trim().replace(/^월\s*/, '')
  if (!raw) return formatWon(0)
  if (raw.includes('원')) return raw

  const numeric = Number(raw.replace(/[,\s₩￦]/g, ''))
  if (Number.isFinite(numeric)) return formatWon(numeric)

  return raw
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

  return '소비 패턴과 카드 혜택 조건을 기준으로 추천한 카드입니다.'
}

function buildExpectedMonthlyBenefit(recommendation) {
  if (recommendation.expected_monthly_benefit) {
    return normalizeWonLabel(recommendation.expected_monthly_benefit)
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

function buildScore(recommendation) {
  if (Number.isFinite(Number(recommendation.score)) && Number(recommendation.score) > 0) {
    return Math.round(Number(recommendation.score))
  }

  return null
}

export function normalizeRecommendation(recommendation = {}, index = 0) {
  return {
    ...recommendation,
    rank: recommendation.rank || index + 1,
    card_id: recommendation.card_id,
    card_name: recommendation.card_name || '추천 카드',
    reason: buildReason(recommendation),
    expected_monthly_benefit: buildExpectedMonthlyBenefit(recommendation),
    score: buildScore(recommendation),
  }
}

export function normalizeRecommendations(recommendations = []) {
  return recommendations.map((recommendation, index) =>
    normalizeRecommendation(recommendation, index),
  )
}
