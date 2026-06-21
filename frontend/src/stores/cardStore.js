import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

import { cardData } from '../data/cardData'
import { cardService } from '../services/cardService'

export const useCardStore = defineStore('cards', () => {
  const cards = ref([...cardData])
  const selectedCard = ref(null)
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
      cards.value = data.results || data
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
      selectedCard.value = data
      return data
    } catch (err) {
      error.value = err
      selectedCard.value = cardData.find((card) => String(card.id) === String(id)) || null
      return selectedCard.value
    } finally {
      isLoading.value = false
    }
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
    isLoading,
    error,
    filters,
    pagination,
    filteredCards,
    fetchCards,
    fetchCardDetail,
    setFilters,
    resetFilters,
  }
})
