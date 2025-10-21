<template>
  <div v-if="show" class="fixed inset-0 bg-black/40 backdrop-blur-sm flex justify-center items-center z-50"
    @click.self="close">
    <div class="bg-white w-[850px] max-h-[85vh] rounded-xl shadow-xl relative overflow-y-auto p-6">
      <!-- Close -->
      <button class="absolute top-3 right-3 text-gray-500 hover:text-gray-700 text-xl" @click="close">✕</button>

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

      <!-- Nút điểm danh tất cả -->
      <div class="flex justify-end mt-4 gap-3 pb-2">
        <button @click="saveAttendance" class="text-sm px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg">
          Điểm danh
        </button>

        <button @click="saveAttendanceWithFace" class="text-sm px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg">
          Quét mặt
        </button>
      </div>

      <!-- Loading -->
      <LoadingSpinner v-if="loading" size="small" message="Đang tải danh sách sinh viên..." />

      <!-- Table -->
      <div v-else-if="students.length" class="border border-gray-200 rounded-lg overflow-hidden">
        <div class="max-h-[60vh] overflow-y-auto">
          <table class="w-full border-collapse">
            <thead class="bg-gray-200 sticky top-0 z-10">
              <tr>
                <th class="px-4 py-2 border text-sm font-semibold text-gray-700">STT</th>
                <th class="px-4 py-2 border text-sm font-semibold text-gray-700">Mã SV</th>
                <th class="px-4 py-2 border text-sm font-semibold text-gray-700">Họ Tên</th>
                <th class="px-4 py-2 border text-sm font-semibold text-center text-gray-700">Có mặt</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(st, index) in students" :key="st.studentCode" class="hover:bg-blue-50 transition-colors">
                <td class="px-4 py-2 border text-sm">{{ index + 1 }}</td>
                <td class="px-4 py-2 border text-sm">{{ st.studentCode }}</td>
                <td class="px-4 py-2 border text-sm">{{ st.fullName }}</td>
                <td class="px-4 py-2 border text-center">
                  <input type="checkbox" v-model="st.present" class="w-4 h-4 accent-blue-600 cursor-pointer" />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
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

      title: string
      extendedProps?: {
        room?: string
        scheduleId?: number | string

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

/* ✅ Load danh sách sinh viên có kèm trạng thái điểm danh */
async function loadStudents() {
  const scheduleId = props.schedule?.extendedProps?.scheduleId
  if (!scheduleId) return

  loading.value = true
  try {
    const res = await fetch(
      `http://localhost:8000/api/attendances/status-by-schedule?schedule_id=${scheduleId}`
    )
    const data = await res.json()
    students.value = data.attendance_list.map((item: any) => ({
      studentId: item.student_id,
      studentCode: item.student_code,
      fullName: item.full_name,
      present: item.status === 'present'
    }))
    console.log('Loaded students with attendance status:', students.value)
  } finally {
    loading.value = false
  }
}

/* ✅ Gửi điểm danh về backend */
async function saveAttendance() {
  const scheduleId = props.schedule?.extendedProps?.scheduleId
  if (!scheduleId) {
    alert("❌ Không tìm thấy schedule_id!")
    return
  }

  try {
    for (const st of students.value) {
      const status = st.present ? 'present' : 'absent'
      console.log(`Marking student ${st.studentId} or ${st.student_id} as ${status}`)

      await fetch(
        `http://localhost:8000/api/attendances/mark?schedule_id=${scheduleId}&student_id=${st.studentId}&status=${status}`,
        {
          method: 'POST',
        }
      )
    }

    alert("✅ Lưu điểm danh thành công!")
  } catch (error) {
    console.error(error)
    alert("❌ Lỗi khi lưu điểm danh!")
  }
}

async function saveAttendanceWithFace() {
  
}

watch(() => props.show, (val) => {
  if (val) loadStudents()
})

onMounted(() => {
  console.log('TeacherPopup mounted with schedule:', props.schedule)
})
</script>
