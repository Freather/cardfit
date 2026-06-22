import { createRouter, createWebHistory } from 'vue-router'

import HomePage from '../pages/HomePage.vue'
import CardSearchPage from '../pages/CardSearchPage.vue'
import CardDetailPage from '../pages/CardDetailPage.vue'
import CardComparePage from '../pages/CardComparePage.vue'
import SpendingReportPage from '../pages/SpendingReportPage.vue'
import AiRecommendationPage from '../pages/AiRecommendationPage.vue'
import ProfilePage from '../pages/ProfilePage.vue'
import LoginPage from '../pages/LoginPage.vue'
import SignupPage from '../pages/SignupPage.vue'
import { useAuthStore } from '../stores/authStore'

const routes = [
  { path: '/', name: 'home', component: HomePage },
  { path: '/cards', name: 'cards', component: CardSearchPage },
  { path: '/cards/:id', name: 'card-detail', component: CardDetailPage, props: true },
  { path: '/compare', name: 'compare', component: CardComparePage },
  { path: '/report', name: 'report', component: SpendingReportPage, meta: { requiresAuth: true } },
  { path: '/ai-recommendations', name: 'ai-recommendations', component: AiRecommendationPage, meta: { requiresAuth: true } },
  { path: '/profile', name: 'profile', component: ProfilePage, meta: { requiresAuth: true } },
  { path: '/login', name: 'login', component: LoginPage },
  { path: '/signup', name: 'signup', component: SignupPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach((to) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  return true
})

export default router

