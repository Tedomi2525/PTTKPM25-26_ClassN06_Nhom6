<template>
  <div
    v-if="show"
    class="fixed inset-0 bg-black/40 backdrop-blur-sm flex justify-center items-center z-50"
    @click.self="close"
  >
    <div class="bg-white w-[850px] max-h-[85vh] rounded-xl shadow-xl relative overflow-y-auto p-6">
<!-- Close -->
      <button
        class="absolute top-3 right-3 text-gray-500 hover:text-gray-700 text-xl"
        @click="close"
      >✕</button>

      <!-- Header -->
      <h2 class="text-2xl font-bold mb-3 text-gray-800">
        Danh sách sinh viên - {{ schedule.subjectName || "Học phần" }}
      </h2>

      <div class="text-sm text-gray-500 mb-3">
        <p><strong>Môn học:</strong> {{ schedule.title || '-' }}</p>
        <p><strong>Phòng học:</strong> {{ schedule.extendedProps?.room || '-' }}</p>
      </div>

      <!-- Title -->
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold">Danh sách sinh viên</h3>
        <span v-if="!loading" class="text-sm bg-blue-100 px-3 py-1 rounded-full text-gray-600">
          Tổng: {{ students.length }} sinh viên
        </span>
      </div>

      <!-- Loading -->
      <LoadingSpinner v-if="loading" size="small" message="Đang tải danh sách sinh viên..." />

      <!-- Table -->
      <div v-else-if="students.length">
        <table class="w-full text-left border-collapse">
          <thead class="bg-gray-100 text-gray-700">
            <tr>
              <th class="px-4 py-2 border">STT</th>
              <th class="px-4 py-2 border">Mã SV</th>
              <th class="px-4 py-2 border">Họ</th>
              <th class="px-4 py-2 border">Tên</th>
              <th class="px-4 py-2 border text-center">Có mặt</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(st, index) in students"
              :key="st.studentCode"
              class="hover:bg-gray-50"
            >
              <td class="px-4 py-2 border">{{ index + 1 }}</td>
              <td class="px-4 py-2 border">{{ st.studentCode }}</td>
              <td class="px-4 py-2 border">{{ st.lastName }}</td>
              <td class="px-4 py-2 border">{{ st.firstName }}</td>
              <td class="px-4 py-2 border text-center">
                <input type="checkbox" v-model="st.present" />
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Empty -->
      <p v-else class="text-center text-gray-500 py-6">Chưa có sinh viên.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const props = defineProps({
  show: Boolean,
  schedule: {
    type: Object as () => {
      classId: number | string
      className: string
      subjectName: string
      scheduleId: number | string
      title: string
      extendedProps?: {
        room?: string
      }
    },
    required: true,
  },
})

const emit = defineEmits(['close'])
const students = ref<any[]>([])
const loading = ref(false)

function close() {
  emit('close')
}

async function loadStudents() {
  if (!props.schedule?.classId) return
  loading.value = true
  try {
    const res = await fetch(`http://localhost:8000/api/course_classes/${props.schedule.classId}/students`)
    const data = await res.json()
    students.value = data.map((item: any) => ({
      studentCode: item.student?.student_code || '-',
      firstName: item.student?.first_name || '-',
      lastName: item.student?.last_name || '-',
      present: false,
    }))
  } catch (e) {
    console.error('Lỗi tải sinh viên:', e)
  } finally {
    loading.value = false
  }
}

watch(() => props.show, (val) => {
  console.log('TeacherPopup show prop changed:', val)
  if (val) loadStudents()
})

onMounted(() => {
  console.log('TeacherPopup mounted with schedule:', props.schedule)
})
</script>
