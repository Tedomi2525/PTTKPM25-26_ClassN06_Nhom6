<template>
  <!-- Dùng lại layout mặc định -->
  <NuxtLayout name="default">
    <template #default>
      <div class="flex min-h-[calc(100vh-64px)] relative">
        <!-- Mobile Menu Button -->
        <button
          @click="toggleMobileSidebar"
          class="lg:hidden fixed top-20 left-4 z-20 bg-gray-800 text-white p-2 rounded-md shadow-lg hover:bg-gray-700 transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path v-if="!isMobileSidebarOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>

        <!-- Sidebar riêng cho Dashboard -->
        <aside
          class="w-64 fixed left-0 top-16 h-[calc(100vh-64px)] bg-gradient-to-b from-white to-white  shadow-lg flex flex-col z-10 transition-transform duration-300 ease-in-out"
          :class="[
            'lg:translate-x-0',
            isMobileSidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
          ]"
        >
          <h2 class="text-lg font-semibold px-4 py-3 border-b border-gray-700 tracking-wide">
            Quản lý Dashboard
          </h2>

          <ul class="flex-1 mt-2 space-y-1 px-2">
            <li v-for="sub in dashboardSubMenu" :key="sub.label">
              <NuxtLink
                :to="sub.href"
                @click="closeMobileSidebar"
                class="block px-4 py-2.5 rounded-lg transition-all duration-200"
                :class="[
                  route.path.startsWith(sub.match)
                    ? 'bg-[#09f] text-white font-medium shadow-sm'
                    : 'hover:bg-gray-200 text-gray-600 hover:text-gray-900'
                ]"
              >
                {{ sub.label }}
              </NuxtLink>
            </li>
          </ul>

          <div class="p-3 border-t border-gray-700 text-sm text-gray-400 text-center">
            © 2025 Admin Panel
          </div>
        </aside>

        <!-- Overlay for mobile -->
        <div
          v-if="isMobileSidebarOpen"
          @click="closeMobileSidebar"
          class="fixed inset-0 bg-black bg-opacity-50 z-5 lg:hidden"
        ></div>

        <!-- Phần nội dung chính -->
        <main class="flex-1 lg:ml-64 bg-gray-50 min-h-[calc(100vh-64px)]">
          <div class="w-full">
            <slot/>
          </div>
        </main>
      </div>
    </template>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue"
import { useRoute } from "vue-router"

const route = useRoute()
const isMobileSidebarOpen = ref(false)

const dashboardSubMenu = [
  { label: "Sinh viên", href: "/Admin/dashboard/student_list", match: "/Admin/dashboard/student" },
  { label: "Giảng viên", href: "/Admin/dashboard/teacher_list", match: "/Admin/dashboard/teacher" },
  { label: "Khoá học", href: "/Admin/dashboard/courses", match: "/Admin/dashboard/course" },
  { label: "Chương trình học", href: "/program/programs", match: "/program/programs" },
]

function toggleMobileSidebar() {
  isMobileSidebarOpen.value = !isMobileSidebarOpen.value
}

function closeMobileSidebar() {
  isMobileSidebarOpen.value = false
}

// Đóng sidebar khi resize về desktop
function handleResize() {
  if (window.innerWidth >= 1024) { // lg breakpoint
    isMobileSidebarOpen.value = false
  }
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>
