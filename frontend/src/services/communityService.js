import api from './api'

export const communityService = {
  fetchPosts(params = {}) {
    return api.get('/api/community/posts/', { params })
  },

  fetchPopularPosts() {
    return api.get('/api/community/posts/popular/')
  },

  fetchPost(id) {
    return api.get(`/api/community/posts/${id}/`)
  },

  createPost(payload) {
    return api.post('/api/community/posts/', payload)
  },

  updatePost(id, payload) {
    return api.put(`/api/community/posts/${id}/`, payload)
  },

  deletePost(id) {
    return api.delete(`/api/community/posts/${id}/`)
  },

  incrementPostView(id) {
    return api.post(`/api/community/posts/${id}/view/`)
  },

  togglePostLike(id) {
    return api.post(`/api/community/posts/${id}/like/`)
  },

  fetchComments(postId) {
    return api.get(`/api/community/posts/${postId}/comments/`)
  },

  createComment(postId, payload) {
    return api.post(`/api/community/posts/${postId}/comments/`, payload)
  },

  updateComment(postId, commentId, payload) {
    return api.put(`/api/community/posts/${postId}/comments/${commentId}/`, payload)
  },

  deleteComment(postId, commentId) {
    return api.delete(`/api/community/posts/${postId}/comments/${commentId}/`)
  },

  toggleCommentLike(postId, commentId) {
    return api.post(`/api/community/posts/${postId}/comments/${commentId}/like/`)
  },
}
