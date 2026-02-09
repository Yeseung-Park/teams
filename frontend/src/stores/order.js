import { defineStore } from 'pinia'
import api from '@/services/api'

export const useOrderStore = defineStore('order', {
  state: () => ({
    orders: [],
    activeOrders: [],
    loading: false
  }),

  actions: {
    async createOrder(items) {
      const { data } = await api.post('/customer/orders', {
        items: items.map(item => ({
          menu_id: item.menu_id,
          quantity: item.quantity
        }))
      })
      return data
    },

    async fetchOrders() {
      this.loading = true
      try {
        const { data } = await api.get('/customer/orders')
        this.orders = data
      } finally {
        this.loading = false
      }
    },

    async fetchActiveOrders() {
      this.loading = true
      try {
        const { data } = await api.get('/admin/orders')
        this.activeOrders = data
      } finally {
        this.loading = false
      }
    },

    async updateOrderStatus(orderId, status) {
      const { data } = await api.patch(`/admin/orders/${orderId}/status`, { status })
      const index = this.activeOrders.findIndex(o => o.order_id === orderId)
      if (index !== -1) this.activeOrders[index] = data
      return data
    },

    async deleteOrder(orderId) {
      await api.delete(`/admin/orders/${orderId}`)
      this.activeOrders = this.activeOrders.filter(o => o.order_id !== orderId)
    },

    addOrder(order) {
      this.activeOrders.unshift(order)
    }
  }
})
