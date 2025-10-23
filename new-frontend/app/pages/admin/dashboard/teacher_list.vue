<template>
  <div class="mx-auto mt-8">
    <LoadingSpinner 
      v-if="isLoading"
      message="Đang tải danh sách giảng viên..."
      sub-message="Vui lòng đợi trong giây lát"
    />
    
    <!-- Data Table with integrated Add button -->
    <DataTable
      v-else
      title="Danh Sách Giảng Viên"
      :data="teachers"
      :columns="columns"
      idKey="teacherId"
      :showAddButton="true"
      addButtonTo="/Admin/dashboard/teacher_add"
      isAdmin="True"
      addLabel="Thêm giảng viên"
      @edit="editTeacher"
      @delete="deleteTeacher"
      max-height="80vh"
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

const teachers = ref([])
const isLoading = ref(true)
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
  isLoading.value = true
  try {
    const res = await fetch('http://localhost:8000/api/teachers')
    if (!res.ok) throw new Error('Không tải được danh sách')
    teachers.value = await res.json()
  } catch (err) {
    alert('Lỗi: ' + err.message)
  } finally {
    isLoading.value = false
  }
}

function editTeacher(teacher) {
  localStorage.setItem('editTeacherId', teacher.teacherId)
  router.push('/Admin/dashboard/teacher_edit')
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
