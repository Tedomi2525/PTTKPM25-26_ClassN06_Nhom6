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
          :class="{
            'border-red-300 focus:border-red-500': newPassword && newPassword.length < 8,
            'border-green-300 focus:border-green-500': newPassword && newPassword.length >= 8
          }"
        />
        <label
          for="newPassword"
          class="absolute left-2 top-3 text-gray-500 text-xs font-semibold transition-all
                 peer-placeholder-shown:top-3.5 peer-placeholder-shown:text-sm peer-placeholder-shown:text-gray-400
                 peer-focus:top-2 peer-focus:text-xs peer-focus:text-blue-600"
        >
          Mật khẩu mới
        </label>
        <!-- Password strength indicator -->
        <div v-if="newPassword" class="text-xs mt-1">
          <span v-if="newPassword.length < 8" class="text-red-500">
            Mật khẩu phải có ít nhất 8 ký tự
          </span>
          <span v-else class="text-green-500">
            Mật khẩu hợp lệ
          </span>
        </div>
      </div>

      <!-- Xác nhận mật khẩu -->
      <div class="relative">
        <input
          id="confirmPassword"
          type="password"
          v-model="confirmPassword"
          placeholder=" "
          class="peer w-full border border-gray-300 rounded-md p-2 pt-6 text-gray-900 text-sm placeholder-transparent focus:border-blue-500 focus:ring-1 focus:ring-blue-100 outline-none transition-all"
          :class="{
            'border-red-300 focus:border-red-500': confirmPassword && newPassword && confirmPassword !== newPassword,
            'border-green-300 focus:border-green-500': confirmPassword && newPassword && confirmPassword === newPassword
          }"
        />
        <label
          for="confirmPassword"
          class="absolute left-2 top-3 text-gray-500 text-xs font-semibold transition-all
                 peer-placeholder-shown:top-3.5 peer-placeholder-shown:text-sm peer-placeholder-shown:text-gray-400
                 peer-focus:top-2 peer-focus:text-xs peer-focus:text-blue-600"
        >
          Xác nhận mật khẩu
        </label>
        <!-- Password match indicator -->
        <div v-if="confirmPassword && newPassword" class="text-xs mt-1">
          <span v-if="confirmPassword !== newPassword" class="text-red-500">
            Mật khẩu không khớp
          </span>
          <span v-else class="text-green-500">
            Mật khẩu khớp
          </span>
        </div>
      </div>
    </div>

    <!-- Nút đổi mật khẩu -->
    <div class="w-full flex justify-end mt-6">
      <CButton
        @click="handleSave"
        :disabled="!canSubmit"
        variant="primary"
      >
        {{ isSubmitting ? 'Đang xử lý...' : 'Đổi mật khẩu' }}
      </CButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, inject } from 'vue'
import CButton from '@/components/CButton.vue'
import { useAuth } from '@/composables/useAuth'

const props = defineProps<{ user: any; student: any }>()

const reloadData = inject<() => Promise<void>>('reloadUserData')
const setError = inject<(show: boolean, message?: string, details?: string) => void>('setError')

const { changePassword } = useAuth()

const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const isSubmitting = ref(false)

const canSubmit = computed(() =>
  currentPassword.value && 
  newPassword.value && 
  confirmPassword.value && 
  !isSubmitting.value
)

const handleSave = async () => {
  // Client-side validation
  if (newPassword.value !== confirmPassword.value) {
    if (setError) {
      setError(true, 'Lỗi xác nhận mật khẩu', 'Mật khẩu mới và xác nhận mật khẩu không khớp')
    } else {
      alert('Mật khẩu mới và xác nhận mật khẩu không khớp')
    }
    return
  }

  if (newPassword.value.length < 8) {
    if (setError) {
      setError(true, 'Mật khẩu không hợp lệ', 'Mật khẩu mới phải có ít nhất 8 ký tự')
    } else {
      alert('Mật khẩu mới phải có ít nhất 8 ký tự')
    }
    return
  }

  if (currentPassword.value === newPassword.value) {
    if (setError) {
      setError(true, 'Mật khẩu không hợp lệ', 'Mật khẩu mới phải khác với mật khẩu hiện tại')
    } else {
      alert('Mật khẩu mới phải khác với mật khẩu hiện tại')
    }
    return
  }

  isSubmitting.value = true

  try {
    const result = await changePassword(
      currentPassword.value,
      newPassword.value,
      confirmPassword.value
    )

    if (result.success) {
      // Clear form
      currentPassword.value = ''
      newPassword.value = ''
      confirmPassword.value = ''

      // Reload user data if available
      if (reloadData) await reloadData()

      // Show success message
      if (setError) {
        // If setError is available, we could use it for success too
        alert(result.message)
      } else {
        alert(result.message)
      }
    } else {
      // Show error message
      if (setError) {
        setError(true, 'Đổi mật khẩu thất bại', result.message)
      } else {
        alert(result.message)
      }
    }
  } catch (error) {
    console.error('Unexpected error during password change:', error)
    const errorMessage = error instanceof Error ? error.message : 'Có lỗi không xác định xảy ra'
    
    if (setError) {
      setError(true, 'Lỗi hệ thống', errorMessage)
    } else {
      alert('Có lỗi xảy ra: ' + errorMessage)
    }
  } finally {
    isSubmitting.value = false
  }
}
</script>
