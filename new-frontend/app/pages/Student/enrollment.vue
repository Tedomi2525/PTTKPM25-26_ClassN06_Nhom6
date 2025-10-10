<template>
  <div class="p-6 space-y-6">
    <!-- Bảng danh sách lớp học phần -->
    <DataTable
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
import { ref, onMounted } from 'vue'
import DataTable from '@/components/DataTable.vue'

const courseClasses = ref([])

const { schoolId } = useAuth()
console.log("schoolId in enrollment.vue:", schoolId.value);
// 🧩 Cấu hình cột hiển thị trong bảng
const columns = [
  { label: "Môn học", field: "courseName" },
  { label: "Giảng viên", field: "teacherName" },
  { label: "Sĩ số tối đa", field: "maxStudents" },
  { label: "Sĩ số tối thiểu", field: "minStudents" },
  { label: "Lớp", field: "section" }
]

// 🧩 Lấy danh sách lớp học phần từ API
async function fetchCourseClasses() {
  try {
    const res = await fetch('http://localhost:8000/api/course_classes')
    if (!res.ok) throw new Error('Không tải được danh sách học phần')
    const data = await res.json()

    // Làm phẳng dữ liệu để dễ hiển thị trong bảng
    courseClasses.value = data.map(item => ({
      ...item,
      courseName: item.course?.name || 'Không có tên môn học',
      teacherName: item.teacher
        ? `${item.teacher.lastName} ${item.teacher.firstName}`
        : 'Không rõ giảng viên'
    }))
  } catch (err) {
    alert('Lỗi: ' + err.message)
  }
}

// 🧩 Hàm đăng ký học phần
async function enroll(row) {
  try {
    const studentId = schoolId.value; // 👈 lấy ID sinh viên
    if (!studentId) {
      alert("⚠️ Không tìm thấy mã sinh viên. Vui lòng đăng nhập lại!");
      return;
    }

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

onMounted(fetchCourseClasses) 

// 🧩 Tiêu đề trang
definePageMeta({
  title: 'Đăng ký học phần'
})
</script>
