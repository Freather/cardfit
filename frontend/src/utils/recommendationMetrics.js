import { calculateAnnualNetBenefit, calculateMonthlyBenefit } from './calculateBenefit'

const categoryLabelMap = {
  food: '식비',
  transport: '교통',
  fuel: '주유',
  shopping: '쇼핑',
  communication: '통신비',
  entertainment: '문화/여가',
  health: '의료/건강',
  other: '기타',
}

const spendingKeyByCategory = {
  food: 'food_monthly',
  transport: 'transport_monthly',
  fuel: 'fuel_monthly',
  shopping: 'shopping_monthly',
  communication: 'communication_monthly',
  entertainment: 'entertainment_monthly',
  health: 'health_monthly',
  other: 'other_monthly',
}

export function formatWonAmount(value) {
  return `${Math.max(0, Math.round(Number(value || 0))).toLocaleString('ko-KR')}원`
}

export function buildSpendingFromBreakdown(breakdown = [], fallbackSurvey = {}) {
  const spending = buildSpendingFromSurvey(fallbackSurvey)

  breakdown.forEach((item) => {
    const key = spendingKeyByCategory[item.category]
    if (key) spending[key] = Number(item.total || 0)
  })

  return spending
}

export function buildSpendingFromSurvey(survey = {}) {
  return Object.values(spendingKeyByCategory).reduce((acc, key) => {
    acc[key] = Number(survey?.[key] || 0)
    return acc
  }, {})
}

export function buildLocalRecommendations(cards = [], spending = {}, limit = 5) {
  const rankedCards = cards
    .map((card) => {
      const monthlyBenefit = calculateMonthlyBenefit(card, spending)
      const netBenefit = calculateAnnualNetBenefit(card, spending)

      return {
        card,
        monthlyBenefit,
        netBenefit,
      }
    })
    .filter((item) => item.monthlyBenefit > 0)
    .sort((a, b) => b.netBenefit - a.netBenefit || b.monthlyBenefit - a.monthlyBenefit)

  const maxMonthlyBenefit = Math.max(...rankedCards.map((item) => item.monthlyBenefit), 1)

  return rankedCards.slice(0, limit).map((item, index) => ({
    card_id: item.card.id,
    card_name: item.card.card_name,
    rank: index + 1,
    reason: buildLocalReason(item.card, spending),
    expected_monthly_benefit: formatWonAmount(item.monthlyBenefit),
    expected_monthly_savings: item.monthlyBenefit,
    net_benefit: Math.round(item.netBenefit),
    score: calculateMatchScore(item.monthlyBenefit, maxMonthlyBenefit),
  }))
}

export function calculateRecommendationScore(recommendation, card, spending, maxMonthlyBenefit = null) {
  if (Number.isFinite(Number(recommendation.score)) && Number(recommendation.score) > 0) {
    return Math.round(Number(recommendation.score))
  }

  const monthlyBenefit =
    Number(recommendation.expected_monthly_savings || recommendation.monthly_savings || 0) ||
    calculateMonthlyBenefit(card, spending)

  const denominator = Number(maxMonthlyBenefit || monthlyBenefit || 1)
  return calculateMatchScore(monthlyBenefit, denominator)
}

export function calculateMatchScore(monthlyBenefit, maxMonthlyBenefit) {
  if (!monthlyBenefit || !maxMonthlyBenefit) return 0
  return Math.max(1, Math.min(100, Math.round((monthlyBenefit / maxMonthlyBenefit) * 100)))
}

function buildLocalReason(card, spending) {
  const matchedBenefits = (card.benefits || [])
    .map((benefit) => {
      const spendingKey = spendingKeyByCategory[benefit.benefit_category]
      const amount = Number(spending[spendingKey] || 0)
      return {
        benefit,
        amount,
      }
    })
    .filter((item) => item.amount > 0)
    .sort((a, b) => b.amount - a.amount)

  const topLabels = matchedBenefits
    .slice(0, 2)
    .map((item) => categoryLabelMap[item.benefit.benefit_category] || '생활')

  if (!topLabels.length) {
    return '소비 패턴과 카드 혜택 조건을 기준으로 예상 혜택이 높은 카드입니다.'
  }

  return `${topLabels.join('와 ')} 지출에 적용되는 혜택이 있어 현재 소비 패턴 기준 예상 절약 금액이 높습니다.`
}
