export function getRepresentativeBenefit(card) {
  return [...(card?.benefits || [])]
    .filter((benefit) => Number(benefit.discount_rate || 0) > 0)
    .sort((a, b) => {
      const rateDiff = Number(b.discount_rate || 0) - Number(a.discount_rate || 0)
      if (rateDiff) return rateDiff
      return Number(b.monthly_limit || 0) - Number(a.monthly_limit || 0)
    })[0]
}
