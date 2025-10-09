<template>
  <div class="p-6 space-y-6">

    <!-- Bảng danh sách lớp học phần -->
    <DataTable
      title="Danh Sách Lớp Học Phần"
      :data="courseClasses"
      :columns="columns"
      idKey="courseClassId"
      :showAddButton="false"
    >
      <!-- Custom action slot -->
      <template #actions="{ row }">
        <button
          class="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded"
          @click="enroll(row)"
        >
          Đăng ký
        </button>
      </template>
    </DataTable>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DataTable from '@/components/DataTable.vue'

const courseClasses = ref([])

// 🔹 Cột hiển thị
const columns = [
  { label: "Mã Lớp", field: "courseId" },
  { label: "Môn học", field: "" },
  { label: "Giảng viên", field: "teacher_name" },
  { label: "Học kỳ", field: "semester_name" },
  { label: "Sĩ số tối đa", field: "maxStudents" },
  { label: "Sĩ số tối thiểu", field: "minStudents" },
  { label: "Lớp", field: "section" },
  { label: "Hành động", field: "actions" } 
]

// 🔹 Fetch danh sách lớp học phần
async function fetchCourseClasses() {
  try {
    const res = await fetch('http://localhost:8000/api/course_classes')
    if (!res.ok) throw new Error('Không tải được danh sách học phần')
    const data = await res.json()
    courseClasses.value = data
  } catch (err) {
    alert('Lỗi: ' + err.message)
  }
}

// 🔹 Hàm đăng ký học phần

onMounted(fetchCourseClasses)

definePageMeta({ 
    title: 'Đăng ký học phần'
})
</script>
