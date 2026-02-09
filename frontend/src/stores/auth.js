import { defineStore } from 'pinia'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null,
    isAdmin: false,
    storeId: null,
    tableId: null,
    sessionId: null
  }),

  getters: {
    isLoggedIn: (state) => !!state.token
  },

  actions: {
    init() {
      // Try to restore customer session
      const customerToken = localStorage.getItem('customer_token')
      const adminToken = localStorage.getItem('admin_token')
      
      // Use whichever is available (customer takes precedence for customer pages)
      if (window.location.pathname.startsWith('/admin') && adminToken) {
        this.token = adminToken
        this.isAdmin = true
        this.storeId = localStorage.getItem('admin_storeId')
      } else if (customerToken) {
        this.token = customerToken
        this.isAdmin = false
        this.storeId = localStorage.getItem('customer_storeId')
        this.tableId = localStorage.getItem('customer_tableId')
        this.sessionId = localStorage.getItem('customer_sessionId')
      }
    },

    async loginCustomer(storeIdentifier, tableNumber, password) {
      const { data } = await api.post('/auth/customer/login', {
        store_identifier: storeIdentifier,
        table_number: tableNumber,
        password
      })
      this.setAuth(data, false)
    },

    async loginAdmin(storeIdentifier, username, password) {
      const { data } = await api.post('/auth/admin/login', {
        store_identifier: storeIdentifier,
        username,
        password
      })
      this.setAuth(data, true)
    },

    setAuth(data, isAdmin) {
      this.token = data.access_token
      this.isAdmin = isAdmin
      this.storeId = data.store_id
      this.tableId = data.table_id
      this.sessionId = data.session_id
      
      const prefix = isAdmin ? 'admin_' : 'customer_'
      localStorage.setItem(prefix + 'token', data.access_token)
      localStorage.setItem(prefix + 'storeId', data.store_id)
      if (data.table_id) localStorage.setItem(prefix + 'tableId', data.table_id)
      if (data.session_id) localStorage.setItem(prefix + 'sessionId', data.session_id)
    },

    logout() {
      const prefix = this.isAdmin ? 'admin_' : 'customer_'
      localStorage.removeItem(prefix + 'token')
      localStorage.removeItem(prefix + 'storeId')
      localStorage.removeItem(prefix + 'tableId')
      localStorage.removeItem(prefix + 'sessionId')
      
      this.token = null
      this.isAdmin = false
      this.storeId = null
      this.tableId = null
      this.sessionId = null
    }
  }
})
