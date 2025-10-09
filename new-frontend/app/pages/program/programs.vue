<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <button 
        @click="$router.push('/admin/dashboard/programs_deleted')" 
        class="bg-gray-500 text-white px-3 py-2 rounded"
      >
        Xem chương trình đã ẩn
      </button>
    </div>

    <DataTable
      title="Danh Sách Chương Trình Đào Tạo"
      :data="programs"
      :columns="columns"
      idKey="program_id"
      deleteLabel="Ẩn"
      @edit="editProgram"
      @delete="hideProgram"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import DataTable from "@/components/DataTable.vue"

const programs = ref([])

const columns = [
  { label: "Tên chương trình", field: "programName" },
  { label: "Năm bắt đầu", field: "startYear" },
  { label: "Thời gian (năm)", field: "duration" },
  { label: "Học kỳ hiện tại", field: "currentSemester" }
]

async function fetchPrograms() {
  try {
    const res = await fetch("http://localhost:8000/api/programs")
    if (!res.ok) throw new Error('Không tải được danh sách chương trình')
    programs.value = await res.json()
  } catch (err) {
    alert('Lỗi: ' + err.message)
  }
}

function editProgram(program) {
  alert('Sửa chương trình: ' + program.program_name + ' (' + program.program_id + ')')
  // hoặc điều hướng tới trang sửa:
  // router.push(`/admin/dashboard/program_edit/${program.program_id}`)
}

async function hideProgram(program) {
  if (!confirm(`Ẩn chương trình ${program.program_name}?`)) return
  try {
    const res = await fetch(`http://localhost:8000/api/program/${program.program_id}/hide`, { 
      method: "PUT" 
    })
    if (!res.ok) throw new Error('Không ẩn được chương trình')
    await fetchPrograms()
  } catch (err) {
    alert('Lỗi: ' + err.message)
  }
}

onMounted(fetchPrograms)

definePageMeta({
  layout: 'dashboard'
})
</script>
