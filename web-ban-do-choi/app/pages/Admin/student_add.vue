<template>
  <div class="max-w-6xl mx-auto mt-8 px-4">
    <div class="bg-white shadow-lg rounded-lg overflow-hidden">
      <div class="bg-blue-600 text-white px-6 py-3">
        <h4 class="text-lg font-semibold">Thêm Sinh Viên</h4>
      </div>

      <div class="p-6">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- THÔNG TIN CÁ NHÂN -->
          <div>
            <h5 class="text-blue-600 font-semibold mb-4">Thông tin cá nhân</h5>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label class="block text-sm font-medium mb-1">Họ và đệm</label>
                <input v-model="form.first_name" type="text" placeholder="VD: Hoàng Minh"
                  class="w-full border rounded px-3 py-2 focus:ring focus:ring-blue-300" />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">Tên</label>
                <input v-model="form.last_name" type="text" placeholder="VD: Quân"
                  class="w-full border rounded px-3 py-2 focus:ring focus:ring-blue-300" />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">Số điện thoại</label>
                <input v-model="form.phone" type="text" placeholder="VD: 0987654321"
                  class="w-full border rounded px-3 py-2 focus:ring focus:ring-blue-300" />
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
              <div>
                <label class="block text-sm font-medium mb-1">Ngày sinh</label>
                <input v-model="form.dob" type="date"
                  class="w-full border rounded px-3 py-2 focus:ring focus:ring-blue-300" />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">Giới tính</label>
                <select v-model="form.gender"
                  class="w-full border rounded px-3 py-2 focus:ring focus:ring-blue-300">
                  <option value="">-- Chọn --</option>
                  <option value="Nam">Nam</option>
                  <option value="Nữ">Nữ</option>
                  <option value="Khác">Khác</option>
                </select>
              </div>
            </div>
          </div>

          <!-- THÔNG TIN ĐÀO TẠO & QUẢN LÝ -->
          <div>
            <h5 class="text-blue-600 font-semibold mb-4">Thông tin đào tạo & quản lý</h5>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label class="block text-sm font-medium mb-1">Lớp</label>
                <input v-model="form.class_name" type="text" placeholder="VD: K17-CNTT_4"
                  class="w-full border rounded px-3 py-2 focus:ring focus:ring-blue-300" />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">Khóa đào tạo</label>
                <input v-model="form.training_program" type="text" placeholder="VD: DH_K17.40"
                  class="w-full border rounded px-3 py-2 focus:ring focus:ring-blue-300" />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">Niên khóa</label>
                <input v-model="form.course_years" type="text" placeholder="VD: 2023-2027"
                  class="w-full border rounded px-3 py-2 focus:ring focus:ring-blue-300" />
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
              <div>
                <label class="block text-sm font-medium mb-1">Hệ đào tạo</label>
                <select v-model="form.education_type"
                  class="w-full border rounded px-3 py-2 focus:ring focus:ring-blue-300">
                  <option value="">-- Chọn --</option>
                  <option value="Đại học chính quy">Đại học chính quy</option>
                  <option value="Liên thông">Liên thông</option>
                  <option value="Cao đẳng">Cao đẳng</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">Khoa quản lý</label>
                <input v-model="form.faculty" type="text" placeholder="VD: Khoa Công nghệ Thông tin"
                  class="w-full border rounded px-3 py-2 focus:ring focus:ring-blue-300" />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">Ngành</label>
                <input v-model="form.major" type="text" placeholder="VD: Công nghệ thông tin"
                  class="w-full border rounded px-3 py-2 focus:ring focus:ring-blue-300" />
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
              <div>
                <label class="block text-sm font-medium mb-1">Trạng thái</label>
                <select v-model="form.status"
                  class="w-full border rounded px-3 py-2 focus:ring focus:ring-blue-300">
                  <option value="Đang học">Đang học</option>
                  <option value="Bảo lưu">Bảo lưu</option>
                  <option value="Đã tốt nghiệp">Đã tốt nghiệp</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">Chức vụ</label>
                <input v-model="form.position" type="text" placeholder="VD: Sinh viên"
                  class="w-full border rounded px-3 py-2 focus:ring focus:ring-blue-300" />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">Ảnh đại diện</label>
                <input type="file" @change="handleFileUpload"
                  class="w-full border rounded px-3 py-2 focus:ring focus:ring-blue-300" />
              </div>
            </div>
          </div>

          <!-- NÚT -->
          <div class="flex justify-end space-x-2">
            <button type="reset" class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400">Làm mới</button>
            <button type="submit"
              class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Lưu sinh viên</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const form = ref({
  first_name: "",
  last_name: "",
  phone: "",
  dob: "",
  gender: "",
  class_name: "",
  training_program: "",
  course_years: "",
  education_type: "",
  faculty: "",
  major: "",
  status: "Đang học",
  position: "",
  avatar: null,
});

const handleFileUpload = (event) => {
  form.value.avatar = event.target.files[0];
};

const handleSubmit = async () => {
  try {
    const { avatar, ...studentData } = form.value;

    const response = await fetch("http://localhost:8000/api/students", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(studentData),
    });

    if (!response.ok) {
      throw new Error("Lỗi khi thêm sinh viên");
    }

    const data = await response.json();
    alert("Thêm sinh viên thành công! Mã SV: " + data.student_code);

    // reset form
    Object.keys(form.value).forEach((key) => (form.value[key] = ""));
  } catch (err) {
    console.error(err);
    alert("Có lỗi xảy ra khi lưu sinh viên");
  }
};
</script>
