<template>
  <div class="table-management">
    <header>
      <h1>테이블 관리</h1>
      <nav>
        <router-link to="/admin">주문</router-link>
        <router-link to="/admin/menus">메뉴</router-link>
        <router-link to="/admin/tables">테이블</router-link>
      </nav>
    </header>
    
    <div class="table-grid">
      <div v-for="table in tables" :key="table.table_id" class="table-card" :class="{ active: table.current_session_id }">
        <div class="table-number">{{ table.table_number }}번</div>
        <div class="table-status">{{ table.current_session_id ? '이용중' : '비어있음' }}</div>
        <div v-if="table.current_session_id" class="table-actions">
          <button @click="completeTable(table.table_id)" class="complete-btn">이용완료</button>
          <button @click="viewHistory(table.table_id)" class="history-btn">내역</button>
        </div>
      </div>
    </div>
    
    <div v-if="showHistory" class="modal-overlay" @click.self="showHistory = false">
      <div class="modal">
        <h2>테이블 {{ selectedTable }} 주문 내역</h2>
        <div v-if="historyLoading" class="loading">로딩 중...</div>
        <div v-else-if="!history.length" class="empty">내역이 없습니다</div>
        <div v-else class="history-list">
          <div v-for="order in history" :key="order.order_id" class="history-item">
            <div class="history-header">
              <span>#{{ order.order_id }}</span>
              <span>{{ order.total_amount.toLocaleString() }}원</span>
            </div>
            <div class="history-items">
              <span v-for="item in order.items" :key="item.order_item_id">
                {{ item.menu_name }} x {{ item.quantity }}
              </span>
            </div>
          </div>
        </div>
        <button @click="showHistory = false" class="close-btn">닫기</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const tables = ref([])
const showHistory = ref(false)
const selectedTable = ref(null)
const history = ref([])
const historyLoading = ref(false)

async function fetchTables() {
  try {
    const { data } = await api.get('/admin/tables')
    tables.value = data
  } catch (e) {
    console.error('Failed to fetch tables:', e)
    tables.value = []
  }
}

async function completeTable(tableId) {
  if (confirm('테이블 이용을 완료하시겠습니까?')) {
    try {
      await api.post(`/admin/tables/${tableId}/complete`)
      const table = tables.value.find(t => t.table_id === tableId)
      if (table) table.current_session_id = null
    } catch (e) {
      alert(e.response?.data?.detail || '처리 실패')
    }
  }
}

async function viewHistory(tableId) {
  selectedTable.value = tableId
  showHistory.value = true
  historyLoading.value = true
  try {
    const { data } = await api.get(`/admin/tables/${tableId}/history`)
    history.value = data
  } catch (e) {
    history.value = []
  } finally {
    historyLoading.value = false
  }
}

onMounted(fetchTables)
</script>

<style scoped>
.table-management { padding: 20px; }
header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; gap: 16px; }
h1 { margin: 0; }
nav { display: flex; gap: 16px; }
nav a { text-decoration: none; color: #666; padding: 8px 16px; border-radius: 4px; }
nav a.router-link-active { background: #1976d2; color: white; }
.table-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 16px; }
.table-card { background: #f5f5f5; border-radius: 8px; padding: 20px; text-align: center; }
.table-card.active { background: #e3f2fd; border: 2px solid #1976d2; }
.table-number { font-size: 24px; font-weight: bold; margin-bottom: 8px; }
.table-status { color: #666; margin-bottom: 12px; }
.table-actions { display: flex; gap: 8px; justify-content: center; }
.complete-btn { background: #4CAF50; color: white; border: none; padding: 8px 12px; border-radius: 4px; cursor: pointer; font-size: 12px; }
.history-btn { background: #1976d2; color: white; border: none; padding: 8px 12px; border-radius: 4px; cursor: pointer; font-size: 12px; }
.modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; }
.modal { background: white; padding: 24px; border-radius: 8px; width: 400px; max-width: 90%; max-height: 80vh; overflow-y: auto; }
.modal h2 { margin: 0 0 20px; }
.loading, .empty { text-align: center; padding: 20px; color: #999; }
.history-list { display: flex; flex-direction: column; gap: 12px; }
.history-item { background: #f9f9f9; padding: 12px; border-radius: 4px; }
.history-header { display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 8px; }
.history-items { font-size: 14px; color: #666; }
.history-items span { display: block; }
.close-btn { width: 100%; margin-top: 16px; padding: 12px; background: #eee; border: none; border-radius: 4px; cursor: pointer; }
</style>
