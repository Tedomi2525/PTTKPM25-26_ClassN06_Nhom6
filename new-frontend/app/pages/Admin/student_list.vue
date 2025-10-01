<template>
  <div class="container mx-auto p-4">
    <div class="bg-white shadow-lg rounded-lg">
      <div class="bg-blue-600 text-white p-4 rounded-t-lg flex justify-between items-center">
        <h2 class="text-xl font-bold">Danh Sách Sinh Viên</h2>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-blue-100 text-center">
            <tr>
              <th class="px-2 py-2">Mã SV</th>
              <th class="px-2 py-2">Họ và đệm</th>
              <th class="px-2 py-2">Tên</th>
              <th class="px-2 py-2">Ngày sinh</th>
              <th class="px-2 py-2">Giới tính</th>
              <th class="px-2 py-2">Email</th>
              <th class="px-2 py-2">SĐT</th>
              <th class="px-2 py-2">Lớp</th>
              <th class="px-2 py-2">Trạng thái</th>
              <th class="px-2 py-2">Ảnh</th>
              <th class="px-2 py-2">Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="student in students" :key="student.studentId" class="text-center border-b">
              <td class="px-2 py-1">{{ student.studentCode }}</td>
              <td class="px-2 py-1">{{ student.lastName }}</td>
              <td class="px-2 py-1">{{ student.firstName }}</td>
              <td class="px-2 py-1">{{ student.dob }}</td>
              <td class="px-2 py-1">{{ student.gender }}</td>
              <td class="px-2 py-1">{{ student.email }}</td>
              <td class="px-2 py-1">{{ student.phone }}</td>
              <td class="px-2 py-1">{{ student.className }}</td>
              <td :class="student.status === 'Đang học' ? 'text-green-500' : 'text-red-500'">{{ student.status }}</td>
              <td class="px-2 py-1">
                <img :src="student.avatar || 'https://via.placeholder.com/50'" class="w-12 h-12 rounded-full object-cover mx-auto" />
              </td>
              <td class="px-2 py-1">
                <button @click="editStudent(student.studentId)" class="bg-yellow-400 px-2 py-1 rounded mr-1">Sửa</button>
                <button @click="deleteStudent(student.studentId)" class="bg-red-500 text-white px-2 py-1 rounded">Xóa</button>
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

const students = ref([])

async function fetchStudents() {
  try {
    const res = await fetch('http://localhost:8000/api/students')
    if (!res.ok) throw new Error('Không tải được danh sách')
    students.value = await res.json()
  } catch (err) {
    alert('Lỗi: ' + err.message)
  }
}

async function deleteStudent(id) {
  if (!confirm('Xác nhận xóa?')) return
  try {
    const res = await fetch(`http://localhost:8000/api/students/${id}`, { method: 'DELETE' })
    if (!res.ok) throw new Error('Không xóa được')
    fetchStudents()
  } catch (err) {
    alert('Lỗi: ' + err.message)
  }
}

function editStudent(id) {
  alert('Sửa sinh viên ID: ' + id)
}

onMounted(fetchStudents)
</script>
