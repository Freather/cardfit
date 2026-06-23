import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

import { cardData } from '../data/cardData'
import { cardService } from '../services/cardService'

const categoryMap = {
  transportation: 'transport',
  leisure: 'entertainment',
  culture: 'entertainment',
  medical: 'health',
  hospital: 'health',
  etc: 'other',
}

const benefitTypeMap = {
  accumulate: 'point',
}

function normalizeBenefit(benefit = {}) {
  return {
    ...benefit,
    benefit_category: categoryMap[benefit.benefit_category] || benefit.benefit_category,
    benefit_type: benefitTypeMap[benefit.benefit_type] || benefit.benefit_type,
  }
}

function normalizeCard(card = {}) {
  return {
    ...card,
    benefits: Array.isArray(card.benefits) ? card.benefits.map(normalizeBenefit) : [],
  }
}

function normalizeWish(wish = {}) {
  return {
    ...wish,
    card: wish.card ? normalizeCard(wish.card) : wish.card,
  }
}

export const useCardStore = defineStore('cards', () => {
  const cards = ref([...cardData])
  const selectedCard = ref(null)
  const wishlist = ref([])
  const isLoading = ref(false)
  const error = ref(null)
  const filters = ref({
    keyword: '',
    benefitCategory: '',
    maxAnnualFee: '',
    cardType: '',
    sort: 'netBenefit',
  })
  const pagination = ref({
    page: 1,
    pageSize: 8,
    total: cardData.length,
  })

  const filteredCards = computed(() => {
    return cards.value.filter((card) => {
      const keyword = filters.value.keyword.trim().toLowerCase()
      const matchesKeyword =
        !keyword ||
        card.card_name.toLowerCase().includes(keyword) ||
        card.card_company.toLowerCase().includes(keyword)
      const matchesType = !filters.value.cardType || card.card_type === filters.value.cardType
      const matchesFee =
        !filters.value.maxAnnualFee ||
        Number(card.annual_fee) <= Number(filters.value.maxAnnualFee)
      const matchesBenefit =
        !filters.value.benefitCategory ||
        card.benefits?.some(
          (benefit) => benefit.benefit_category === filters.value.benefitCategory,
        )

      return matchesKeyword && matchesType && matchesFee && matchesBenefit
    })
  })

  async function fetchCards(params = {}) {
    isLoading.value = true
    error.value = null

    try {
      const { data } = await cardService.fetchCards(params)
      cards.value = (data.results || data).map(normalizeCard)
      pagination.value.total = data.count || cards.value.length
      return cards.value
    } catch (err) {
      error.value = err
      return cards.value
    } finally {
      isLoading.value = false
    }
  }

  async function fetchCardDetail(id) {
    isLoading.value = true
    error.value = null

    try {
      const { data } = await cardService.fetchCardDetail(id)
      selectedCard.value = normalizeCard(data)
      return selectedCard.value
    } catch (err) {
      error.value = err
      selectedCard.value = cardData.find((card) => String(card.id) === String(id)) || null
      return selectedCard.value
    } finally {
      isLoading.value = false
    }
  }

  async function fetchWishlist() {
    const { data } = await cardService.fetchWishlist()
    wishlist.value = (data.results || data).map(normalizeWish)
    return wishlist.value
  }

  async function addWishlist(cardId, source = 'detail') {
    const { data } = await cardService.addWishlist(cardId, source)
    const normalizedWish = normalizeWish(data)
    if (!wishlist.value.some((wish) => wish.card?.id === normalizedWish.card?.id)) {
      wishlist.value = [normalizedWish, ...wishlist.value]
    }
    if (selectedCard.value?.id === normalizedWish.card?.id) {
      selectedCard.value = { ...selectedCard.value, is_wished: true }
    }
    cards.value = cards.value.map((card) =>
      card.id === normalizedWish.card?.id ? { ...card, is_wished: true } : card,
    )
    return normalizedWish
  }

  async function removeWishlist(cardId) {
    await cardService.removeWishlist(cardId)
    wishlist.value = wishlist.value.filter((wish) => String(wish.card?.id) !== String(cardId))
    if (selectedCard.value?.id && String(selectedCard.value.id) === String(cardId)) {
      selectedCard.value = { ...selectedCard.value, is_wished: false }
    }
    cards.value = cards.value.map((card) =>
      String(card.id) === String(cardId) ? { ...card, is_wished: false } : card,
    )
  }

  function setFilters(nextFilters) {
    filters.value = { ...filters.value, ...nextFilters }
    pagination.value.page = 1
  }

  function resetFilters() {
    filters.value = {
      keyword: '',
      benefitCategory: '',
      maxAnnualFee: '',
      cardType: '',
      sort: 'netBenefit',
    }
    pagination.value.page = 1
  }

  return {
    cards,
    selectedCard,
    wishlist,
    isLoading,
    error,
    filters,
    pagination,
    filteredCards,
    fetchCards,
    fetchCardDetail,
    fetchWishlist,
    addWishlist,
    removeWishlist,
    setFilters,
    resetFilters,
  }
})
