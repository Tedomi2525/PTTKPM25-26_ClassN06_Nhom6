<template>
  <div class="p-6 flex flex-col items-center w-full font-semibold max-w-5xl mx-auto">
    <!-- Grid layout -->
    <div class="grid grid-cols-3 gap-4 w-full">
      <div class="flex flex-col gap-1 bg-gray-50 border border-gray-200 p-3 rounded-lg hover:border-gray-300 hover:shadow-sm transition-all duration-200">
        <p class="text-gray-700 font-semibold text-sm m-0">Mã sinh viên</p>
        <input
          type="text"
          :value="props.student?.studentCode"
          class="bg-gray-100 border border-gray-300 p-2 rounded-lg text-gray-600 cursor-not-allowed text-sm font-medium"
          readonly
        />
      </div>
      <!-- Lớp -->
      <div class="flex flex-col gap-1 bg-gray-50 border border-gray-200 p-3 rounded-lg hover:border-gray-300 hover:shadow-sm transition-all duration-200">
        <p class="text-gray-700 font-semibold text-sm m-0">Lớp học</p>
        <input
          type="text"
          :value="props.student?.className"
          class="bg-gray-100 border border-gray-300 p-2 rounded-lg text-gray-600 cursor-not-allowed text-sm font-medium"
          readonly
        />
      </div>

      <!-- Trường -->
      <div class="flex flex-col gap-1 bg-gray-50 border border-gray-200 p-3 rounded-lg hover:border-gray-300 hover:shadow-sm transition-all duration-200">
        <p class="text-gray-700 font-semibold text-sm m-0">Ngành học</p>
        <input
          type="text"
          :value="props.student?.major"
          class="bg-gray-100 border border-gray-300 p-2 rounded-lg text-gray-600 cursor-not-allowed text-sm font-medium"
          readonly
        />
      </div>
      <div class="flex flex-col gap-1 bg-gray-50 border border-gray-200 p-3 rounded-lg hover:border-gray-300 hover:shadow-sm transition-all duration-200">
        <p class="text-gray-700 font-semibold text-sm m-0">Khoa</p>
        <input
          type="text"
          :value="props.student?.faculty"
          class="bg-gray-100 border border-gray-300 p-2 rounded-lg text-gray-600 cursor-not-allowed text-sm font-medium"
          readonly
        />
      </div>
      <div class="flex flex-col gap-1 bg-gray-50 border border-gray-200 p-3 rounded-lg hover:border-gray-300 hover:shadow-sm transition-all duration-200 col-span-2">
        <p class="text-gray-700 font-semibold text-sm m-0">Chương trình đào tạo</p>
        <input
          type="text"
          :value="props.student?.trainingProgram"
          class="bg-gray-100 border border-gray-300 p-2 rounded-lg text-gray-600 cursor-not-allowed text-sm font-medium"
          readonly
        />
      </div>
      <!-- Chức vụ -->
      <div class="flex flex-col gap-1 bg-gray-50 border border-gray-200 p-3 rounded-lg hover:border-gray-300 hover:shadow-sm transition-all duration-200">
        <p class="text-gray-700 font-semibold text-sm m-0">Chức vụ lớp</p>
        <input
          type="text"
          :value="props.student?.position"
          class="bg-gray-100 border border-gray-300 p-2 rounded-lg text-gray-600 cursor-not-allowed text-sm font-medium"
          readonly
        />
      </div>

      <!-- Trạng thái -->
      <div class="flex flex-col gap-1 bg-gray-50 border border-gray-200 p-3 rounded-lg hover:border-gray-300 hover:shadow-sm transition-all duration-200">
        <p class="text-gray-700 font-semibold text-sm m-0">Trạng thái</p>
        <input
          type="text"
          :value="props.student?.status ? 'Đang học' : 'Tạm nghỉ'"
          class="bg-gray-100 border border-gray-300 p-2 rounded-lg text-gray-600 cursor-not-allowed text-sm font-medium"
          readonly
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { inject } from 'vue'

const props = defineProps<{ 
  user: any, 
  student: any
}>()

const reloadData = inject('reloadUserData') as () => Promise<void>
const setError = inject('setError') as (
  show: boolean,
  message?: string,
  details?: string
) => void
</script>
