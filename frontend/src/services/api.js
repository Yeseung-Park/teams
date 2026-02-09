import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 10000
})

api.interceptors.request.use(config => {
  // Determine if this is an admin or customer request based on URL
  const isAdmin = config.url.includes('/admin/')
  const prefix = isAdmin ? 'admin_' : 'customer_'
  const token = localStorage.getItem(prefix + 'token')
  
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Redirect based on current path
      const isAdminPath = window.location.pathname.startsWith('/admin')
      if (isAdminPath) {
        localStorage.removeItem('admin_token')
        window.location.href = '/admin/login'
      } else {
        localStorage.removeItem('customer_token')
        window.location.href = '/'
      }
    }
    return Promise.reject(error)
  }
)

export default api
