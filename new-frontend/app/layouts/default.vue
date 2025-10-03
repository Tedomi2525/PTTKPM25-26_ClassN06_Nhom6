<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from "vue"
import { useRouter } from "vue-router"
import { useAuth } from "@/composables/useAuth"

const open = ref(false)
const { displayName, logout, validateToken, token, role } = useAuth()
const router = useRouter()

const isAdmin = computed(() => role.value === "admin")
const isStudent = computed(() => role.value === "student")

function toggleMenu() {
  open.value = !open.value
}

function handleLogout() {
  logout()
  open.value = false
}

onMounted(async () => {
  if (!token.value) {
    router.push("/")
    return
  }
  await validateToken()
})

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

// menu chính
const adminMenuItems = [
  { label: 'Dashboard', href: '/Admin/dashboard' },
  { label: 'Thời khóa biểu', href: '/Admin/schedule' },
  { label: 'Điểm danh', href: '/Admin/attendance' },
]

const studentMenuItems = [
  { label: 'Thời khóa biểu', href: '/Student/schedule' },
  { label: 'Điểm danh', href: '/Student/attendance' }
]

// submenu của Dashboard
const dashboardSubMenu = [
  { label: 'Học sinh', href: '/Admin/student_list' },
  { label: 'Giáo viên', href: '/Admin/teacher_list' },
  { label: 'Khoá học', href: '/Admin/courses' }
]

const selectedMenu = ref<string | null>(null)

function handleMenuClick(item: { label: string; href: string }) {
  if (selectedMenu.value === item.label) {
    // Nếu đang click lại đúng menu đó thì tắt
    selectedMenu.value = null
  } else {
    selectedMenu.value = item.label
  }
}
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
          <NavBar
            v-if="isAdmin"
            :items="adminMenuItems"
            @menu-click="handleMenuClick"
          />
          <NavBar
            v-if="isStudent"
            :items="studentMenuItems"
          />

          <!-- User Dropdown -->
          <div class="relative user-dropdown">
            <button @click="toggleMenu" class="px-3 py-1 rounded hover:text-gray-300">
              Xin chào, {{ displayName }}
            </button>
            <ul v-if="open" class="absolute right-0 bg-white text-gray-800 mt-2 rounded shadow-lg">
              <li>
                <button
                  @click="handleLogout"
                  class="block px-4 py-2 hover:bg-gray-100 w-full text-left"
                >
                  Đăng xuất
                </button>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- MAIN CONTENT + SIDEBAR -->
    <div class="flex">
      <!-- Sidebar chỉ hiển thị khi chọn Dashboard -->
      <aside v-if="selectedMenu === 'Dashboard'" class="w-64 bg-gray-200 p-4">
        <ul>
          <li v-for="sub in dashboardSubMenu" :key="sub.label">
            <NuxtLink
              :to="sub.href"
              class="block py-2 px-3 hover:bg-gray-300 rounded"
            >
              {{ sub.label }}
            </NuxtLink>
          </li>
        </ul>
      </aside>

      <!-- Nội dung chính -->
      <main class="flex-1 p-4">
        <slot />
      </main>
    </div>
  </div>
</template>
