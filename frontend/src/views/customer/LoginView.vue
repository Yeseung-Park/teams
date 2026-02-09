<template>
  <div class="login-container">
    <h1>테이블오더</h1>
    <form @submit.prevent="handleLogin">
      <input v-model="storeId" placeholder="매장 코드" required />
      <input v-model="tableNumber" type="number" placeholder="테이블 번호" required />
      <input v-model="password" type="password" placeholder="비밀번호" required />
      <button type="submit" :disabled="loading">{{ loading ? '로그인 중...' : '로그인' }}</button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const storeId = ref('')
const tableNumber = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''
  try {
    await auth.loginCustomer(storeId.value, parseInt(tableNumber.value), password.value)
    router.push('/menu')
  } catch (e) {
    error.value = e.response?.data?.detail || '로그인 실패'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container { max-width: 320px; margin: 100px auto; padding: 20px; }
h1 { text-align: center; margin-bottom: 30px; }
form { display: flex; flex-direction: column; gap: 12px; }
input { padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px; }
button { padding: 14px; background: #4CAF50; color: white; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; }
button:disabled { background: #ccc; }
.error { color: #f44336; text-align: center; margin: 0; }
</style>
