<template>
  <DataTable
    title="Danh Sách Học Phần"
    :data="courses"
    :columns="columns"
    idKey="courseId"
    :has-actions="true"
  >
    <!-- Cột Hành động -->
    <template #row-actions="{ row }">
      <button 
        @click="editCourse(row.courseId)" 
        class="bg-yellow-400 px-2 py-1 rounded mr-1"
      >
        Sửa
      </button>
      <button 
        @click="deleteCourse(row.courseId)" 
        class="bg-red-500 text-white px-2 py-1 rounded"
      >
        Xóa
      </button>
    </template>
  </DataTable>
</template>

<script setup>
import { ref, onMounted } from "vue"
import DataTable from "@/components/DataTable.vue"

const courses = ref([])

const columns = [
  { label: "Mã học phần", field: "courseCode" },
  { label: "Tên học phần", field: "name" },
  { label: "Số tín chỉ", field: "credits" }
]

// Lấy danh sách học phần
async function fetchCourses() {
  try {
    const res = await fetch("http://localhost:8000/api/courses")
    if (!res.ok) throw new Error("Không tải được danh sách học phần")
    courses.value = await res.json()
  } catch (err) {
    alert("Lỗi: " + err.message)
  }
}

// Xóa học phần
async function deleteCourse(id) {
  if (!confirm("Xác nhận xóa học phần?")) return
  try {
    const res = await fetch(`http://localhost:8000/api/courses/${id}`, { method: "DELETE" })
    if (!res.ok) throw new Error("Không xóa được học phần")
    fetchCourses()
  } catch (err) {
    alert("Lỗi: " + err.message)
  }
}

// Sửa học phần
function editCourse(id) {
  alert("Sửa học phần ID: " + id)
}

onMounted(fetchCourses)
</script>
