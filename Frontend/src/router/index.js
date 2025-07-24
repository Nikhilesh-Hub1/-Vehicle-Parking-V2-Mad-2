import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/user/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    //-----------------------user routes-----------------------
    {
      path: '/user/dashboard',
      name: 'user-dashboard',
      component: HomeView,
      meta: { requiresAuth: true },
    },
    {
      path: '/',
      name: 'home',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/in',
      name: 'auth',
      component: () => import('../AuthView.vue'),
    },
    //-----------------------admin routes-----------------------

    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/admin/HomeView.vue'),
      meta: { requiresAuth: true, isAdmin: true },
    },

    {
      path: '/admin/parkinglots',
      name: 'parkinglots',
      component: () => import('../views/admin/ParkingLot.vue'),
      meta: { requiresAuth: true, isAdmin: true },
    },
    {
      path: '/admin/parkinglots/add',
      name: 'add-parkinglot',
      component: () => import('../views/admin/AddLot.vue'),
      meta: { requiresAuth: true, isAdmin: true },
    },
    {
      path: '/admin/parkinglots/edit/:id',
      name: 'EditLot',
      component: () => import('../views/admin/EditLot.vue'),
    },
    {
      path: '/admin/userslist',
      name: 'UsersList',
      component: () => import('../views/admin/UsersList.vue'),
    },

    {
      path: '/admin/summary',
      name: 'summary',
      component: () => import('../views/admin/Summary.vue'),
      meta: { requiresAuth: true, adminOnly: true },
    },
     {
      path: '/user/summary',
      name: 'user-summary',
      
       component: () => import('../views/user/UserSummary.vue'),
      meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const isAuthenticated = !!token
  const user = token ? JSON.parse(localStorage.getItem('user')) : null

  //  If already logged in, redirect from auth to correct dashboard
  if (to.name === 'auth' && isAuthenticated) {
    if (user?.role === 'admin') {
      next({ name: 'admin' })
    } else {
      next({ name: 'user-dashboard' })
    }
  }
  // Block non-authenticated users from protected routes
  else if (to.meta.requiresAuth && !isAuthenticated) {
    alert('Access denied: Please log in first')
    next({ name: 'auth' })
  }
  // Block non-admin users from admin routes
  else if (to.meta.isAdmin && user?.role !== 'admin') {
    alert('Access denied: Admins only')
    next({ name: 'user-dashboard' })
  }
  // Everything okay
  else {
    next()
  }
})

// Export the router instance
export default router
