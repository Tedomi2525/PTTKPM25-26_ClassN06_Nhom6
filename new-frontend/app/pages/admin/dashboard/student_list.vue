<template>
  <div class="p-6 space-y-6">
    <!-- Data Table with integrated Add button -->
    <DataTable
      title="Danh Sách Sinh Viên"
      :data="students"
      :columns="columns"
      idKey="studentId"
      :showAddButton="true"
      addButtonTo="/Admin/dashboard/student_add"
      addLabel="Thêm sinh viên"
      @edit="editStudent"
      @delete="deleteStudent"
    />

  </div>
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

function editStudent(student) {
  alert('Sửa sinh viên: ' + student.firstName + ' (' + student.studentId + ')')
  // hoặc điều hướng tới trang sửa:
  // router.push(`/Admin/dashboard/student_edit/${student.studentId}`)
}

async function deleteStudent(student) {
  if (!confirm(`Xác nhận xóa sinh viên ${student.firstName}?`)) return
  try {
    const res = await fetch(`http://localhost:8000/api/students/${student.studentId}`, {
      method: 'DELETE'
    })
    if (!res.ok) throw new Error('Không xóa được')
    await fetchStudents()
  } catch (err) {
    alert('Lỗi: ' + err.message)
  }
}


onMounted(fetchStudents)

definePageMeta({
  layout: 'dashboard'
})
</script>
