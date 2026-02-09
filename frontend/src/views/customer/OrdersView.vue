<template>
  <div class="orders-view">
    <header>
      <h1>주문내역</h1>
    </header>
    
    <div v-if="orderStore.loading" class="loading">로딩 중...</div>
    <div v-else-if="!orderStore.orders.length" class="empty">주문 내역이 없습니다</div>
    
    <div v-else class="order-list">
      <div v-for="order in orderStore.orders" :key="order.order_id" class="order-card">
        <div class="order-header">
          <span class="order-id">#{{ order.order_id }}</span>
          <span :class="['status', order.status]">{{ statusText(order.status) }}</span>
        </div>
        <div class="order-items">
          <div v-for="item in order.items" :key="item.order_item_id" class="order-item">
            <span>{{ item.menu_name }} x {{ item.quantity }}</span>
            <span>{{ (item.unit_price * item.quantity).toLocaleString() }}원</span>
          </div>
        </div>
        <div class="order-total">
          <span>합계</span>
          <span>{{ order.total_amount.toLocaleString() }}원</span>
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
import { onMounted } from 'vue'
import { useOrderStore } from '@/stores/order'

const orderStore = useOrderStore()

const statusText = (status) => ({
  pending: '대기중',
  preparing: '준비중',
  ready: '완료',
  cancelled: '취소됨'
}[status] || status)

onMounted(() => orderStore.fetchOrders())
</script>

<style scoped>
.orders-view { padding-bottom: 70px; }
header { padding: 16px; }
h1 { margin: 0; }
.loading, .empty { text-align: center; padding: 60px 20px; color: #999; }
.order-list { padding: 0 16px; }
.order-card { background: #f9f9f9; border-radius: 12px; padding: 16px; margin-bottom: 16px; }
.order-header { display: flex; justify-content: space-between; margin-bottom: 12px; }
.order-id { font-weight: bold; }
.status { padding: 4px 8px; border-radius: 4px; font-size: 12px; }
.status.pending { background: #fff3e0; color: #f57c00; }
.status.preparing { background: #e3f2fd; color: #1976d2; }
.status.ready { background: #e8f5e9; color: #388e3c; }
.status.cancelled { background: #ffebee; color: #d32f2f; }
.order-items { border-top: 1px solid #eee; padding-top: 12px; }
.order-item { display: flex; justify-content: space-between; padding: 4px 0; font-size: 14px; }
.order-total { display: flex; justify-content: space-between; border-top: 1px solid #eee; padding-top: 12px; margin-top: 12px; font-weight: bold; }
.bottom-nav { position: fixed; bottom: 0; left: 0; right: 0; display: flex; background: white; border-top: 1px solid #eee; }
.bottom-nav a { flex: 1; padding: 16px; text-align: center; text-decoration: none; color: #666; }
.bottom-nav a.router-link-active { color: #4CAF50; }
</style>
