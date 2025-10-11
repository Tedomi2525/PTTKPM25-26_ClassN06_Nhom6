<template>
  <div class="p-6 flex flex-col items-center w-full font-semibold max-w-5xl mx-auto">
    <!-- Form -->
    <div class="w-full">
      <div class="grid grid-cols-4 gap-4 mb-4">
        <!-- Họ và tên -->
        <div class="col-span-2 flex flex-col gap-1 bg-gray-50 border border-gray-200 p-3 rounded-lg hover:border-gray-300 hover:shadow-sm transition-all duration-200">
          <p class="text-gray-700 font-semibold text-sm m-0">Họ và tên</p>
          <input
            type="text"
            :value="props.student?.full_name || props.user?.fullName"
            class="bg-gray-100 border border-gray-300 p-2 rounded-lg text-gray-600 cursor-not-allowed text-sm font-medium"
            readonly
          />
        </div>

        <!-- Ngày sinh -->
        <div class="col-span-1 flex flex-col gap-1 bg-gray-50 border border-gray-200 p-3 rounded-lg hover:border-gray-300 hover:shadow-sm transition-all duration-200">
          <p class="text-gray-700 font-semibold text-sm m-0">Ngày sinh</p>
          <input
            type="text"
            :value="formatDate(props.student?.dob)"
            class="bg-white border border-gray-300 p-2 rounded-lg focus:border-blue-400 focus:ring-2 focus:ring-blue-100 transition-all duration-200 text-sm font-medium focus:outline-none"
          />
        </div>

        <!-- Giới tính -->
        <div class="col-span-1 flex flex-col gap-1 bg-gray-50 border border-gray-200 p-3 rounded-lg hover:border-gray-300 hover:shadow-sm transition-all duration-200">
          <p class="text-gray-700 font-semibold text-sm m-0">Giới tính</p>
          <input
            type="text"
            :value="props.student?.gender"
            class="bg-white border border-gray-300 p-2 rounded-lg focus:border-blue-400 focus:ring-2 focus:ring-blue-100 transition-all duration-200 text-sm font-medium focus:outline-none"
          />
        </div>
        <!-- Số điện thoại -->
        <div class="col-span-2 flex flex-col gap-1 bg-gray-50 border border-gray-200 p-3 rounded-lg hover:border-gray-300 hover:shadow-sm transition-all duration-200">
          <p class="text-gray-700 font-semibold text-sm m-0">Số điện thoại</p>
          <input
            type="text"
            :value="props.student?.phone"
            class="bg-white border border-gray-300 p-2 rounded-lg focus:border-blue-400 focus:ring-2 focus:ring-blue-100 transition-all duration-200 text-sm font-medium focus:outline-none"
          />
        </div>

        <!-- Email -->
        <div class="col-span-2 flex flex-col gap-1 bg-gray-50 border border-gray-200 p-3 rounded-lg hover:border-gray-300 hover:shadow-sm transition-all duration-200">
          <p class="text-gray-700 font-semibold text-sm m-0">Email</p>
          <input
            type="text"
            :value="props.student?.email"
            class="bg-white border border-gray-300 p-2 rounded-lg focus:border-blue-400 focus:ring-2 focus:ring-blue-100 transition-all duration-200 text-sm font-medium focus:outline-none"
          />
        </div>

        <!-- Địa chỉ -->
        <div class="col-span-4 flex flex-col gap-1 bg-gray-50 border border-gray-200 p-3 rounded-lg hover:border-gray-300 hover:shadow-sm transition-all duration-200">
          <p class="text-gray-700 font-semibold text-sm m-0">Địa chỉ</p>
          <input
            type="text"
            v-model="address"
            class="bg-white border border-gray-300 p-2 rounded-lg focus:border-blue-400 focus:ring-2 focus:ring-blue-100 transition-all duration-200 text-sm font-medium focus:outline-none placeholder-gray-400"
            placeholder="Nhập địa chỉ đầy đủ"
          />
        </div>
      </div>
    </div>

    <!-- Button -->
    <div class="w-full flex justify-end">
      <CButton
        @click="handleSave"
        variant="primary"
      >
        Lưu thông tin
      </CButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, inject, watch } from 'vue'
import { useSchool } from '~/composables/useSchool'
import CButton from '@/components/CButton.vue'

const { student, isLoading, error, studentInit, updateStudent } = useSchool()


const props = defineProps<{ user: any; student: any }>()

const address = ref(props.student?.address || '')

watch(
  () => props.student?.address,
  (newAddress) => (address.value = newAddress || ''),
  { immediate: true }
)

const reloadData = inject('reloadUserData') as () => Promise<void>
const setError = inject('setError') as (
  show: boolean,
  message?: string,
  details?: string
) => void

async function handleSave() {
  try {
    if (props.student) props.student.address = address.value
    if (reloadData) await reloadData()
    console.log('✅ Lưu thông tin thành công')
  } catch (error) {
    console.error('❌ Lỗi lưu:', error)
    if (setError)
      setError(true, 'Lưu thông tin thất bại', error instanceof Error ? error.message : '')
  }
}

const formatDate = (dateStr?: string) => {
  if (!dateStr) return ''
  try {
    const d = new Date(dateStr)
    return `${String(d.getDate()).padStart(2, '0')}-${String(
      d.getMonth() + 1
    ).padStart(2, '0')}-${d.getFullYear()}`
  } catch {
    return dateStr
  }
}
</script>
