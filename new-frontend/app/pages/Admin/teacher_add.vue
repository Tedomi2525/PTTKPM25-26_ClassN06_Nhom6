<template>
  <div class="min-h-screen flex justify-center items-start bg-gray-100 p-6">
    <div class="w-full max-w-4xl bg-white shadow-lg rounded-2xl p-8 space-y-6">
      <h2 class="text-2xl font-bold text-blue-600 mb-4">Thêm Giảng Viên</h2>

      <form @submit.prevent="submitForm" class="space-y-6">
        <!-- Thông tin cá nhân -->
        <h3 class="text-blue-600 font-semibold">Thông tin cá nhân</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block mb-1 font-medium">Họ và đệm</label>
            <input v-model="teacher.last_name" type="text" class="input" placeholder="VD: Nguyễn Văn" required />
          </div>
          <div>
            <label class="block mb-1 font-medium">Tên</label>
            <input v-model="teacher.first_name" type="text" class="input" placeholder="VD: An" required />
          </div>
          <div>
            <label class="block mb-1 font-medium">Số điện thoại</label>
            <input v-model="teacher.phone" type="text" class="input" placeholder="VD: 0901234567" />
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block mb-1 font-medium">Ngày sinh</label>
            <input v-model="teacher.dob" type="date" class="input" />
          </div>
          <div>
            <label class="block mb-1 font-medium">Giới tính</label>
            <select v-model="teacher.gender" class="input">
              <option value="">-- Chọn --</option>
              <option>Nam</option>
              <option>Nữ</option>
              <option>Khác</option>
            </select>
          </div>
        </div>

        <!-- Thông tin chuyên môn & quản lý -->
        <h3 class="text-blue-600 font-semibold">Thông tin chuyên môn & quản lý</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block mb-1 font-medium">Khoa quản lý</label>
            <input v-model="teacher.faculty" type="text" class="input" placeholder="VD: Khoa Công nghệ Thông tin" />
          </div>
          <div>
            <label class="block mb-1 font-medium">Bộ môn</label>
            <input v-model="teacher.department" type="text" class="input" placeholder="VD: Khoa học máy tính" />
          </div>
          <div>
            <label class="block mb-1 font-medium">Chuyên ngành</label>
            <input v-model="teacher.major" type="text" class="input" placeholder="VD: Trí tuệ nhân tạo" />
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block mb-1 font-medium">Học vị</label>
            <select v-model="teacher.degree" class="input">
              <option value="">-- Chọn --</option>
              <option>Cử nhân</option>
              <option>Thạc sĩ</option>
              <option>Tiến sĩ</option>
            </select>
          </div>
          <div>
            <label class="block mb-1 font-medium">Học hàm</label>
            <select v-model="teacher.title" class="input">
              <option value="">-- Chọn --</option>
              <option>Giảng viên</option>
              <option>Phó Giáo sư</option>
              <option>Giáo sư</option>
            </select>
          </div>
        </div>

        <!-- Nút -->
        <div class="flex justify-end gap-2">
          <button type="reset" @click="resetForm" class="btn-secondary">Làm mới</button>
          <button type="submit" class="btn-primary">Lưu</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

const teacher = reactive({
  first_name: '',
  last_name: '',
  phone: '',
  dob: '',
  gender: '',
  faculty: '',
  department: '',
  major: '',
  degree: '',
  title: ''
})

const resetForm = () => {
  Object.keys(teacher).forEach(key => teacher[key] = '')
}

const submitForm = async () => {
  try {
    const res = await fetch('http://localhost:8000/api/teachers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(teacher)
    })
    if (!res.ok) throw new Error('Lỗi khi thêm giảng viên')
    const data = await res.json()
    alert(`✅ Thêm giảng viên thành công!\nMã GV: ${data.teacher_code}\nEmail: ${data.email}`)
    resetForm()
  } catch (err) {
    console.error(err)
    alert('❌ Có lỗi xảy ra khi lưu giảng viên')
  }
}
</script>

<style>
.input {
  @apply border border-gray-300 rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-400;
}
.btn-primary {
  @apply bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700;
}
.btn-secondary {
  @apply bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500;
}
</style>
