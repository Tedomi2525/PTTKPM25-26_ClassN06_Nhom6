<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue"
import { useRouter } from "vue-router"
import { useAuth } from "@/composables/useAuth"

const open = ref(false)
const { displayName, logout, validateToken, token } = useAuth()
const router = useRouter()

// toggle menu
function toggleMenu() {
  open.value = !open.value
}

// logout
function handleLogout() {
  logout()
  open.value = false
}

// Lấy tên user khi mounted
onMounted(async () => {
  if (!token.value) {
    router.push("/")
    return
  }

  // validateToken sẽ tự động cập nhật displayName nếu thành công
  await validateToken()
})

// click ngoài đóng dropdown
onMounted(() => {
  const handler = (e: MouseEvent) => {
    const target = e.target as HTMLElement
    if (!target.closest(".user-dropdown")) {
      open.value = false
    }
  }
  document.addEventListener("click", handler)
  onUnmounted(() => document.removeEventListener("click", handler))
})

console.log(displayName)

</script>

<template>
  <div class="bg-gray-100 min-h-screen">
    <!-- HEADER / NAVBAR -->
    <nav class="bg-[#09f] text-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <!-- Logo -->
          <NuxtLink to="/Admin/dashboard" class="text-xl font-bold">Hệ thống Quản lý</NuxtLink>

          <!-- Menu -->
          <div class="hidden md:flex space-x-6">
            <NuxtLink to="/Admin/student_list" class="hover:text-gray-300">Sinh viên</NuxtLink>
            <NuxtLink to="/Admin/teacher_list" class="hover:text-gray-300">Giảng viên</NuxtLink>
          </div>

          <!-- User Dropdown -->
          <div class="relative user-dropdown">
            <button @click="toggleMenu" class="px-3 py-1 rounded hover:text-gray-300">
              Xin chào, {{ displayName }}
            </button>
            <ul v-if="open" class="absolute right-0 bg-white text-gray-800 mt-2 rounded shadow-lg">
              <li>
                <button @click="handleLogout" class="block px-4 py-2 hover:bg-gray-100 w-full text-left">
                  Đăng xuất
                </button>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </nav>

    <main>
      <slot />
    </main>
  </div>
</template>
