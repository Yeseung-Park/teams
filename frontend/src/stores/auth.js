import { defineStore } from 'pinia'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token'),
    isAdmin: localStorage.getItem('isAdmin') === 'true',
    storeId: localStorage.getItem('storeId'),
    tableId: localStorage.getItem('tableId'),
    sessionId: localStorage.getItem('sessionId')
  }),

  getters: {
    isLoggedIn: (state) => !!state.token
  },

  actions: {
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
      
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('isAdmin', isAdmin)
      localStorage.setItem('storeId', data.store_id)
      if (data.table_id) localStorage.setItem('tableId', data.table_id)
      if (data.session_id) localStorage.setItem('sessionId', data.session_id)
    },

    logout() {
      this.token = null
      this.isAdmin = false
      localStorage.clear()
    }
  }
})
