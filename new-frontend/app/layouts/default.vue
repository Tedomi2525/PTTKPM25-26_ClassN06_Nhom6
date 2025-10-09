<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, watch } from "vue"
import { useRouter, useRoute } from "vue-router"
import { useAuth } from "@/composables/useAuth"

const open = ref(false)
const { displayName, logout, validateToken, token, role } = useAuth()
const router = useRouter()
const route = useRoute()

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

// MENU
const adminMenuItems = [
  { label: 'Trang chủ', href: '/Home' },
  { label: 'Thời khóa biểu', href: '/Admin/schedule' },
  { label: 'Điểm danh', href: '/Admin/attendance' },
  { label: 'Quản lý', href: '/Admin/dashboard' },
]

const studentMenuItems = [
  { label: 'Thời khóa biểu', href: '/Student/schedule' },
  // { label: 'Điểm danh', href: '/Student/attendance' },
  { label: 'Đăng kí học', href: '/Student/enrollment' }
]

const selectedMenu = ref<string | null>(null)

function handleMenuClick(item: { label: string; href: string }) {
  selectedMenu.value = selectedMenu.value === item.label ? null : item.label
}

watch(
  () => route.path,
  (newPath) => {
    if (newPath.startsWith("/Admin/dashboard")) {
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
    <div class="bg-[#09f] text-white  fixed w-full flex flex-col z-10">
      <div class="mx-auto w-full px-42">
        <div class="flex justify-between h-16 items-center">
          <!-- Logo -->
          <NuxtLink to="/Admin/dashboard" class="text-xl font-bold">
            EDUNERA
          </NuxtLink>

          <!-- Navigation Menu -->
          <NavBar
            v-if="isAdmin"
            :items="adminMenuItems"
            @menu-click="handleMenuClick"
          />
          <NavBar v-if="isStudent" :items="studentMenuItems" />

          <!-- User Dropdown -->
          <div class="relative user-dropdown">
            <button @click="toggleMenu" class="px-3 py-1 rounded hover:text-gray-300">
              Xin chào, {{ displayName }}
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
    <main class="flex-1 pt-16">
      <slot />
    </main>
  </div>
</template>
