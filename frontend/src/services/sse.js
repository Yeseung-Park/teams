class SSEService {
  constructor() {
    this.eventSource = null
    this.listeners = new Map()
  }

  connect(storeId) {
    const token = localStorage.getItem('token')
    this.eventSource = new EventSource(`/api/v1/admin/orders/stream?token=${token}`)
    
    this.eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data)
      this.listeners.forEach(callback => callback(data))
    }
    
    this.eventSource.onerror = () => {
      this.disconnect()
      setTimeout(() => this.connect(storeId), 5000)
    }
  }

  disconnect() {
    if (this.eventSource) {
      this.eventSource.close()
      this.eventSource = null
    }
  }

  subscribe(id, callback) {
    this.listeners.set(id, callback)
  }

  unsubscribe(id) {
    this.listeners.delete(id)
  }
}

export default new SSEService()
