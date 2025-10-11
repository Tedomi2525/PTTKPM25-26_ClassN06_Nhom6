<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, watch } from "vue"
import { useRouter, useRoute } from "vue-router"
import { useAuth } from "@/composables/useAuth"

const open = ref(false)
const { displayName, logout, validateToken, token, role, avatar, user } = useAuth()
const router = useRouter()
const route = useRoute()

const isAdmin = computed(() => role.value === "admin")
const isStudent = computed(() => role.value === "student")

const avatarUrl = computed(() => {
  if (!avatar.value) {
    // Avatar mặc định khi không có avatar
    return '/images/default-avatar.svg'
  }
  
  // Nếu avatar đã có đầy đủ URL (http/https)
  if (avatar.value.startsWith('http')) {
    return avatar.value
  }
  
  // Nếu avatar là relative path, nối với base URL
  return `http://127.0.0.1:8000${avatar.value.startsWith('/') ? avatar.value : '/' + avatar.value}`
})

console.log("Avatar URL:", avatarUrl.value);

function toggleMenu() {
  open.value = !open.value
}

function handleLogout() {
  logout()
  open.value = false
}

function handleImageError(event: Event) {
  const img = event.target as HTMLImageElement
  img.src = '/images/default-avatar.svg'
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
    // { label: 'Điểm danh', href: '/student/attendance' },
    { label: 'Đăng kí học', href: '/student/enrollment' }
  ]
  
  // Trang profile hiện tại được thiết kế cho user đang đăng nhập
  // Không cần dynamic ID vì chỉ hiển thị thông tin của chính user đó
  baseItems.push({ label: 'Hồ sơ cá nhân', href: '/student/profile' })
  
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
  <div class="bg-gray-100">
    <!-- HEADER / NAVBAR -->
    <div class="bg-[#09f] text-white  fixed w-full flex flex-col z-10">
      <div class="mx-auto min-w-[50%]">
        <div class="flex justify-between h-16 items-center">
          <!-- Logo -->
          <NuxtLink to="/admin/dashboard" class="text-xl font-bold">
            EDUNERA
          </NuxtLink>

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



          <!-- User Dropdown -->
          <div class="relative user-dropdown">
            
            <button @click="toggleMenu" class="px-3 py-1 rounded hover:text-gray-300 flex items-center">
              <div class="mr-3">
                <img 
                  :src="avatarUrl" 
                  alt="avatar" 
                  class="w-10 h-10 rounded-full object-cover border-2 border-white/20" 
                  @error="handleImageError"
                />
              </div>
              {{ displayName }}
            </button>
            <ul
              v-if="open"
              class="absolute right-0 bg-white text-gray-800 mt-2 rounded shadow-lg"
            >
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
      

    <!-- MAIN CONTENT -->
    <main class="flex-1 pt-16 h-full">
      <slot />
    </main>
  </div>
</template>
