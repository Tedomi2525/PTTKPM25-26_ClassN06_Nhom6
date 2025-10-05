<template>
    <div class="p-6">
      <CButton to="/Admin/dashboard/student_add">
        Thêm sinh viên
      </CButton>
    </div>

  <DataTable
    title="Danh Sách Sinh Viên"
    :data="students"
    :columns="columns"
    idKey="studentId"
    :has-actions="true"
  >
    <template #title-right>
    <RouterLink
      to="/Admin/student_add"
      class="bg-green-500 text-white px-3 py-2 rounded hover:bg-green-600"
    >
      Thêm sinh viên
    </RouterLink>
    </template>

    <!-- Tùy biến cột Hành động -->
    <template #row-actions="{ row }">
      <button @click="editStudent(row.studentId)" class="bg-yellow-400 px-2 py-1 rounded mr-1 cursor-pointer">Sửa</button>
      <button @click="deleteStudent(row.studentId)" class="bg-red-500 text-white px-2 py-1 rounded cursor-pointer">Xóa</button>
    </template>
  </DataTable>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DataTable from '@/components/DataTable.vue'

const students = ref([])

const columns = [
  { label: "Mã SV", field: "studentCode" },
  { label: "Họ và đệm", field: "lastName" },
  { label: "Tên", field: "firstName" },
  { label: "Ngày sinh", field: "dob" },
  { label: "Giới tính", field: "gender" },
  { label: "Email", field: "email" },
  { label: "SĐT", field: "phone" },
  { label: "Lớp", field: "className" },
  { label: "Trạng thái", field: "status" }
]

async function fetchStudents() {
  try {
    const res = await fetch('http://localhost:8000/api/students')
    if (!res.ok) throw new Error('Không tải được danh sách')
    students.value = await res.json()
  } catch (err) {
    alert('Lỗi: ' + err.message)
  }
}

async function deleteStudent(id) {
  if (!confirm('Xác nhận xóa?')) return
  try {
    const res = await fetch(`http://localhost:8000/api/students/${id}`, { method: 'DELETE' })
    if (!res.ok) throw new Error('Không xóa được')
    fetchStudents()
  } catch (err) {
    alert('Lỗi: ' + err.message)
  }
}

function editStudent(id) {
  alert('Sửa sinh viên ID: ' + id)
}

onMounted(fetchStudents)

definePageMeta({
  layout: 'dashboard'
})
</script>
