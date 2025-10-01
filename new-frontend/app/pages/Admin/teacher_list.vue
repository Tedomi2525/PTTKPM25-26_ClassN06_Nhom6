<template>
  <DataTable
    title="Danh Sách Giảng Viên"
    :data="teachers"
    :columns="columns"
    idKey="teacherId"
    :has-actions="true"
  >
    <template #row-actions="{ row }">
      <button @click="editTeacher(row.teacherId)" class="bg-yellow-400 px-2 py-1 rounded mr-1">Sửa</button>
      <button @click="deleteTeacher(row.teacherId)" class="bg-red-500 text-white px-2 py-1 rounded">Xóa</button>
    </template>
  </DataTable>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DataTable from '@/components/DataTable.vue'

const teachers = ref([])
const columns = [
  { label: "Mã GV", field: "teacherCode" },
  { label: "Họ và đệm", field: "lastName" },
  { label: "Tên", field: "firstName" },
  { label: "Ngày sinh", field: "dob" },
  { label: "Giới tính", field: "gender" },
  { label: "Email", field: "email" },
  { label: "SĐT", field: "phone" },
  { label: "Khoa", field: "faculty" },
  { label: "Bộ môn", field: "department" },
  { label: "Chuyên ngành", field: "specialization" },
  { label: "Học vị", field: "degree" },
  { label: "Học hàm", field: "academicRank" }
]

async function fetchTeachers() {
  const res = await fetch('http://localhost:8000/api/teachers')
  teachers.value = await res.json()
}

async function deleteTeacher(id) {
  if (!confirm('Xác nhận xóa?')) return
  await fetch(`http://localhost:8000/api/teachers/${id}`, { method: 'DELETE' })
  fetchTeachers()
}

function editTeacher(id) {
  alert('Sửa giảng viên ID: ' + id)
}

onMounted(fetchTeachers)
</script>
