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
          <td><img v-if="menu.image_url" :src="`http://localhost:8000${menu.image_url}`" class="thumb" /></td>
          <td>{{ menu.menu_name }}</td>
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
          <input v-model="form.menu_name" placeholder="메뉴명" required />
          <select v-model.number="form.category_id" required>
            <option value="">카테고리 선택</option>
            <option value="1">메인 요리</option>
            <option value="2">사이드 메뉴</option>
            <option value="3">음료</option>
          </select>
          <input v-model.number="form.price" type="number" placeholder="가격" required />
          <textarea v-model="form.description" placeholder="설명"></textarea>
          
          <div class="image-upload">
            <label for="image-file">이미지 선택</label>
            <input id="image-file" type="file" accept="image/*" @change="handleImageSelect" />
            <div v-if="imagePreview" class="preview">
              <img :src="imagePreview" alt="미리보기" />
            </div>
          </div>
          
          <label><input type="checkbox" v-model="form.is_available" /> 판매중</label>
          <div class="form-actions">
            <button type="button" @click="closeForm">취소</button>
            <button type="submit" :disabled="uploading">{{ uploading ? '저장 중...' : '저장' }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useMenuStore } from '@/stores/menu'
import axios from 'axios'

const menuStore = useMenuStore()
const showForm = ref(false)
const editingMenu = ref(null)
const uploading = ref(false)
const selectedImage = ref(null)
const imagePreview = ref(null)
const form = reactive({ 
  menu_name: '', 
  category_id: '', 
  price: 0, 
  description: '', 
  is_available: true,
  image_url: ''
})

function handleImageSelect(event) {
  const file = event.target.files[0]
  if (file) {
    selectedImage.value = file
    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

function editMenu(menu) {
  editingMenu.value = menu
  Object.assign(form, menu)
  if (menu.image_url) {
    imagePreview.value = `http://localhost:8000${menu.image_url}`
  }
  showForm.value = true
}

function closeForm() {
  showForm.value = false
  editingMenu.value = null
  selectedImage.value = null
  imagePreview.value = null
  Object.assign(form, { 
    menu_name: '', 
    category_id: '', 
    price: 0, 
    description: '', 
    is_available: true,
    image_url: ''
  })
}

async function uploadImage() {
  if (!selectedImage.value) return null
  
  const formData = new FormData()
  formData.append('file', selectedImage.value)
  
  const token = localStorage.getItem('token')
  const response = await axios.post('http://localhost:8000/api/v1/admin/upload/image', formData, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'multipart/form-data'
    }
  })
  
  return response.data.image_url
}

async function saveMenu() {
  try {
    uploading.value = true
    
    // Upload image if selected
    if (selectedImage.value) {
      const imageUrl = await uploadImage()
      form.image_url = imageUrl
    }
    
    if (editingMenu.value) {
      await menuStore.updateMenu(editingMenu.value.menu_id, form)
    } else {
      await menuStore.createMenu(form)
    }
    closeForm()
    await menuStore.fetchAdminMenus()
  } catch (e) {
    alert(e.response?.data?.detail || '저장 실패')
  } finally {
    uploading.value = false
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
.modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal { background: white; padding: 24px; border-radius: 8px; width: 500px; max-width: 90%; max-height: 90vh; overflow-y: auto; }
.modal h2 { margin: 0 0 20px; }
.modal form { display: flex; flex-direction: column; gap: 12px; }
.modal input[type="text"], .modal input[type="number"], .modal select, .modal textarea { padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
.modal textarea { min-height: 80px; }
.image-upload { border: 2px dashed #ddd; padding: 16px; border-radius: 4px; text-align: center; }
.image-upload label { display: block; margin-bottom: 8px; font-weight: bold; cursor: pointer; color: #1976d2; }
.image-upload input[type="file"] { display: block; margin: 0 auto; }
.preview { margin-top: 12px; }
.preview img { max-width: 100%; max-height: 200px; border-radius: 4px; }
.form-actions { display: flex; gap: 12px; justify-content: flex-end; margin-top: 8px; }
.form-actions button { padding: 10px 20px; border-radius: 4px; cursor: pointer; }
.form-actions button[type="button"] { background: #eee; border: none; }
.form-actions button[type="submit"] { background: #4CAF50; color: white; border: none; }
.form-actions button:disabled { background: #ccc; cursor: not-allowed; }
</style>
