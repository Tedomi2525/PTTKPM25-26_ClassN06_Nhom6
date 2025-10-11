<template>
  <div class="p-3 flex flex-col items-center font-semibold">
    <!-- Grid Layout (desktop only) -->
    <div class="grid grid-cols-1 w-full">
      <!-- UUID -->
      <div class="relative w-full col-span-1 mb-4">
        <input
          id="user_id"
          type="text"
          v-model="user_id"
          readonly
          placeholder=" "
          class="peer w-full border border-gray-300 rounded-lg p-2 pt-6 text-gray-900 text-lg font-medium placeholder-transparent 
                focus:border-gray-300 focus:ring-0 cursor-default bg-gray-50"
        />
        <label
          for="user_id"
          class="absolute left-2 top-3 text-gray-500 text-sm font-semibold transition-all duration-200 
                peer-placeholder-shown:top-4 peer-placeholder-shown:text-gray-400 peer-placeholder-shown:text-base 
                peer-focus:top-2 peer-focus:text-xs peer-focus:text-blue-600"
        >
          UUID
        </label>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, inject, computed } from 'vue'
import { useAuth } from '~/composables/useAuth'

const props = defineProps<{
  user: any
  student: any
}>()

const { user: authUser } = useAuth()

const user_id = computed(() => {
  return props.user?.user_id || props.user?.id || authUser.value?.id || ''
})

const reloadData = inject('reloadUserData') as () => Promise<void>
const setError = inject('setError') as (
  show: boolean,
  message?: string,
  details?: string
) => void

const nickname = ref(props.user?.nickname || props.user?.fullName || '')
const originalNickname = ref(props.user?.nickname || props.user?.fullName || '')

const isChanged = computed(() => nickname.value !== originalNickname.value)

watch(
  () => props.user,
  (newUser) => {
    if (newUser) {
      nickname.value = newUser.nickname || newUser.fullName || ''
      originalNickname.value = newUser.nickname || newUser.fullName || ''
    }
  }
)

async function handleSave() {
  try {
    if (props.user) {
      props.user.nickname = nickname.value
      originalNickname.value = nickname.value
    }

    if (reloadData) {
      await reloadData()
    }

    if (setError) {
      setError(false)
    }

    console.log('✅ Đã cập nhật nickname:', nickname.value)
  } catch (e: any) {
    const errorMessage = e?.message || 'Cập nhật thất bại'
    if (setError) {
      setError(true, errorMessage, e?.details || '')
    }
    console.error('❌ Update nickname error:', errorMessage)
  }
}

function handleCancel() {
  nickname.value = originalNickname.value
}
</script>
