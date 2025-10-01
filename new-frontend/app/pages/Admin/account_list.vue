<template>
  <div class="max-w-5xl mx-auto mt-8 px-4">
    <h3 class="text-2xl font-semibold mb-6">Danh sách Tài khoản 🔑</h3>

    <!-- Nút chọn -->
    <div class="mb-4 space-x-2">
      <button
        @click="active = 'student'"
        class="px-4 py-2 rounded text-white"
        :class="active === 'student' ? 'bg-blue-600' : 'bg-blue-400 hover:bg-blue-500'"
      >
        Tài khoản Sinh viên
      </button>
      <button
        @click="active = 'teacher'"
        class="px-4 py-2 rounded text-white"
        :class="active === 'teacher' ? 'bg-green-600' : 'bg-green-400 hover:bg-green-500'"
      >
        Tài khoản Giảng viên
      </button>
    </div>

    <!-- Bảng tài khoản Sinh viên -->
    <div
      v-if="active === 'student'"
      class="bg-white shadow rounded-lg overflow-hidden"
    >
      <div class="bg-blue-600 text-white px-4 py-2 font-semibold">
        Tài khoản Sinh viên
      </div>
      <div class="p-4 overflow-x-auto">
        <table class="min-w-full border text-sm">
          <thead class="bg-gray-100">
            <tr>
              <th class="border px-4 py-2">Mã SV</th>
              <th class="border px-4 py-2">Tên Sinh viên</th>
              <th class="border px-4 py-2">Email</th>
              <th class="border px-4 py-2">Tài khoản</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="border px-4 py-2">SV001</td>
              <td class="border px-4 py-2">Nguyễn Văn A</td>
              <td class="border px-4 py-2">a.nguyen@example.com</td>
              <td class="border px-4 py-2">a.nguyen</td>
            </tr>
            <tr class="bg-gray-50">
              <td class="border px-4 py-2">SV002</td>
              <td class="border px-4 py-2">Trần Thị B</td>
              <td class="border px-4 py-2">b.tran@example.com</td>
              <td class="border px-4 py-2">b.tran</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Bảng tài khoản Giảng viên -->
    <div
      v-if="active === 'teacher'"
      class="bg-white shadow rounded-lg overflow-hidden"
    >
      <div class="bg-green-600 text-white px-4 py-2 font-semibold">
        Tài khoản Giảng viên
      </div>
      <div class="p-4 overflow-x-auto">
        <table class="min-w-full border text-sm">
          <thead class="bg-gray-100">
            <tr>
              <th class="border px-4 py-2">Mã GV</th>
              <th class="border px-4 py-2">Tên Giảng viên</th>
              <th class="border px-4 py-2">Email</th>
              <th class="border px-4 py-2">Tài khoản</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="border px-4 py-2">GV001</td>
              <td class="border px-4 py-2">Phạm Văn C</td>
              <td class="border px-4 py-2">c.pham@example.com</td>
              <td class="border px-4 py-2">c.pham</td>
            </tr>
            <tr class="bg-gray-50">
              <td class="border px-4 py-2">GV002</td>
              <td class="border px-4 py-2">Lê Thị D</td>
              <td class="border px-4 py-2">d.le@example.com</td>
              <td class="border px-4 py-2">d.le</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const active = ref("student"); // mặc định hiển thị bảng sinh viên
</script>
