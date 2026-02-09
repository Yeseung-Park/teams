import { defineStore } from 'pinia'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: []
  }),

  getters: {
    totalAmount: (state) => state.items.reduce((sum, item) => sum + item.price * item.quantity, 0),
    itemCount: (state) => state.items.reduce((sum, item) => sum + item.quantity, 0)
  },

  actions: {
    addItem(menu) {
      const existing = this.items.find(item => item.menu_id === menu.menu_id)
      if (existing) {
        existing.quantity++
      } else {
        this.items.push({ ...menu, quantity: 1 })
      }
    },

    updateQuantity(menuId, quantity) {
      const item = this.items.find(item => item.menu_id === menuId)
      if (item) {
        item.quantity = Math.max(0, quantity)
        if (item.quantity === 0) this.removeItem(menuId)
      }
    },

    removeItem(menuId) {
      this.items = this.items.filter(item => item.menu_id !== menuId)
    },

    clear() {
      this.items = []
    }
  }
})
