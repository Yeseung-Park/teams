import { defineStore } from 'pinia'
import api from '@/services/api'

export const useMenuStore = defineStore('menu', {
  state: () => ({
    menus: [],
    categories: [],
    loading: false
  }),

  getters: {
    getByCategory: (state) => (category) => 
      category ? state.menus.filter(m => m.category === category) : state.menus
  },

  actions: {
    async fetchMenus() {
      this.loading = true
      try {
        const { data } = await api.get('/customer/menus')
        this.menus = data
        this.categories = [...new Set(data.map(m => m.category))]
      } finally {
        this.loading = false
      }
    },

    async fetchAdminMenus() {
      this.loading = true
      try {
        const { data } = await api.get('/admin/menus')
        this.menus = data
        this.categories = [...new Set(data.map(m => m.category))]
      } finally {
        this.loading = false
      }
    },

    async createMenu(menuData) {
      const { data } = await api.post('/admin/menus', menuData)
      this.menus.push(data)
      return data
    },

    async updateMenu(menuId, menuData) {
      const { data } = await api.put(`/admin/menus/${menuId}`, menuData)
      const index = this.menus.findIndex(m => m.menu_id === menuId)
      if (index !== -1) this.menus[index] = data
      return data
    },

    async deleteMenu(menuId) {
      await api.delete(`/admin/menus/${menuId}`)
      this.menus = this.menus.filter(m => m.menu_id !== menuId)
    }
  }
})
