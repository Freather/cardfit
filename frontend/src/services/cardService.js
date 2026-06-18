import api from './api'
import { cardData } from '../data/cardData'

export const cardService = {
  async fetchCards(params = {}) {
    try {
      return await api.get('/api/cards/', { params })
    } catch (error) {
      return { data: { count: cardData.length, results: cardData }, error }
    }
  },

  async fetchCardDetail(id) {
    try {
      return await api.get(`/api/cards/${id}/`)
    } catch (error) {
      const card = cardData.find((item) => String(item.id) === String(id))
      return { data: card || null, error }
    }
  },

  fetchCardBenefits(id, params = {}) {
    return api.get(`/api/cards/${id}/benefits/`, { params })
  },
}
