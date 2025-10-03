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
      :has-actions="true"
    >
      <template #row-actions="{ row }">
        <button @click="editCourse(row.courseId)" class="bg-yellow-400 px-2 py-1 rounded mr-1">Sửa</button>
        <button @click="hideCourse(row.courseId)" class="bg-red-500 text-white px-2 py-1 rounded">Ẩn</button>
      </template>
    </DataTable>
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
  const res = await fetch("http://localhost:8000/api/courses")
  courses.value = await res.json()
}

async function hideCourse(id) {
  if (!confirm("Ẩn học phần này?")) return
  await fetch(`http://localhost:8000/api/course/${id}/hide`, { method: "PUT" })
  fetchCourses()
}

function editCourse(id) {
  alert("Sửa học phần ID: " + id)
}

onMounted(fetchCourses)
</script>
