<template>
  <div class="max-w-6xl mx-auto mt-4">
    <div class="px-6 pb-2">
      <CButton type="goto" to="/Admin/dashboard/programs_deleted" variant="secondary">Bảng chương trình đã ẩn</CButton>
    </div>

    <LoadingSpinner 
      v-if="isLoading"
      message="Đang tải danh sách chương trình đào tạo..."
      sub-message="Vui lòng đợi trong giây lát"
    />
    
    <DataTable
      v-else
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
import LoadingSpinner from "@/components/LoadingSpinner.vue"

const programs = ref([])
const isLoading = ref(true)

const columns = [
  { label: "Tên chương trình", field: "programName" },
  { label: "Năm bắt đầu", field: "startYear" },
  { label: "Thời gian (năm)", field: "duration" },
  { label: "Học kỳ hiện tại", field: "currentSemester" }
]

async function fetchPrograms() {
  isLoading.value = true
  try {
    const res = await fetch("http://localhost:8000/api/programs")
    if (!res.ok) throw new Error('Không tải được danh sách chương trình')
    programs.value = await res.json()
  } catch (err) {
    alert('Lỗi: ' + err.message)
  } finally {
    isLoading.value = false
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
