import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(_to, _from, savedPosition) {
    // Always scroll to top when navigating to a new page
    if (savedPosition) {
      // If there's a saved position (browser back/forward), use it
      return savedPosition
    } else {
      // Otherwise, scroll to top
      return { top: 0, behavior: 'smooth' }
    }
  },
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/Home.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/Register.vue')
    },
    {
      path: '/jobs',
      name: 'jobs',
      component: () => import('../views/Jobs.vue')
    },
    {
      path: '/jobs/:id',
      name: 'job-details',
      component: () => import('../views/JobDetails.vue')
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/Dashboard.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/ai-assistant',
      name: 'ai-assistant',
      component: () => import('../views/AIAssistant.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/Profile.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/post-job',
      name: 'post-job',
      component: () => import('../views/PostJob.vue'),
      meta: { requiresAuth: true, requiresRecruiter: true }
    },
    {
      path: '/saved-jobs',
      name: 'saved-jobs',
      component: () => import('../views/SavedJobs.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/interviews',
      name: 'interviews',
      component: () => import('../views/Interviews.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

// Navigation guard
router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router
