<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <button 
        @click="$router.push('/Admin/courses')" 
        class="bg-blue-500 text-white px-3 py-2 rounded"
      >
        Quay lại danh sách chính
      </button>
    </div>

    <DataTable
      title="Danh Sách Học Phần Đã Ẩn"
      :data="deletedCourses"
      :columns="columns"
      idKey="courseId"
      :has-actions="true"
    >
      <template #row-actions="{ row }">
        <button 
          @click="restoreCourse(row.courseId)" 
          class="bg-green-500 text-white px-2 py-1 rounded"
        >
          Phục hồi
        </button>
      </template>
    </DataTable>
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
  const res = await fetch("http://localhost:8000/api/courses/deleted")
  deletedCourses.value = await res.json()
}

async function restoreCourse(id) {
  if (!confirm("Phục hồi học phần này?")) return
  await fetch(`http://localhost:8000/api/course/${id}/restore`, { method: "PUT" })
  fetchDeletedCourses()
}

onMounted(fetchDeletedCourses)

definePageMeta({
  layout: 'dashboard'
})
</script>
