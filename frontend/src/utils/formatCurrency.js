export function formatCurrency(value, options = {}) {
  const amount = Number(value || 0)

  return new Intl.NumberFormat('ko-KR', {
    style: 'currency',
    currency: 'KRW',
    maximumFractionDigits: 0,
    ...options,
  }).format(amount)
}
