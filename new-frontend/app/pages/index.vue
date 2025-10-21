<template>
  <main class="min-h-screen flex">
    <!-- Left Section -->
    <section class="hidden md:flex flex-col justify-center items-center w-1/2 bg-[#09f] p-10">
      <header class="text-right space-y-2">
        <h1 class="text-4xl font-bold text-white pt-20">
          Phân tích thiết kế phần mềm
        </h1>
        <h2 class="text-4xl py-[10px] font-bold text-white">
          Nhóm 6
        </h2>
        <h3 class="text-4xl font-bold text-white">
          Quản lý đào tạo ứng dụng hệ thống điểm danh khuôn mặt
        </h3>
      </header>
      <img
        src="https://c.animaapp.com/mewurn4ndN2M6v/img/students-pana-fba09de9-1.svg"
        alt="Students illustration"
        class="max-w-xl mb-6 py-[10px]"
      />
    </section>

    <!-- Right Section -->
    <section class="flex flex-col justify-center items-center w-full md:w-1/2 p-8 bg-[#f0f0f0]">
      <div class="w-full max-w-md bg-white shadow-lg rounded-2xl p-8 space-y-6">
        <!-- Logo -->
        <div class="flex justify-center">
          <img src="/images/Sec_Edunera_Logo_512.png" alt="Edunera Logo" class="h-16" />
        </div>

        <!-- Error message -->
        <p v-if="loginError" class="text-red-500 h-5 text-center">{{ loginError }}</p>
        
        <!-- Loading indicator -->
        <div v-if="isChecking" class="text-center text-blue-600 h-5">
          <span class="inline-flex items-center">
            <svg class="animate-spin -ml-1 mr-3 h-4 w-4 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Đang đăng nhập...
          </span>
        </div>

        <!-- Login Form -->
        <form class="space-y-4" @submit.prevent="handleLogin" :disabled="isChecking">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700">
              Tên đăng nhập
            </label>
            <InputField
              id="username"
              v-model="username"
              placeholder="Nhập tên đăng nhập"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              Mật khẩu
            </label>
            <InputField
              id="password"
              type="password"
              v-model="password"
              placeholder="Nhập mật khẩu"
            />
          </div>

          <nav class="flex justify-between text-sm">
            <a href="#" class="text-black hover:text-[#09f]">Quên mật khẩu?</a>
          </nav>

          <button
            type="submit"
            class="w-full py-3 bg-[#09f] hover:bg-blue-600 text-white font-bold rounded-lg transition cursor-pointer disabled:opacity-60"
            :disabled="isChecking"
          >
            {{ isChecking ? 'Đang xử lý...' : 'Đăng nhập' }}
          </button>
        </form>

        <!-- Footer -->
        <footer class="text-center text-gray-400 text-sm">
          © 2025. Edunera. All rights reserved. Developed by Group 6
        </footer>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuth } from '~/composables/useAuth'

const { login, isChecking, validateToken } = useAuth()
const username = ref('')
const password = ref('')
const loginError = ref<string | null>(null)

async function handleLogin() {
  loginError.value = null // Reset lỗi cũ
  const result = await login({
    username: username.value,
    password: password.value,
  })

  if (!result.success) {
    loginError.value = result.message || 'Đã có lỗi xảy ra.'
  }
  // Nếu thành công, composable sẽ tự redirect
}

// Kiểm tra token khi load trang
onMounted(async () => {
  if (typeof localStorage !== 'undefined') {
    const token = localStorage.getItem('token')
    if (token) {
      const isValid = await validateToken()
      if (isValid) {
        await navigateTo('/home')
        return
      }
    }
  }
})

definePageMeta({
  layout: false,
})
</script>
