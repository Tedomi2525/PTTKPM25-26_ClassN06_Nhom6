<template>
  <!-- Dùng lại layout mặc định -->
  <NuxtLayout name="default">
    <template #default>
      <div class="flex flex-1 ">
        <!-- Sidebar riêng cho Dashboard -->
        <aside
          class="min-w-[250px] h-[calc(100vh-64px)] bg-gradient-to-b from-gray-800 to-gray-900 text-gray-100 shadow-lg flex flex-col"
        >
          <h2 class="text-lg font-semibold px-4 py-3 border-b border-gray-700 tracking-wide">
            Quản lý Dashboard
          </h2>

          <ul class="flex-1 mt-2 space-y-1 px-2">
            <li v-for="sub in dashboardSubMenu" :key="sub.label">
              <NuxtLink
                :to="sub.href"
                class="block px-4 py-2.5 rounded-lg transition-all duration-200"
                :class="[
                  route.path.startsWith(sub.match)
                    ? 'bg-blue-600 text-white font-medium shadow-sm'
                    : 'hover:bg-gray-700 hover:text-white text-gray-300'
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

        <!-- Phần nội dung chính -->
        <main class="flex-1 p-4">
          <slot/>
        </main>
      </div>
    </template>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router"

const route = useRoute()

const dashboardSubMenu = [
  { label: "Học sinh", href: "/Admin/dashboard/student_list", match: "/Admin/dashboard/student" },
  { label: "Giáo viên", href: "/Admin/dashboard/teacher_list", match: "/Admin/dashboard/teacher" },
  { label: "Khoá học", href: "/Admin/dashboard/courses", match: "/Admin/dashboard/course" },
]
</script>
