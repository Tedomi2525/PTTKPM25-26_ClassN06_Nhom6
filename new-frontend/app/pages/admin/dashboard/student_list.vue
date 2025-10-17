<template>
    <div class="mx-auto mt-8">
    <LoadingSpinner 
      v-if="isLoading"
      message="Đang tải danh sách sinh viên..."
      sub-message="Vui lòng đợi trong giây lát"
    />
    
    <DataTable
      v-else
      title="Danh Sách Sinh Viên"
      :data="students"
      :columns="columns"
      idKey="studentId"
      :showAddButton="true"
      addButtonTo="/Admin/dashboard/student_add"
      addLabel="Thêm sinh viên"
      isAdmin="True"
      @edit="editStudent"
      @delete="deleteStudent"
    />

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import DataTable from '@/components/DataTable.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const router = useRouter() // Thêm useRouter để sử dụng navigateTo
const students = ref([])
const isLoading = ref(true)

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
  isLoading.value = true
  try {
    const res = await fetch('http://localhost:8000/api/students')
    if (!res.ok) throw new Error('Không tải được danh sách')
    students.value = await res.json()
  } catch (err) {
    alert('Lỗi: ' + err.message)
  } finally {
    isLoading.value = false
  }
}

function editStudent(student) {
  localStorage.setItem('editStudentId', student.studentId)
  router.push('/Admin/dashboard/student_edit')
}

async function deleteStudent(student) {
  if (!student || !student.studentId) {
    alert('Không tìm thấy ID sinh viên để xóa.')
    return
  }
  
  if (!confirm(`Xác nhận xóa sinh viên ${student.firstName} ${student.lastName}?`)) return
  
  try {
    const res = await fetch(`http://localhost:8000/api/students/${student.studentId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    if (!res.ok) {
      const errorData = await res.json().catch(() => ({ detail: 'Unknown error' }))
      throw new Error(errorData.detail || `HTTP ${res.status}: ${res.statusText}`)
    }
    
    if (res.status !== 204) {
      await res.json()
    }

    alert('Xóa sinh viên thành công!')
    await fetchStudents()
  } catch (err) {
    alert('Lỗi khi xóa sinh viên: ' + err.message)
  }
}


onMounted(fetchStudents)

definePageMeta({
  layout: 'dashboard'
})
</script>