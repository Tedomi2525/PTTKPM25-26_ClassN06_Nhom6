<script setup>
import { onMounted } from 'vue'

definePageMeta({
  layout: "default"
});

const { isAuthenticated, validateToken } = useAuth()

onMounted(async () => {
  // Kiểm tra authentication
  if (typeof localStorage !== 'undefined') {
    const token = localStorage.getItem('token')
    if (!token) {
      await navigateTo('/')
      return
    }
    
    // Kiểm tra token hợp lệ
    const isValid = await validateToken()
    if (!isValid) {
      await navigateTo('/')
      return
    }
  }
})
</script>

<template>
  <div class="max-w-4xl mx-auto mt-6">
    <div class="bg-white shadow rounded-lg p-6">
      <h4 class="text-xl font-semibold mb-2">Chào mừng đến với hệ thống quản lý 🎓</h4>
      <p class="text-gray-600">Hãy chọn chức năng từ thanh menu ở trên.</p>
    </div>
  </div>
</template>
