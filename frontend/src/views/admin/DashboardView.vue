<template>
  <div class="dashboard">
    <header>
      <h1>주문 대시보드</h1>
      <nav>
        <router-link to="/admin">주문</router-link>
        <router-link to="/admin/menus">메뉴</router-link>
        <router-link to="/admin/tables">테이블</router-link>
        <button @click="logout" class="logout-btn">로그아웃</button>
      </nav>
    </header>
    
    <div v-if="orderStore.loading" class="loading">로딩 중...</div>
    
    <div v-else class="order-grid">
      <div v-for="order in orderStore.activeOrders" :key="order.order_id" class="order-card" :class="order.status">
        <div class="order-header">
          <span class="table">테이블 {{ order.table_number }}</span>
          <span class="order-id">#{{ order.order_id }}</span>
        </div>
        <div class="order-items">
          <div v-for="item in order.items" :key="item.order_item_id">
            {{ item.menu_name }} x {{ item.quantity }}
          </div>
        </div>
        <div class="order-actions">
          <select :value="order.status" @change="updateStatus(order.order_id, $event.target.value)">
            <option value="pending">대기</option>
            <option value="preparing">준비중</option>
            <option value="ready">완료</option>
          </select>
          <button @click="deleteOrder(order.order_id)" class="delete-btn">삭제</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useOrderStore } from '@/stores/order'
import sseService from '@/services/sse'

const router = useRouter()
const auth = useAuthStore()
const orderStore = useOrderStore()

function updateStatus(orderId, status) {
  orderStore.updateOrderStatus(orderId, status)
}

function deleteOrder(orderId) {
  if (confirm('주문을 삭제하시겠습니까?')) {
    orderStore.deleteOrder(orderId)
  }
}

function logout() {
  auth.logout()
  sseService.disconnect()
  router.push('/admin/login')
}

onMounted(() => {
  orderStore.fetchActiveOrders()
  sseService.connect(auth.storeId)
  sseService.subscribe('dashboard', (data) => {
    if (data.type === 'new_order') orderStore.addOrder(data.order)
  })
})

onUnmounted(() => {
  sseService.unsubscribe('dashboard')
})
</script>

<style scoped>
.dashboard { padding: 20px; }
header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; gap: 16px; }
h1 { margin: 0; }
nav { display: flex; gap: 16px; align-items: center; }
nav a { text-decoration: none; color: #666; padding: 8px 16px; border-radius: 4px; }
nav a.router-link-active { background: #1976d2; color: white; }
.logout-btn { background: none; border: 1px solid #f44336; color: #f44336; padding: 8px 16px; border-radius: 4px; cursor: pointer; }
.loading { text-align: center; padding: 40px; }
.order-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.order-card { background: white; border-radius: 8px; padding: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border-left: 4px solid #ccc; }
.order-card.pending { border-left-color: #f57c00; }
.order-card.preparing { border-left-color: #1976d2; }
.order-card.ready { border-left-color: #388e3c; }
.order-header { display: flex; justify-content: space-between; margin-bottom: 12px; }
.table { font-weight: bold; font-size: 18px; }
.order-id { color: #999; }
.order-items { padding: 12px 0; border-top: 1px solid #eee; border-bottom: 1px solid #eee; }
.order-actions { display: flex; gap: 8px; margin-top: 12px; }
.order-actions select { flex: 1; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
.delete-btn { background: #f44336; color: white; border: none; padding: 8px 12px; border-radius: 4px; cursor: pointer; }
</style>
