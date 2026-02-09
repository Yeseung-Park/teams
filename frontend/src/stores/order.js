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
      const orderItems = items.map(item => ({
        menu_id: item.menu_id,
        quantity: item.quantity
      }))
      const { data } = await api.post('/customer/orders', orderItems)
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
        // Flatten grouped data: [{table_id, orders: []}] -> flat order array with table_number
        this.activeOrders = data.flatMap(table => 
          table.orders.map(order => ({
            ...order,
            table_number: table.table_number
          }))
        )
      } finally {
        this.loading = false
      }
    },

    async updateOrderStatus(orderId, status) {
      try {
        const { data } = await api.patch(`/admin/orders/${orderId}/status`, { status })
        const index = this.activeOrders.findIndex(o => o.order_id === orderId)
        if (index !== -1) {
          this.activeOrders[index] = {
            ...this.activeOrders[index],
            ...data
          }
        }
        return data
      } catch (e) {
        console.error('Failed to update order status:', e)
        throw e
      }
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
