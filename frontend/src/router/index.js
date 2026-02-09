import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  // Customer
  { path: '/', name: 'customer-login', component: () => import('@/views/customer/LoginView.vue') },
  { path: '/menu', name: 'menu', component: () => import('@/views/customer/MenuView.vue'), meta: { requiresAuth: true } },
  { path: '/cart', name: 'cart', component: () => import('@/views/customer/CartView.vue'), meta: { requiresAuth: true } },
  { path: '/orders', name: 'orders', component: () => import('@/views/customer/OrdersView.vue'), meta: { requiresAuth: true } },
  
  // Admin
  { path: '/admin/login', name: 'admin-login', component: () => import('@/views/admin/LoginView.vue') },
  { path: '/admin', name: 'dashboard', component: () => import('@/views/admin/DashboardView.vue'), meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/admin/menus', name: 'menu-management', component: () => import('@/views/admin/MenuManagement.vue'), meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/admin/tables', name: 'table-management', component: () => import('@/views/admin/TableManagement.vue'), meta: { requiresAuth: true, requiresAdmin: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  auth.init() // Initialize auth state from localStorage
  
  if (to.meta.requiresAuth && !auth.token) {
    next(to.meta.requiresAdmin ? '/admin/login' : '/')
  } else if (to.meta.requiresAdmin && !auth.isAdmin) {
    next('/admin/login')
  } else {
    next()
  }
})

export default router
