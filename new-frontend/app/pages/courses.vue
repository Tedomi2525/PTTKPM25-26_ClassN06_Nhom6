<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <button 
        @click="navigateTo('/Admin/courses_deleted')" 
        class="bg-gray-500 text-white px-3 py-2 rounded hover:bg-gray-600 transition"
      >
        Xem học phần đã ẩn
      </button>
    </div>

    <DataTable
      v-if="!loading"
      title="Danh Sách Học Phần"
      :data="courses"
      :columns="columns"
      idKey="courseId"
      deleteLabel="Ẩn"
      @edit="editCourse"
      @delete="hideCourse"
    />

    <div v-else class="text-center text-gray-500">Đang tải danh sách học phần...</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import DataTable from "@/components/DataTable.vue"

const courses = ref([])
const loading = ref(true)

const columns = [
  { label: "Mã học phần", field: "courseCode" },
  { label: "Tên học phần", field: "name" },
  { label: "Số tín chỉ", field: "credits" }
]

// ✅ Dùng $fetch (tự động parse JSON, xử lý lỗi tốt hơn)
async function fetchCourses() {
  loading.value = true
  try {
    courses.value = await $fetch("http://localhost:8000/api/courses")
  } catch (err) {
    console.error(err)
    alert("Không tải được danh sách học phần.")
  } finally {
    loading.value = false
  }
}

function editCourse(course) {
  navigateTo(`/Admin/dashboard/course_edit/${course.courseId}`)
}

async function hideCourse(course) {
  if (!confirm(`Ẩn học phần "${course.name}"?`)) return
  try {
    await $fetch(`http://localhost:8000/api/course/${course.courseId}/hide`, { method: "PUT" })
    await fetchCourses()
  } catch (err) {
    console.error(err)
    alert("Không thể ẩn học phần.")
  }
}

onMounted(fetchCourses)
</script>
