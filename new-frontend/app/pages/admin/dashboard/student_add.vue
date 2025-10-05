<template>
  <div class="p-6">
    <CButton type="back" variant="secondary">Trở lại</CButton>
  </div>
  <div class="max-w-6xl mx-auto mt-8 px-4">
    <div class="bg-white shadow-lg rounded-lg overflow-hidden">
      <div class="bg-[#09f] text-white px-6 py-3">
        <h4 class="text-lg font-semibold">Thêm Sinh Viên</h4>
      </div>

      <div class="p-6">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- THÔNG TIN CÁ NHÂN -->
          <div>
            <h5 class="text-blue-600 font-semibold mb-4">Thông tin cá nhân</h5>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label for="first_name" class="block text-sm font-medium mb-1">Họ và đệm</label>
                <InputField id="first_name" v-model="form.first_name" placeholder="VD: Hoàng Minh" />
              </div>
              <div>
                <label for="last_name" class="block text-sm font-medium mb-1">Tên</label>
                <InputField id="last_name" v-model="form.last_name" placeholder="VD: Quân" />
              </div>
              <div>
                <label for="phone" class="block text-sm font-medium mb-1">Số điện thoại</label>
                <InputField id="phone" v-model="form.phone" placeholder="VD: 0987654321" />
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
              <div>
                <label for="dob" class="block text-sm font-medium mb-1">Ngày sinh</label>
                <InputField id="dob" v-model="form.dob" type="date" />
              </div>
              <div>
                <label for="gender" class="block text-sm font-medium mb-1">Giới tính</label>
                <DropDown
                  id="gender"
                  placeholder="Chọn giới tính"
                  v-model="form.gender"
                  :options="[
                    { label: 'Nam', value: 'Nam' },
                    { label: 'Nữ', value: 'Nữ' },
                    { label: 'Khác', value: 'Khác' }
                  ]"
                />
              </div>
            </div>
          </div>

          <!-- THÔNG TIN ĐÀO TẠO & QUẢN LÝ -->
          <div>
            <h5 class="text-blue-600 font-semibold mb-4">Thông tin đào tạo & quản lý</h5>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label for="class_name" class="block text-sm font-medium mb-1">Lớp</label>
                <InputField id="class_name" v-model="form.class_name" placeholder="VD: K17-CNTT_4" />
              </div>
              <div>
                <label for="training_program" class="block text-sm font-medium mb-1">Khóa đào tạo</label>
                <InputField id="training_program" v-model="form.training_program" placeholder="VD: DH_K17.40" />
              </div>
              <div>
                <label for="course_years" class="block text-sm font-medium mb-1">Niên khóa</label>
                <InputField id="course_years" v-model="form.course_years" placeholder="VD: 2023-2027" />
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
              <div>
                <label for="education_type" class="block text-sm font-medium mb-1">Hệ đào tạo</label>
                <DropDown
                  id="education_type"
                  placeholder="Chọn hệ đào tạo"
                  v-model="form.education_type"
                  :options="[
                    { label: 'Chính quy', value: 'Chính quy' },
                    { label: 'Từ xa', value: 'Từ xa' }
                  ]"
                />
              </div>
              <div>
                <label for="faculty" class="block text-sm font-medium mb-1">Khoa quản lý</label>
                <InputField id="faculty" v-model="form.faculty" placeholder="VD: Khoa Công nghệ Thông tin" />
              </div>
              <div>
                <label for="major" class="block text-sm font-medium mb-1">Ngành</label>
                <InputField id="major" v-model="form.major" placeholder="VD: Công nghệ thông tin" />
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
              <div>
                <label for="position" class="block text-sm font-medium mb-1">Chức vụ</label>
                <InputField id="position" v-model="form.position" placeholder="VD: Sinh viên" />
              </div>
              <div>
                <label for="avatar" class="block text-sm font-medium mb-1">Ảnh đại diện</label>
                <ImageAddButton
                  id="avatar"
                  buttonText="Tải ảnh lên"
                  @update:file="handleFileUpload"
                />
              </div>
            </div>
          </div>

          <!-- NÚT -->
          <div class="flex justify-end space-x-2">
            <button
              type="reset"
              class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400 transition"
            >
              Làm mới
            </button>
            <CButton type="submit">Lưu sinh viên</CButton>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref } from "vue";
import DropDown from "~/components/DropDown.vue";

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

definePageMeta({
  layout: 'dashboard'
})
</script>
