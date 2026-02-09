<template>
  <div class="menu-management">
    <header>
      <h1>메뉴 관리</h1>
      <nav>
        <router-link to="/admin">주문</router-link>
        <router-link to="/admin/menus">메뉴</router-link>
        <router-link to="/admin/tables">테이블</router-link>
      </nav>
    </header>
    
    <div class="toolbar">
      <button @click="showForm = true" class="add-btn">+ 메뉴 추가</button>
    </div>
    
    <div v-if="menuStore.loading" class="loading">로딩 중...</div>
    
    <table v-else class="menu-table">
      <thead>
        <tr>
          <th>이미지</th>
          <th>이름</th>
          <th>카테고리</th>
          <th>가격</th>
          <th>상태</th>
          <th>관리</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="menu in menuStore.menus" :key="menu.menu_id">
          <td><img v-if="menu.image_url" :src="menu.image_url" class="thumb" /></td>
          <td>{{ menu.name }}</td>
          <td>{{ menu.category }}</td>
          <td>{{ menu.price.toLocaleString() }}원</td>
          <td>{{ menu.is_available ? '판매중' : '품절' }}</td>
          <td>
            <button @click="editMenu(menu)" class="edit-btn">수정</button>
            <button @click="deleteMenu(menu.menu_id)" class="delete-btn">삭제</button>
          </td>
        </tr>
      </tbody>
    </table>
    
    <div v-if="showForm" class="modal-overlay" @click.self="closeForm">
      <div class="modal">
        <h2>{{ editingMenu ? '메뉴 수정' : '메뉴 추가' }}</h2>
        <form @submit.prevent="saveMenu">
          <input v-model="form.name" placeholder="메뉴명" required />
          <input v-model="form.category" placeholder="카테고리" required />
          <input v-model.number="form.price" type="number" placeholder="가격" required />
          <textarea v-model="form.description" placeholder="설명"></textarea>
          <label><input type="checkbox" v-model="form.is_available" /> 판매중</label>
          <div class="form-actions">
            <button type="button" @click="closeForm">취소</button>
            <button type="submit">저장</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useMenuStore } from '@/stores/menu'

const menuStore = useMenuStore()
const showForm = ref(false)
const editingMenu = ref(null)
const form = reactive({ name: '', category: '', price: 0, description: '', is_available: true })

function editMenu(menu) {
  editingMenu.value = menu
  Object.assign(form, menu)
  showForm.value = true
}

function closeForm() {
  showForm.value = false
  editingMenu.value = null
  Object.assign(form, { name: '', category: '', price: 0, description: '', is_available: true })
}

async function saveMenu() {
  try {
    if (editingMenu.value) {
      await menuStore.updateMenu(editingMenu.value.menu_id, form)
    } else {
      await menuStore.createMenu(form)
    }
    closeForm()
  } catch (e) {
    alert(e.response?.data?.detail || '저장 실패')
  }
}

async function deleteMenu(menuId) {
  if (confirm('메뉴를 삭제하시겠습니까?')) {
    await menuStore.deleteMenu(menuId)
  }
}

onMounted(() => menuStore.fetchAdminMenus())
</script>

<style scoped>
.menu-management { padding: 20px; }
header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; gap: 16px; }
h1 { margin: 0; }
nav { display: flex; gap: 16px; }
nav a { text-decoration: none; color: #666; padding: 8px 16px; border-radius: 4px; }
nav a.router-link-active { background: #1976d2; color: white; }
.toolbar { margin-bottom: 16px; }
.add-btn { background: #4CAF50; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
.loading { text-align: center; padding: 40px; }
.menu-table { width: 100%; border-collapse: collapse; }
.menu-table th, .menu-table td { padding: 12px; text-align: left; border-bottom: 1px solid #eee; }
.thumb { width: 50px; height: 50px; object-fit: cover; border-radius: 4px; }
.edit-btn { background: #1976d2; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; margin-right: 8px; }
.delete-btn { background: #f44336; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; }
.modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; }
.modal { background: white; padding: 24px; border-radius: 8px; width: 400px; max-width: 90%; }
.modal h2 { margin: 0 0 20px; }
.modal form { display: flex; flex-direction: column; gap: 12px; }
.modal input, .modal textarea { padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
.modal textarea { min-height: 80px; }
.form-actions { display: flex; gap: 12px; justify-content: flex-end; }
.form-actions button { padding: 10px 20px; border-radius: 4px; cursor: pointer; }
.form-actions button[type="button"] { background: #eee; border: none; }
.form-actions button[type="submit"] { background: #4CAF50; color: white; border: none; }
</style>
