<template>
  <div class="p-6 space-y-6">
    <!-- Loading state -->
    <LoadingSpinner 
      v-if="isLoading" 
      message="Đang tải danh sách học phần..."
      sub-message="Vui lòng đợi trong giây lát"
    />

    <!-- Error state -->
    <div v-else-if="errorMessage" class="flex justify-center items-center min-h-[400px]">
      <div class="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md">
        <div class="flex items-center mb-3">
          <svg class="w-6 h-6 text-red-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <h3 class="text-lg font-semibold text-red-800">Lỗi tải dữ liệu</h3>
        </div>
        <p class="text-red-700 mb-4">{{ errorMessage }}</p>
        <button 
          @click="fetchCourseClasses" 
          class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition"
        >
          Thử lại
        </button>
      </div>
    </div>

    <!-- Bảng danh sách lớp học phần -->
    <DataTable
      v-else
      title="Danh Sách Lớp Học Phần"
      :data="courseClasses"
      :columns="columns"
      idKey="courseClassId"
      :showAddButton="false"
      :registerMode="true"
      :showRegisterButton="true"
      registerLabel="Đăng ký"
      @register="enroll"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import DataTable from '@/components/DataTable.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import { useAuth } from '@/composables/useAuth'

const { schoolId, programId, user, initAuth, isChecking } = useAuth()

const courseClasses = ref([])
const isLoading = ref(true)
const errorMessage = ref('')

const columns = [
  { label: "Môn học", field: "courseName" },
  { label: "Giảng viên", field: "teacherName" },
  { label: "Sĩ số hiện tại", field: "currentStudents" },
  { label: "Sĩ số tối đa", field: "maxStudents" },
  { label: "Sĩ số tối thiểu", field: "minStudents" },
  { label: "Lớp", field: "section" }
]

// 🧩 Lấy danh sách lớp học phần
async function fetchCourseClasses() {
  const currentProgramId = programId.value || user.value?.programId
  const currentSchoolId = schoolId.value || localStorage.getItem('schoolId')
  
  // Kiểm tra dữ liệu cần thiết
  if (!currentProgramId) {
    console.error('❌ Program ID không có')
    errorMessage.value = 'Không tìm thấy thông tin chương trình học. Vui lòng đăng nhập lại.'
    isLoading.value = false
    return
  }
  
  if (!currentSchoolId) {
    console.error('❌ Student ID không có')
    errorMessage.value = 'Không tìm thấy mã sinh viên. Vui lòng đăng nhập lại.'
    isLoading.value = false
    return
  }

  console.log(`📚 Đang tải lớp học phần cho program ${currentProgramId}, student ${currentSchoolId}`)
  
  try {
    isLoading.value = true
    errorMessage.value = ''
    
    const res = await fetch(`http://localhost:8000/api/by_program/${currentProgramId}?student_id=${currentSchoolId}`)
    
    if (!res.ok) {
      throw new Error('Không tải được danh sách học phần')
    }
    
    const data = await res.json()

    courseClasses.value = data.map(item => ({
      ...item,
      courseName: item.course?.name || 'Không có tên môn học',
      teacherName: item.teacher
        ? `${item.teacher.lastName} ${item.teacher.firstName}`
        : 'Không rõ giảng viên'
    }))
    
    console.log(`✅ Đã tải ${courseClasses.value.length} lớp học phần`)
  } catch (err) {
    console.error('🚨 Lỗi khi tải học phần:', err)
    errorMessage.value = err.message
  } finally {
    isLoading.value = false
  }
}

// 🧩 Hàm đăng ký học phần
async function enroll(row) {
  const studentId = schoolId.value || localStorage.getItem('schoolId')
  if (!studentId) {
    alert("⚠️ Không tìm thấy mã sinh viên. Vui lòng đăng nhập lại!");
    return;
  }

  try {
    const response = await fetch('http://127.0.0.1:8000/api/enrollments', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        studentId: Number(studentId),
        courseClassId: row.courseClassId
      })
    });

    const result = await response.json();

    if (!response.ok) {
      console.error('Lỗi đăng ký:', result);
      alert(`⚠️ Đăng ký thất bại!\nChi tiết: ${result.detail?.[0]?.msg || 'Không rõ lỗi'}`);
      return;
    }

    alert(`✅ Đăng ký thành công!\nMã đăng ký: ${result.enrollmentId}`);
  } catch (error) {
    console.error('Chi tiết lỗi:', error);
    alert('❌ Lỗi kết nối đến server: ' + error.message);
  }
}

// Watch programId và schoolId để tự động load khi có dữ liệu
watch([programId, schoolId], ([newProgramId, newSchoolId]) => {
  if (newProgramId && newSchoolId && !isChecking.value) {
    console.log('✅ Auth data sẵn sàng, đang load học phần...')
    fetchCourseClasses()
  }
}, { immediate: true })

onMounted(async () => {
  // Đảm bảo auth đã được khởi tạo
  if (!programId.value || !schoolId.value) {
    console.log('🔄 Đang khởi tạo auth...')
    await initAuth()
  }
  
  // Nếu đã có đủ dữ liệu, load ngay
  if (programId.value && schoolId.value) {
    await fetchCourseClasses()
  }
})

definePageMeta({
  title: 'Đăng ký học phần'
})
</script>
