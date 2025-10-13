<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, watch } from "vue"
import { useRouter, useRoute } from "vue-router"
import { useAuth } from "@/composables/useAuth"

const open = ref(false)
const { displayName, logout, validateToken, token, role, avatar, user, isLoggingOut } = useAuth()
const router = useRouter()
const route = useRoute()

const isAdmin = computed(() => role.value === "admin")
const isStudent = computed(() => role.value === "student")
const isTeacher = computed(() => role.value === "teacher")

const avatarUrl = computed(() => {
  if (!avatar.value) return '/images/default-avatar.svg'
  if (avatar.value.startsWith('http')) return avatar.value
  return `http://127.0.0.1:8000${avatar.value.startsWith('/') ? avatar.value : '/' + avatar.value}`
})

function showDropdown() {
  open.value = true
}

function hideDropdown() {
  open.value = false
}

function handleLogout() {
  if (isLoggingOut.value) return // Prevent multiple logout calls
  
  open.value = false
  logout()
}

function handleImageError(event: Event) {
  const img = event.target as HTMLImageElement
  img.src = '/images/default-avatar.svg'
}

// Note: Removed click outside handler since we're using hover now

// Validate token
onMounted(async () => {
  if (!token.value) {
    router.push("/")
    return
  }
  await validateToken()
})

// MENU
const adminMenuItems = [
  { label: 'Trang chủ', href: '/home' },
  { label: 'Thời khóa biểu', href: '/admin/schedule' },
  { label: 'Điểm danh', href: '/admin/attendance' },
  { label: 'Quản lý', href: '/admin/dashboard' },
]

const studentMenuItems = computed(() => {
  const baseItems = [
    { label: 'Thời khóa biểu', href: '/student/schedule' },
    { 
      label: 'Đăng kí học', 
      dropdown: [
        { label: 'Đăng ký học', href: '/student/enrollment' },
        { label: 'Kết quả đăng ký', href: '/student/enrollment-result' }
      ]
    }
  ]
  return baseItems
})

const teacherMenuItems = computed(() => {
  const baseItems = [
    { label: 'Thời khóa biểu', href: '/teacher/schedule' },
  ]
  return baseItems
})

const selectedMenu = ref<string | null>(null)

function handleMenuClick(item: { label: string; href: string }) {
  selectedMenu.value = selectedMenu.value === item.label ? null : item.label
}

watch(
  () => route.path,
  (newPath) => {
    if (newPath.startsWith("/admin/dashboard")) {
      selectedMenu.value = "Dashboard"
    } else {
      selectedMenu.value = null
    }
  },
  { immediate: true }
)
</script>

<template>
<div class="bg-gray-100 min-h-screen">
  <!-- HEADER / NAVBAR -->
  <header class="bg-blue-500 text-white fixed w-full flex flex-col z-50 shadow-md">
    <div class="mx-auto min-w-[70%]">
      <div class="flex justify-between h-16 items-center px-4">
        <!-- Logo -->
        <NuxtLink to="/" class="text-xl font-bold">QLDT</NuxtLink>

        <!-- Navigation Menu -->
        <NavBar
          v-if="isAdmin"
          :items="adminMenuItems"
          @menu-click="handleMenuClick"
        />
        <NavBar
          v-if="isStudent"
          :items="studentMenuItems"
          @menu-click="handleMenuClick"
        />
        <NavBar
          v-if="isTeacher"
          :items="teacherMenuItems"
          @menu-click="handleMenuClick"
        />

        <!-- User Dropdown -->
        <div 
          class="relative user-dropdown"
          @mouseenter="showDropdown"
          @mouseleave="hideDropdown"
        >
          <button
            class="flex items-center px-3 py-1 rounded-lg hover:bg-white/20 transition-all duration-200"
          >
            <img 
              :src="avatarUrl" 
              alt="avatar" 
              class="w-10 h-10 rounded-full object-cover border-2 border-white/30 mr-3"
              @error="handleImageError"
            />
            <span class="font-medium">{{ displayName }}</span>
            <svg
              class="w-4 h-4 ml-2 text-white transition-transform duration-200"
              :class="{ 'rotate-180': open }"
              fill="none" stroke="currentColor" viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>

          <transition
            enter-active-class="transition ease-out duration-200"
            enter-from-class="opacity-0 transform -translate-y-2"
            enter-to-class="opacity-100 transform translate-y-0"
            leave-active-class="transition ease-in duration-150"
            leave-from-class="opacity-100 transform translate-y-0"
            leave-to-class="opacity-0 transform -translate-y-2"
          >
            <div 
              v-if="open"
              class="absolute right-0 pt-2 w-48 z-50"
            >
              <!-- Triangle pointer -->
              <div class="flex justify-end pr-4">
                <div class="w-0 h-0 border-l-[8px] border-l-transparent border-r-[8px] border-r-transparent border-b-[8px] border-b-white"></div>
              </div>
              <!-- Dropdown content -->
              <ul class="bg-white rounded-lg shadow-xl border border-gray-200 overflow-hidden mt-0">
              <li>
                <button
                  @click="handleLogout"
                  :disabled="isLoggingOut"
                  class="flex items-center px-4 py-2 w-full text-left transition-colors duration-200"
                  :class="isLoggingOut 
                    ? 'text-gray-400 cursor-not-allowed bg-gray-100' 
                    : 'text-gray-800 hover:bg-blue-100 hover:text-blue-700'"
                >
                  <svg v-if="!isLoggingOut" class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7" />
                  </svg>
                  <svg v-else class="w-4 h-4 mr-2 animate-spin" fill="none" viewBox="0 0 24 24">
                    <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" class="opacity-25"></circle>
                    <path fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" class="opacity-75"></path>
                  </svg>
                  {{ isLoggingOut ? 'Đang đăng xuất...' : 'Đăng xuất' }}
                </button>
              </li>
              <li>
                <NuxtLink
                  to="/profile"
                  class="flex items-center px-4 py-2 text-gray-800 hover:bg-blue-100 hover:text-blue-700 transition-colors duration-200"
                >
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A12.045 12.045 0 0112 15c3.314 0 6.314 1.356 8.879 3.555M12 3a9 9 0 019 9v0a9 9 0 11-18 0v0a9 9 0 019-9z" />
                  </svg>
                  Hồ sơ cá nhân
                </NuxtLink>
              </li>
              </ul>
            </div>
          </transition>
        </div>
      </div>
    </div>
  </header>

  <!-- MAIN CONTENT -->
  <main class="pt-16">
    <slot />
  </main>
</div>
</template>
