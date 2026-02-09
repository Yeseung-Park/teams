<template>
  <div class="cart-view">
    <header>
      <button @click="$router.back()" class="back-btn">←</button>
      <h1>장바구니</h1>
      <button v-if="cartStore.items.length" @click="cartStore.clear()" class="clear-btn">비우기</button>
    </header>
    
    <div v-if="!cartStore.items.length" class="empty">장바구니가 비어있습니다</div>
    
    <div v-else class="cart-items">
      <div v-for="item in cartStore.items" :key="item.menu_id" class="cart-item">
        <div class="item-info">
          <h3>{{ item.menu_name }}</h3>
          <p class="price">{{ (item.price * item.quantity).toLocaleString() }}원</p>
        </div>
        <div class="quantity-control">
          <button @click="cartStore.updateQuantity(item.menu_id, item.quantity - 1)">-</button>
          <span>{{ item.quantity }}</span>
          <button @click="cartStore.updateQuantity(item.menu_id, item.quantity + 1)">+</button>
        </div>
      </div>
    </div>
    
    <div v-if="cartStore.items.length" class="order-section">
      <div class="total">
        <span>총 금액</span>
        <span class="amount">{{ cartStore.totalAmount.toLocaleString() }}원</span>
      </div>
      <button @click="submitOrder" :disabled="loading" class="order-btn">
        {{ loading ? '주문 중...' : '주문하기' }}
      </button>
    </div>
    
    <nav class="bottom-nav">
      <router-link to="/menu">메뉴</router-link>
      <router-link to="/cart">장바구니</router-link>
      <router-link to="/orders">주문내역</router-link>
    </nav>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { useOrderStore } from '@/stores/order'

const router = useRouter()
const cartStore = useCartStore()
const orderStore = useOrderStore()
const loading = ref(false)

async function submitOrder() {
  loading.value = true
  try {
    await orderStore.createOrder(cartStore.items)
    cartStore.clear()
    router.push('/orders')
  } catch (e) {
    alert(e.response?.data?.detail || '주문 실패')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.cart-view { padding-bottom: 140px; }
header { display: flex; align-items: center; padding: 16px; gap: 16px; }
.back-btn { background: none; border: none; font-size: 24px; cursor: pointer; }
h1 { flex: 1; margin: 0; }
.clear-btn { background: none; border: none; color: #f44336; cursor: pointer; }
.empty { text-align: center; padding: 60px 20px; color: #999; }
.cart-items { padding: 0 16px; }
.cart-item { display: flex; justify-content: space-between; align-items: center; padding: 16px 0; border-bottom: 1px solid #eee; }
.item-info h3 { margin: 0 0 4px; }
.price { margin: 0; color: #4CAF50; }
.quantity-control { display: flex; align-items: center; gap: 12px; }
.quantity-control button { width: 32px; height: 32px; border: 1px solid #ddd; border-radius: 50%; background: white; cursor: pointer; }
.order-section { position: fixed; bottom: 60px; left: 0; right: 0; background: white; padding: 16px; border-top: 1px solid #eee; }
.total { display: flex; justify-content: space-between; margin-bottom: 12px; }
.amount { font-size: 20px; font-weight: bold; color: #4CAF50; }
.order-btn { width: 100%; padding: 16px; background: #4CAF50; color: white; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; }
.order-btn:disabled { background: #ccc; }
.bottom-nav { position: fixed; bottom: 0; left: 0; right: 0; display: flex; background: white; border-top: 1px solid #eee; }
.bottom-nav a { flex: 1; padding: 16px; text-align: center; text-decoration: none; color: #666; }
.bottom-nav a.router-link-active { color: #4CAF50; }
</style>
