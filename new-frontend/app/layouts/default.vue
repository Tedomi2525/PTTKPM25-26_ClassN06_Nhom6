<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from "vue"
import { useRouter } from "vue-router"
import { useAuth } from "@/composables/useAuth"

const open = ref(false)
const { displayName, logout, validateToken, token, role } = useAuth()
const router = useRouter()

const isAdmin = computed(() => role.value === "admin")
const isStudent = computed(() => role.value === "student")
// toggle menu
function toggleMenu() {
  open.value = !open.value
}

// logout
function handleLogout() {
  logout()
  open.value = false
}

// Lấy tên user và role khi mounted
onMounted(async () => {
  if (!token.value) {
    router.push("/")
    return
  }
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

const adminMenuItems = [
  { label: 'Dashboard', href: '/Admin/dashboard' },
  { label: 'Sinh viên', href: '/Admin/student_list' },
  { label: 'Giáo viên', href: '/Admin/teacher_list' },
  { label: 'Khóa học', href: '/Admin/courses' },
  { label: 'Điểm danh', href: '/Admin/attendance' }
]

const studentMenuItems = [
  { label: 'Dashboard', href: '/Student/dashboard' },
  { label: 'Khóa học của tôi', href: '/Student/schedule' },
  { label: 'Điểm danh', href: '/Student/attendance' }
]

</script>

<template>
  <div class="bg-gray-100 min-h-screen">
    <!-- HEADER / NAVBAR -->
    <div class="bg-[#09f] text-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <!-- Logo -->
          <NuxtLink to="/Admin/dashboard" class="text-xl font-bold">Hệ thống Quản lý</NuxtLink>
          <!-- Navigation Menu -->
          <NavBar v-if="isAdmin" :items="adminMenuItems" />
          <NavBar v-if="isStudent" :items="studentMenuItems" />
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
    </div>

    <main>
      <slot />
    </main>
  </div>
</template>