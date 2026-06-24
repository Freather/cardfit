import { calculateAnnualNetBenefit, calculateMonthlyBenefit } from './calculateBenefit'

const categoryLabelMap = {
  food: '식비',
  transport: '교통',
  transportation: '교통',
  fuel: '주유',
  shopping: '쇼핑',
  communication: '통신비',
  entertainment: '문화/여가',
  leisure: '문화/여가',
  culture: '문화/여가',
  health: '의료/건강',
  medical: '의료/건강',
  hospital: '의료/건강',
  other: '기타',
  etc: '기타',
}

const spendingKeyByCategory = {
  food: 'food_monthly',
  transport: 'transport_monthly',
  transportation: 'transport_monthly',
  fuel: 'fuel_monthly',
  shopping: 'shopping_monthly',
  communication: 'communication_monthly',
  entertainment: 'entertainment_monthly',
  leisure: 'entertainment_monthly',
  culture: 'entertainment_monthly',
  health: 'health_monthly',
  medical: 'health_monthly',
  hospital: 'health_monthly',
  other: 'other_monthly',
  etc: 'other_monthly',
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

  return rankedCards.slice(0, limit).map((item, index) => ({
    card_id: item.card.id,
    card_name: item.card.card_name,
    rank: index + 1,
    reason: buildLocalReason(item.card, spending),
    expected_monthly_benefit: formatWonAmount(item.monthlyBenefit),
    expected_monthly_savings: item.monthlyBenefit,
    net_benefit: Math.round(item.netBenefit),
    score: calculateCardFitScore(item.card, spending, item.monthlyBenefit, item.netBenefit),
    score_reason: buildScoreReason(item.card, spending, item.monthlyBenefit, item.netBenefit),
  }))
}

export function calculateRecommendationScore(recommendation, card, spending) {
  if (recommendation.isScoreLocked && Number.isFinite(Number(recommendation.score))) {
    return Math.round(Number(recommendation.score))
  }

  const monthlyBenefit =
    Number(recommendation.expected_monthly_savings || recommendation.monthly_savings || 0) ||
    calculateMonthlyBenefit(card, spending)
  const netBenefit =
    Number(recommendation.net_benefit || 0) ||
    calculateAnnualNetBenefit(card, spending)

  return calculateCardFitScore(card, spending, monthlyBenefit, netBenefit)
}

export function calculateMatchScore(monthlyBenefit, maxMonthlyBenefit) {
  if (!monthlyBenefit || !maxMonthlyBenefit) return 0
  return Math.max(1, Math.min(100, Math.round((monthlyBenefit / maxMonthlyBenefit) * 100)))
}

export function calculateCardFitScore(card, spending = {}, monthlyBenefit = null, netBenefit = null) {
  const benefitAmount = Number(monthlyBenefit ?? calculateMonthlyBenefit(card, spending))
  if (!card || benefitAmount <= 0) return 0

  const spendingTotal = Object.values(spending || {}).reduce((sum, value) => sum + Number(value || 0), 0)
  if (spendingTotal <= 0) return Math.max(1, Math.min(70, Math.round(benefitAmount / 1000)))

  const matchedSpending = getMatchedBenefitSpending(card, spending)
    .reduce((sum, item) => sum + item.amount, 0)
  const annualNetBenefit = Number(netBenefit ?? calculateAnnualNetBenefit(card, spending))
  const requiredSpending = Number(card.min_prev_month_spending || 0)

  const coverageScore = Math.min(matchedSpending / spendingTotal, 1) * 25
  const benefitRateScore = Math.min(benefitAmount / spendingTotal / 0.05, 1) * 25
  const netBenefitScore = Math.min(Math.max(annualNetBenefit, 0) / 240000, 1) * 10
  const conditionScore = requiredSpending > 0
    ? Math.min(spendingTotal / requiredSpending, 1) * 5
    : 5

  return Math.max(
    1,
    Math.min(98, Math.round(35 + coverageScore + benefitRateScore + netBenefitScore + conditionScore)),
  )
}

export function buildScoreReason(card, spending = {}, monthlyBenefit = null, netBenefit = null) {
  if (!card) return '카드 상세 정보가 부족해 확인 가능한 소비 데이터와 혜택만 기준으로 계산했어요.'

  const benefitAmount = Number(monthlyBenefit ?? calculateMonthlyBenefit(card, spending))
  const annualNetBenefit = Number(netBenefit ?? calculateAnnualNetBenefit(card, spending))
  const spendingTotal = Object.values(spending || {}).reduce((sum, value) => sum + Number(value || 0), 0)
  const requiredSpending = Number(card.min_prev_month_spending || 0)
  const matchedItems = getMatchedBenefitSpending(card, spending)
  const matchedSpending = matchedItems.reduce((sum, item) => sum + item.amount, 0)
  const matchedLabels = [...new Set(matchedItems.map((item) => item.label))].slice(0, 2)
  const benefitRate = spendingTotal
    ? Math.round((benefitAmount / spendingTotal) * 1000) / 10
    : 0
  const conditionText = requiredSpending
    ? `전월실적 ${formatWonAmount(requiredSpending)} 조건`
    : '전월실적 부담 없음'

  if (!matchedItems.length) {
    return `월 ${formatWonAmount(benefitAmount)} 절약, 연 ${formatWonAmount(annualNetBenefit)} 순혜택, ${conditionText}을 반영한 점수예요.`
  }

  return `${matchedLabels.join(', ')} 지출 ${formatWonAmount(matchedSpending)}에 혜택이 적용되고, 월 ${formatWonAmount(benefitAmount)} 절약(소비의 ${benefitRate}%), 연 ${formatWonAmount(annualNetBenefit)} 순혜택, ${conditionText}을 반영한 점수예요.`
}

function getMatchedBenefitSpending(card, spending = {}) {
  const seenSpendingKeys = new Set()

  return (card.benefits || [])
    .map((benefit) => {
      const spendingKey = spendingKeyByCategory[benefit.benefit_category]
      const amount = Number(spending[spendingKey] || 0)
      return {
        benefit,
        amount,
        spendingKey,
        label: categoryLabelMap[benefit.benefit_category] || '생활',
      }
    })
    .filter((item) => {
      if (!item.amount || seenSpendingKeys.has(item.spendingKey)) return false
      seenSpendingKeys.add(item.spendingKey)
      return true
    })
    .sort((a, b) => b.amount - a.amount)
}

function buildLocalReason(card, spending) {
  const matchedBenefits = getMatchedBenefitSpending(card, spending)

  const topLabels = matchedBenefits
    .slice(0, 2)
    .map((item) => item.label)

  if (!topLabels.length) {
    return '소비 패턴과 카드 혜택 조건을 기준으로 예상 혜택이 높은 카드입니다.'
  }

  return `${topLabels.join('와 ')} 지출에 적용되는 혜택이 있어 현재 소비 패턴 기준 예상 절약 금액이 높습니다.`
}
