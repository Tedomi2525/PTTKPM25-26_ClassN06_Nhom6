<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <button 
        @click="$router.push('/Admin/courses_deleted')" 
        class="bg-gray-500 text-white px-3 py-2 rounded"
      >
        Xem học phần đã ẩn
      </button>
    </div>

    <DataTable
      title="Danh Sách Học Phần"
      :data="courses"
      :columns="columns"
      idKey="courseId"
      deleteLabel="Ẩn"
      @edit="editCourse"
      @delete="hideCourse"
    />
  </div>
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

async function fetchCourses() {
  try {
    const res = await fetch("http://localhost:8000/api/courses")
    if (!res.ok) throw new Error('Không tải được danh sách')
    courses.value = await res.json()
  } catch (err) {
    alert('Lỗi: ' + err.message)
  }
}

function editCourse(course) {
  alert('Sửa học phần: ' + course.name + ' (' + course.courseId + ')')
  // hoặc điều hướng tới trang sửa:
  // router.push(`/Admin/dashboard/course_edit/${course.courseId}`)
}

async function hideCourse(course) {
  if (!confirm(`Ẩn học phần ${course.name}?`)) return
  try {
    const res = await fetch(`http://localhost:8000/api/course/${course.courseId}/hide`, { 
      method: "PUT" 
    })
    if (!res.ok) throw new Error('Không ẩn được')
    await fetchCourses()
  } catch (err) {
    alert('Lỗi: ' + err.message)
  }
}

onMounted(fetchCourses)

definePageMeta({
  layout: 'dashboard'
})
</script>
