<template>
  <div class="mx-auto mt-4">
    <div class="px-6 pb-2">
    <CButton type="back" variant="secondary" @click="$router.goto()">Trở lại</CButton>
  </div>
    <DataTable
      title="Danh Sách Học Phần Đã Ẩn"
      :data="deletedCourses"
      :columns="columns"
      idKey="courseId"
      editLabel="Phục hồi"
      :hideDeleteButton="true"
      @edit="restoreCourse"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import DataTable from "@/components/DataTable.vue"

const deletedCourses = ref([])

const columns = [
  { label: "Mã học phần", field: "courseCode" },
  { label: "Tên học phần", field: "name" },
  { label: "Số tín chỉ", field: "credits" }
]

async function fetchDeletedCourses() {
  try {
    const res = await fetch("http://localhost:8000/api/courses/deleted")
    if (!res.ok) throw new Error('Không tải được danh sách')
    deletedCourses.value = await res.json()
  } catch (err) {
    alert('Lỗi: ' + err.message)
  }
}

async function restoreCourse(course) {
  if (!confirm(`Phục hồi học phần ${course.name}?`)) return
  try {
    const res = await fetch(`http://localhost:8000/api/course/${course.courseId}/restore`, { 
      method: "PUT" 
    })
    if (!res.ok) throw new Error('Không phục hồi được')
    await fetchDeletedCourses()
  } catch (err) {
    alert('Lỗi: ' + err.message)
  }
}

onMounted(fetchDeletedCourses)

definePageMeta({
  layout: 'dashboard'
})
</script>
