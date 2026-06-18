import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

const MAX_COMPARE_COUNT = 3

export const useCompareStore = defineStore('compare', () => {
  const compareCards = ref([])

  const isFull = computed(() => compareCards.value.length >= MAX_COMPARE_COUNT)

  function addCard(card) {
    if (!card) return false
    if (compareCards.value.some((item) => item.id === card.id)) return true
    if (isFull.value) return false

    compareCards.value.push(card)
    return true
  }

  function removeCard(cardId) {
    compareCards.value = compareCards.value.filter((card) => String(card.id) !== String(cardId))
  }

  function clearCards() {
    compareCards.value = []
  }

  return {
    compareCards,
    isFull,
    addCard,
    removeCard,
    clearCards,
  }
})
