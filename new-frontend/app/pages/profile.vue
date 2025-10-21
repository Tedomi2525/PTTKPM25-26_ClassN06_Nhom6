<template>
<div class="mx-auto px-4 bg-gray-50 grid grid-cols-12">
  <div class="col-span-1">

  </div>
  <!-- Sidebar left -->
  <nav
    class="self-start font-bold text-2xl col-span-12 lg:col-span-2 sticky top-32 h-fit hidden lg:block"
  >
    <h1 class="text-4xl font-bold mb-8 text-gray-800 whitespace-nowrap">
      Hồ sơ cá nhân
    </h1>
    <ul class="space-y-2 justify-center">
      <li
        v-for="(section, index) in sections"
        :key="index"
        :class="{
          'text-[#09f] font-bold': activeSection === section.id, 
          'text-gray-600 hover:text-[#09f]': activeSection !== section.id,
          'cursor-pointer transition-colors duration-200 whitespace-nowrap': true
        }"
        @click="scrollToSection(section.id)"
      >
        {{ section.label }}
      </li>
    </ul>
  </nav>

  <!-- Content right -->
  <div class="col-span-12 lg:col-span-8 pt-8 rounded-lg">
    <ErrorNotification
      :message="errorMessage"
      :details="errorDetails"
      :show="showError"
      closable
      @close="closeError"
    />

    <section
      v-for="(section, index) in sections"
      :key="index"
      :id="section.id"
      class="rounded-lg shadow-lg border border-gray-200 flex overflow-hidden hover:shadow-xl transition-shadow duration-300 mb-10"
    >
      <div class="w-3/9 bg-gradient-to-br from-[#09f] to-[#008ae6] p-8 text-white">
        <h2 class="font-bold text-2xl mb-2 ">{{ section.label }}</h2>
        <p class="text-blue-100 text-sm leading-relaxed">{{ section.description }}</p>
      </div>

      <div class="w-6/9 bg-white p-8">
        <component
          :is="sectionComponents[section.id]"
          :user="userRef"
          :student="student"
        />
      </div>
    </section>
    <div class="h-[63vh]"></div>
  </div>
</div>

</template>

<script setup lang="ts">
import { ref, onMounted, provide } from 'vue'
import { useAuth } from '~/composables/useAuth'
import UUID from '~/components/profile/UUID.vue'
import AccountManagement from '~/components/profile/AccountManagement.vue'
import PersonalInformation from '~/components/profile/PersonalInformation.vue'
import StudentInfo from '~/components/profile/StudentInfo.vue'
import ErrorNotification from '~/components/ErrorMessage.vue'
import type { Ref } from 'vue'
import Avatar from '~/components/profile/Avatar.vue'


const { user, initAuth } = useAuth()  // user là Ref<User | null>
const { student, studentInit, updateStudent } = useSchool()

// reactive ref để truyền xuống child
const userRef = user

const showError = ref(false)
const errorMessage = ref('')
const errorDetails = ref('')

function setError(show: boolean, message = '', details = '') {
  showError.value = show
  errorMessage.value = message
  errorDetails.value = details
}

function closeError() {
  showError.value = false
}

// Reload data function
async function reloadUserData() {
  await initAuth()
  if (user.value?.schoolId) {
    await studentInit(user.value.schoolId)
  }
}

// Provide the reload function to child components
provide('reloadUserData', reloadUserData)
provide('setError', setError)

// Scroll & highlight section
const sections = [
  { id: 'uuid', label: 'UUID', description: 'Mã định danh duy nhất trong hệ thống' },
  { id: 'personal-info', label: 'Thông tin cá nhân', description: 'Thông tin cá nhân cơ bản' },
  { id: 'avatar', label: 'Ảnh đại diện', description: 'Ảnh đại diện của bạn' },
  { id: 'student-info', label: 'Thông tin sinh viên', description: 'Thông tin liên quan đến việc học' },
  { id: 'account-management', label: 'Quản lý tài khoản', description: 'Quản lý tài khoản và bảo mật' },
]

const sectionComponents: Record<string, any> = {
  'uuid': UUID,
  'avatar': Avatar,
  'personal-info': PersonalInformation,
  'account-management': AccountManagement,
  'student-info': StudentInfo
}

const activeSection = ref('uuid')

function scrollToSection(id: string) {
  const el = document.getElementById(id)
  if (el) {
    const y = el.getBoundingClientRect().top + window.scrollY
    window.scrollTo({ top: y - 128, behavior: 'smooth' })
  }
}

function onScroll() {
  for (const section of sections) {
    const el = document.getElementById(section.id)
    if (el) {
      const rect = el.getBoundingClientRect()
      if (rect.top <= 150 && rect.bottom > 150) {
        activeSection.value = section.id
        break
      }
    }
  }
}

onMounted(async () => {
  await initAuth()
  if (user.value?.schoolId) {
    await studentInit(user.value.schoolId)
  }
  window.addEventListener('scroll', onScroll)
})
</script>