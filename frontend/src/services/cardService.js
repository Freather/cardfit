import api from './api'

export const cardService = {
  fetchCards(params = {}) {
    return api.get('/api/cards/', { params })
  },

  fetchCardDetail(id) {
    return api.get(`/api/cards/${id}/`)
  },

  fetchCardBenefits(id, params = {}) {
    return api.get(`/api/cards/${id}/benefits/`, { params })
  },

  fetchWishlist() {
    return api.get('/api/cards/wishlist/')
  },

  addWishlist(cardId, source = 'detail') {
    return api.post('/api/cards/wishlist/', { card_id: cardId, source })
  },

  removeWishlist(cardId) {
    return api.delete(`/api/cards/wishlist/${cardId}/`)
  },
}
