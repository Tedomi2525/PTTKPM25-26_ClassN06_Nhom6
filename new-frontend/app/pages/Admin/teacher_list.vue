<template>
  <div class="min-h-screen p-6 bg-gray-100">
    <div class="max-w-6xl mx-auto bg-white shadow-lg rounded-2xl p-6">
      <h2 class="text-2xl font-bold text-blue-600 mb-4">Danh Sách Giảng Viên</h2>

      <div class="overflow-x-auto">
        <table class="w-full table-auto border border-gray-300">
          <thead class="bg-blue-200 text-center">
            <tr>
              <th class="border px-2 py-1">Mã GV</th>
              <th class="border px-2 py-1">Họ và đệm</th>
              <th class="border px-2 py-1">Tên</th>
              <th class="border px-2 py-1">Ngày sinh</th>
              <th class="border px-2 py-1">Giới tính</th>
              <th class="border px-2 py-1">Email</th>
              <th class="border px-2 py-1">SĐT</th>
              <th class="border px-2 py-1">Khoa</th>
              <th class="border px-2 py-1">Bộ môn</th>
              <th class="border px-2 py-1">Chuyên ngành</th>
              <th class="border px-2 py-1">Học vị</th>
              <th class="border px-2 py-1">Học hàm</th>
              <th class="border px-2 py-1">Ảnh</th>
              <th class="border px-2 py-1">Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="teacher in teachers" :key="teacher.teacherId" class="text-center hover:bg-gray-50">
              <td class="border px-2 py-1">{{ teacher.teacherCode }}</td>
              <td class="border px-2 py-1">{{ teacher.lastName }}</td>
              <td class="border px-2 py-1">{{ teacher.firstName }}</td>
              <td class="border px-2 py-1">{{ teacher.dob }}</td>
              <td class="border px-2 py-1">{{ teacher.gender }}</td>
              <td class="border px-2 py-1">{{ teacher.email }}</td>
              <td class="border px-2 py-1">{{ teacher.phone }}</td>
              <td class="border px-2 py-1">{{ teacher.faculty }}</td>
              <td class="border px-2 py-1">{{ teacher.department }}</td>
              <td class="border px-2 py-1">{{ teacher.specialization }}</td>
              <td class="border px-2 py-1">{{ teacher.degree }}</td>
              <td class="border px-2 py-1">{{ teacher.academicRank }}</td>
              <td class="border px-2 py-1">
                <img :src="teacher.avatar || 'https://via.placeholder.com/50'" class="rounded-full w-12 h-12 mx-auto" />
              </td>
              <td class="border px-2 py-1 space-x-1">
                <button @click="editTeacher(teacher.teacherId)" class="px-2 py-1 bg-yellow-500 text-white rounded hover:bg-yellow-600 text-sm">Sửa</button>
                <button @click="deleteTeacher(teacher.teacherId)" class="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600 text-sm">Xóa</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from "vue";

const teachers = reactive([]);

const fetchTeachers = async () => {
  try {
    const res = await fetch("http://localhost:8000/api/teachers");
    if (!res.ok) throw new Error("Không tải được danh sách");
    const data = await res.json();
    teachers.splice(0, teachers.length, ...data); // Thêm dữ liệu vào reactive array
  } catch (err) {
    alert("Lỗi: " + err.message);
  }
};

const deleteTeacher = async (id) => {
  if (!confirm("Bạn chắc muốn xóa?")) return;
  try {
    const res = await fetch(`http://localhost:8000/api/teachers/${id}`, { method: "DELETE" });
    if (!res.ok) throw new Error("Không xóa được");
    fetchTeachers();
  } catch (err) {
    alert("Lỗi: " + err.message);
  }
};

const editTeacher = (id) => {
  alert("Sửa giảng viên ID: " + id);
};

onMounted(fetchTeachers);
</script>

<style>
/* Bạn có thể thêm style Tailwind tùy chỉnh nếu cần */
</style>
