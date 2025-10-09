<template>
  <div class="max-w-6xl mx-auto mt-8 px-4">
    <!-- Data Table with integrated Add button -->
    <DataTable
      title="Danh Sách Giảng Viên"
      :data="teachers"
      :columns="columns"
      idKey="teacherId"
      :showAddButton="true"
      addButtonTo="/Admin/dashboard/teacher_add"
      addLabel="Thêm giảng viên"
      @edit="editTeacher"
      @delete="deleteTeacher"
    />
  </div>
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
  try {
    const res = await fetch('http://localhost:8000/api/teachers')
    if (!res.ok) throw new Error('Không tải được danh sách')
    teachers.value = await res.json()
  } catch (err) {
    alert('Lỗi: ' + err.message)
  }
}

function editTeacher(teacher) {
  alert('Sửa giảng viên: ' + teacher.firstName + ' (' + teacher.teacherId + ')')
  // hoặc điều hướng tới trang sửa:
  // router.push(`/Admin/dashboard/teacher_edit/${teacher.teacherId}`)
}

async function deleteTeacher(teacher) {
  if (!confirm(`Xác nhận xóa giảng viên ${teacher.firstName}?`)) return
  try {
    const res = await fetch(`http://localhost:8000/api/teachers/${teacher.teacherId}`, {
      method: 'DELETE'
    })
    if (!res.ok) throw new Error('Không xóa được')
    await fetchTeachers()
  } catch (err) {
    alert('Lỗi: ' + err.message)
  }
}

onMounted(fetchTeachers)

definePageMeta({
  layout: 'dashboard'
})
</script>
