import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/user/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    //-----------------------user routes-----------------------
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true },
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/in',
      name: 'auth',
      component: () => import('../views/AuthView.vue'),
    },
  ],
})

//-----------------------admin routes-----------------------
router.addRoute({
  path: '/admin',
  name: 'admin',
  component: () => import('../views/admin/HomeView.vue'),
  meta: { requiresAuth: true, isAdmin: true },
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token')
  const user = JSON.parse(localStorage.getItem('user'))

  if (to.name === 'auth' && isAuthenticated) {
    next({ name: 'home' })
  } else if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'auth' })
  } else if (to.meta.isAdmin && (!user || user.role !== 'admin')) {
    alert('Access denied: Admins only')
    next({ name: 'home' })
  } else {
    next()
  }
})

// Export the router instance
export default router
