<template>
  <div class="p-6 space-y-6">
    <LoadingSpinner 
      v-if="isLoading || isChecking" 
      :message="isChecking ? 'Đang xác thực người dùng...' : 'Đang tải kết quả đăng ký...'"
      sub-message="Vui lòng đợi trong giây lát"
    />

    <div v-else-if="errorMessage" class="flex justify-center items-center min-h-[400px]">
      <div class="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md text-center">
        <h3 class="text-lg font-semibold text-red-800 mb-2">Lỗi tải dữ liệu</h3>
        <p class="text-red-700 mb-4">{{ errorMessage }}</p>
        <button 
          @click="fetchEnrollments" 
          class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition"
        >
          Thử lại
        </button>
      </div>
    </div>

    <DataTable
      v-else
      title="Kết Quả Đăng Ký Học Phần"
      :data="enrollments"
      :columns="columns"
      idKey="enrollmentId"
      :showAddButton="false"
      :hideDeleteButton="true"
    />
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import DataTable from '@/components/DataTable.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import { useAuth } from '@/composables/useAuth'

definePageMeta({
  title: 'Kết quả đăng ký học phần'
})

const { user, initAuth, isChecking } = useAuth()

const enrollments = ref([])
const isLoading = ref(true)
const errorMessage = ref('')

const columns = [
  { label: "Môn học", field: "courseName" },
  { label: "Giảng viên", field: "teacherName" },
  { label: "Lớp", field: "section" },
  { label: "Ngày đăng ký", field: "enrollmentDate" },
]

async function fetchEnrollments() {
  // Đợi auth state được khởi tạo hoàn tất trước khi fetch data
  if (isChecking.value) {
    console.log('⏳ Đang đợi khởi tạo auth state...')
    let attempts = 0
    while (isChecking.value && attempts < 50) {
      await new Promise(resolve => setTimeout(resolve, 100))
      attempts++
    }
  }

  if (!user.value?.schoolId) {
    console.error('❌ Không có thông tin sinh viên:', { user: user.value, isChecking: isChecking.value })
    errorMessage.value = 'Không tìm thấy thông tin sinh viên. Vui lòng đăng nhập lại.'
    isLoading.value = false
    return
  }

  console.log(`📚 Đang tải kết quả đăng ký cho sinh viên ${user.value.schoolId}`)
  
  try {
    isLoading.value = true
    errorMessage.value = ''
    
    const res = await fetch(`http://localhost:8000/api/enrollments?student_id=${user.value.schoolId}`)
    
    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}))
      throw new Error(errorData.detail || 'Không thể tải dữ liệu đăng ký.')
    }
    
    const data = await res.json()

    enrollments.value = data.map(item => ({
      enrollmentId: item.enrollmentId,
      courseName: item.courseClass?.course?.name || 'N/A',
      teacherName: item.courseClass?.teacher ? `${item.courseClass.teacher.lastName} ${item.courseClass.teacher.firstName}` : 'N/A',
      section: item.courseClass?.section || 'N/A',
      enrollmentDate: new Date(item.createdAt).toLocaleDateString('vi-VN'),
    }))
    
    console.log(`✅ Đã tải ${enrollments.value.length} kết quả đăng ký.`)
  } catch (err) {
    console.error('🚨 Lỗi khi tải kết quả đăng ký:', err)
    errorMessage.value = err.message
  } finally {
    isLoading.value = false
  }
}

// Khởi tạo khi component mount
onMounted(async () => {
  console.log('🔧 Component mounted - bắt đầu khởi tạo auth và fetch data')
  
  // Đảm bảo auth được khởi tạo
  if (!user.value && !isChecking.value) {
    console.log('🔄 Khởi tạo auth state...')
    await initAuth()
  }
  
  // Sau khi auth sẵn sàng, fetch enrollments
  if (user.value?.schoolId) {
    await fetchEnrollments()
  } else {
    console.warn('⚠️ Không có schoolId sau khi khởi tạo auth')
    isLoading.value = false
  }
})

// Watch cho trường hợp user change (switch account, etc.)
watch(() => user.value?.schoolId, async (newSchoolId, oldSchoolId) => {
  // Chỉ fetch lại khi có schoolId mới và khác với cũ
  if (newSchoolId && newSchoolId !== oldSchoolId && !isChecking.value) {
    console.log(`👤 SchoolId changed: ${oldSchoolId} → ${newSchoolId}`)
    await fetchEnrollments()
  }
})
</script>
