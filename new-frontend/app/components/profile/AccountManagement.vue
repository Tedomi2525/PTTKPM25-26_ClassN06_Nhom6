<template>
  <div class="p-4 flex flex-col items-center w-full font-medium max-w-md mx-auto">
    <!-- Form -->
    <div class="w-full space-y-5">
      <!-- Mật khẩu hiện tại -->
      <div class="relative">
        <input
          id="currentPassword"
          type="password"
          v-model="currentPassword"
          placeholder=" "
          class="peer w-full border border-gray-300 rounded-md p-2 pt-6 text-gray-900 text-sm placeholder-transparent focus:border-blue-500 focus:ring-1 focus:ring-blue-100 outline-none transition-all"
        />
        <label
          for="currentPassword"
          class="absolute left-2 top-3 text-gray-500 text-xs font-semibold transition-all
                 peer-placeholder-shown:top-3.5 peer-placeholder-shown:text-sm peer-placeholder-shown:text-gray-400
                 peer-focus:top-2 peer-focus:text-xs peer-focus:text-blue-600"
        >
          Mật khẩu hiện tại
        </label>
      </div>

      <!-- Mật khẩu mới -->
      <div class="relative">
        <input
          id="newPassword"
          type="password"
          v-model="newPassword"
          placeholder=" "
          class="peer w-full border border-gray-300 rounded-md p-2 pt-6 text-gray-900 text-sm placeholder-transparent focus:border-blue-500 focus:ring-1 focus:ring-blue-100 outline-none transition-all"
        />
        <label
          for="newPassword"
          class="absolute left-2 top-3 text-gray-500 text-xs font-semibold transition-all
                 peer-placeholder-shown:top-3.5 peer-placeholder-shown:text-sm peer-placeholder-shown:text-gray-400
                 peer-focus:top-2 peer-focus:text-xs peer-focus:text-blue-600"
        >
          Mật khẩu mới
        </label>
      </div>

      <!-- Xác nhận mật khẩu -->
      <div class="relative">
        <input
          id="confirmPassword"
          type="password"
          v-model="confirmPassword"
          placeholder=" "
          class="peer w-full border border-gray-300 rounded-md p-2 pt-6 text-gray-900 text-sm placeholder-transparent focus:border-blue-500 focus:ring-1 focus:ring-blue-100 outline-none transition-all"
        />
        <label
          for="confirmPassword"
          class="absolute left-2 top-3 text-gray-500 text-xs font-semibold transition-all
                 peer-placeholder-shown:top-3.5 peer-placeholder-shown:text-sm peer-placeholder-shown:text-gray-400
                 peer-focus:top-2 peer-focus:text-xs peer-focus:text-blue-600"
        >
          Xác nhận mật khẩu
        </label>
      </div>
    </div>

    <!-- Nút đổi mật khẩu -->
    <div class="w-full flex justify-end mt-6">
      <CButton
        @click="handleSave"
        :disabled="!canSubmit"
        variant="primary"
      >
        Đổi mật khẩu
      </CButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, inject } from 'vue'
import CButton from '@/components/CButton.vue'

const props = defineProps<{ user: any; student: any }>()

const reloadData = inject('reloadUserData') as () => Promise<void>
const setError = inject('setError') as (show: boolean, message?: string, details?: string) => void

const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')

const canSubmit = computed(() =>
  currentPassword.value && newPassword.value && confirmPassword.value
)

const handleSave = async () => {
  if (newPassword.value !== confirmPassword.value) {
    alert('Mật khẩu mới và xác nhận mật khẩu không khớp')
    return
  }

  try {
    console.log('Đổi mật khẩu:', {
      currentPassword: currentPassword.value,
      newPassword: newPassword.value
    })

    if (reloadData) await reloadData()

    currentPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''

    alert('Đổi mật khẩu thành công!')
  } catch (error) {
    console.error(error)
    if (setError)
      setError(true, 'Password change failed', error instanceof Error ? error.message : 'Unknown error')
  }
}
</script>
