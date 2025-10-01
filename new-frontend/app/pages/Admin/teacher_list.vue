<template>
  <div class="container mx-auto p-4">
    <div class="bg-white shadow-lg rounded-lg">
      <div class="bg-blue-600 text-white p-4 rounded-t-lg flex justify-between items-center">
        <h2 class="text-xl font-bold">Danh Sách Giảng Viên</h2>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-blue-100 text-center">
            <tr>
              <th class="px-2 py-2">Mã GV</th>
              <th class="px-2 py-2">Họ và đệm</th>
              <th class="px-2 py-2">Tên</th>
              <th class="px-2 py-2">Ngày sinh</th>
              <th class="px-2 py-2">Giới tính</th>
              <th class="px-2 py-2">Email</th>
              <th class="px-2 py-2">SĐT</th>
              <th class="px-2 py-2">Khoa</th>
              <th class="px-2 py-2">Bộ môn</th>
              <th class="px-2 py-2">Chuyên ngành</th>
              <th class="px-2 py-2">Học vị</th>
              <th class="px-2 py-2">Học hàm</th>
              <th class="px-2 py-2">Ảnh</th>
              <th class="px-2 py-2">Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="teacher in teachers" :key="teacher.teacherId" class="text-center border-b">
              <td class="px-2 py-1">{{ teacher.teacherCode }}</td>
              <td class="px-2 py-1">{{ teacher.lastName }}</td>
              <td class="px-2 py-1">{{ teacher.firstName }}</td>
              <td class="px-2 py-1">{{ teacher.dob }}</td>
              <td class="px-2 py-1">{{ teacher.gender }}</td>
              <td class="px-2 py-1">{{ teacher.email }}</td>
              <td class="px-2 py-1">{{ teacher.phone }}</td>
              <td class="px-2 py-1">{{ teacher.faculty }}</td>
              <td class="px-2 py-1">{{ teacher.department }}</td>
              <td class="px-2 py-1">{{ teacher.specialization }}</td>
              <td class="px-2 py-1">{{ teacher.degree }}</td>
              <td class="px-2 py-1">{{ teacher.academicRank }}</td>
              <td class="px-2 py-1">
                <img :src="teacher.avatar || 'https://via.placeholder.com/50'" class="w-12 h-12 rounded-full object-cover mx-auto" />
              </td>
              <td class="px-2 py-1">
                <button @click="editTeacher(teacher.teacherId)" class="bg-yellow-400 px-2 py-1 rounded mr-1">Sửa</button>
                <button @click="deleteTeacher(teacher.teacherId)" class="bg-red-500 text-white px-2 py-1 rounded">Xóa</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const teachers = ref([])

async function fetchTeachers() {
  try {
    const res = await fetch('http://localhost:8000/api/teachers')
    if (!res.ok) throw new Error('Không tải được danh sách')
    teachers.value = await res.json()
  } catch (err) {
    alert('Lỗi: ' + err.message)
  }
}

async function deleteTeacher(id) {
  if (!confirm('Xác nhận xóa?')) return
  try {
    const res = await fetch(`http://localhost:8000/api/teachers/${id}`, { method: 'DELETE' })
    if (!res.ok) throw new Error('Không xóa được')
    fetchTeachers()
  } catch (err) {
    alert('Lỗi: ' + err.message)
  }
}

function editTeacher(id) {
  alert('Sửa giảng viên ID: ' + id)
}

onMounted(fetchTeachers)
</script>
