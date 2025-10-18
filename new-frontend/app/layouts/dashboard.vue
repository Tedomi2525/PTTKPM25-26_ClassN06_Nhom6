<template>
  <NuxtLayout name="default">
    <template #default>
      <div class="flex min-h-[calc(100vh-64px)] ">
        
        <aside
          class="h-[calc(100vh-64px)] bg-gradient-to-b from-white to-white shadow-lg flex flex-col z-10 transition-all duration-300 ease-in-out fixed top-16 left-0 right-0"
          :class="{
            'w-64': !isAsideCollapsed,
            'w-20': isAsideCollapsed,
            'flex-shrink-0': true
          }"
        >
          <div class="flex items-center px-4 py-3 border-b border-gray-200"
               :class="{ 'justify-between': !isAsideCollapsed, 'justify-center': isAsideCollapsed }">
            <h2 v-if="!isAsideCollapsed" class="text-lg font-semibold tracking-wide text-black truncate">
              Quản lý
            </h2>
            <button 
              @click="toggleAside" 
              class="p-2 rounded-full hover:bg-gray-200 text-gray-600 hover:text-gray-900 transition-colors"
              :class="{ 'ml-auto': !isAsideCollapsed, 'mx-auto': isAsideCollapsed }"
              aria-label="Toggle sidebar"
            >
              <svg class="w-6 h-6 transform transition-transform duration-300 ease-in-out" 
                   :class="{ 'rotate-180': isAsideCollapsed }" 
                   fill="none" 
                   stroke="currentColor" 
                   viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7"></path>
              </svg>
            </button>
          </div>
          
          <hr class="w-[95%] mx-auto border-gray-200" /> 
          
          <ul class="flex-1 mt-2 space-y-1 px-2">
            <li v-for="sub in dashboardSubMenu" :key="sub.label">
              <NuxtLink
                :to="sub.href"
                class="flex items-center gap-3 px-4 py-2.5 rounded-lg transition-all duration-200"
                :class="[
                  route.path.startsWith(sub.match)
                    ? 'bg-[#09f] text-white font-medium shadow-sm'
                    : 'hover:bg-gray-200 text-gray-600 hover:text-gray-900',
                  { 'justify-center': isAsideCollapsed, 'w-full': isAsideCollapsed }
                ]"
              >
                <span class="flex-shrink-0">
                  <img v-if="sub.label === 'Sinh viên'" src="/images/student-50.png" alt="Sinh viên" class="w-6 h-6 object-contain" />
                  <img v-else-if="sub.label === 'Giảng viên'" src="/images/icons8-lecturer-50.png" alt="Giảng viên" class="w-6 h-6 object-contain" />
                  <svg v-else-if="sub.label === 'Học phần' || sub.label === 'Chương trình học'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.206 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.794 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.794 5 16.5 5s3.332.477 4.5 1.253v13C19.832 18.477 18.206 18 16.5 18s-3.332.477-4.5 1.253"/>
                  </svg>
                  <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                  </svg>
                </span>
                <span v-if="!isAsideCollapsed" class="truncate">
                  {{ sub.label }}
                </span>
              </NuxtLink>
            </li>
          </ul>

          <div v-if="!isAsideCollapsed" class="p-3 text-sm text-gray-400 text-center">
            © 2025 Admin Panel
          </div>
          <div v-else class="p-3 text-sm text-gray-400 text-center truncate">
             ©
          </div>
        </aside>

      <main 
        class="flex-1 bg-gray-50 min-h-[calc(100vh-64px)] transition-all duration-300 ease-in-out"
        :style="{
          marginLeft: isAsideCollapsed ? '5rem' : '16rem'  // w-20 = 5rem, w-64 = 16rem
        }"
      >
        <div class="relative">
          <slot/>
        </div>
      </main>
      </div>
    </template>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { useRoute } from "vue-router"

const route = useRoute()

const isAsideCollapsed = ref(false) // Trạng thái ẩn/hiện của aside

const dashboardSubMenu = [
  { label: "Sinh viên", href: "/admin/dashboard/student_list", match: "/admin/dashboard/student" },
  { label: "Giảng viên", href: "/admin/dashboard/teacher_list", match: "/admin/dashboard/teacher" },
  { label: "Học phần", href: "/admin/dashboard/courses", match: "/admin/dashboard/course" },
  { label: "Chương trình học", href: "/admin/dashboard/program/programs", match: "/admin/dashboard/program" },
]

function toggleAside() {
  isAsideCollapsed.value = !isAsideCollapsed.value
}
</script>