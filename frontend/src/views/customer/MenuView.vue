<template>
  <div class="menu-view">
    <header>
      <h1>메뉴</h1>
      <router-link to="/cart" class="cart-btn">🛒 {{ cartStore.itemCount }}</router-link>
    </header>
    
    <div class="categories">
      <button :class="{ active: !selectedCategory }" @click="selectedCategory = ''">전체</button>
      <button v-for="cat in menuStore.categories" :key="cat" :class="{ active: selectedCategory === cat }" @click="selectedCategory = cat">{{ cat }}</button>
    </div>
    
    <div v-if="menuStore.loading" class="loading">로딩 중...</div>
    <div v-else class="menu-grid">
      <div v-for="menu in filteredMenus" :key="menu.menu_id" class="menu-card" @click="addToCart(menu)">
        <img v-if="menu.image_url" :src="menu.image_url" :alt="menu.menu_name" />
        <div class="menu-info">
          <h3>{{ menu.menu_name }}</h3>
          <p class="price">{{ menu.price.toLocaleString() }}원</p>
        </div>
      </div>
    </div>
    
    <nav class="bottom-nav">
      <router-link to="/menu">메뉴</router-link>
      <router-link to="/cart">장바구니</router-link>
      <router-link to="/orders">주문내역</router-link>
    </nav>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useMenuStore } from '@/stores/menu'
import { useCartStore } from '@/stores/cart'

const menuStore = useMenuStore()
const cartStore = useCartStore()
const selectedCategory = ref('')

const filteredMenus = computed(() => menuStore.getByCategory(selectedCategory.value))

function addToCart(menu) {
  cartStore.addItem(menu)
}

onMounted(() => menuStore.fetchMenus())
</script>

<style scoped>
.menu-view { padding-bottom: 70px; }
header { display: flex; justify-content: space-between; align-items: center; padding: 16px; position: sticky; top: 0; background: white; }
h1 { margin: 0; }
.cart-btn { background: #4CAF50; color: white; padding: 8px 16px; border-radius: 20px; text-decoration: none; }
.categories { display: flex; gap: 8px; padding: 0 16px; overflow-x: auto; }
.categories button { padding: 8px 16px; border: 1px solid #ddd; border-radius: 20px; background: white; white-space: nowrap; }
.categories button.active { background: #4CAF50; color: white; border-color: #4CAF50; }
.loading { text-align: center; padding: 40px; }
.menu-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; padding: 16px; }
.menu-card { border: 1px solid #eee; border-radius: 12px; overflow: hidden; cursor: pointer; }
.menu-card img { width: 100%; height: 120px; object-fit: cover; }
.menu-info { padding: 12px; }
.menu-info h3 { margin: 0 0 8px; font-size: 14px; }
.price { margin: 0; color: #4CAF50; font-weight: bold; }
.bottom-nav { position: fixed; bottom: 0; left: 0; right: 0; display: flex; background: white; border-top: 1px solid #eee; }
.bottom-nav a { flex: 1; padding: 16px; text-align: center; text-decoration: none; color: #666; }
.bottom-nav a.router-link-active { color: #4CAF50; }
</style>
