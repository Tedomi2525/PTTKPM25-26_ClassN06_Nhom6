<template>
  <div class="p-6">
    <CButton type="back" variant="secondary">Trở lại</CButton>
  </div>
  <div class="max-w-6xl mx-auto mt-8 px-4">
    <div class="bg-white shadow-lg rounded-lg overflow-hidden">
      <div class="bg-[#09f] text-white px-6 py-3">
        <h4 class="text-lg font-semibold">Thêm Giảng Viên</h4>
      </div>

      <div class="p-6">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- THÔNG TIN CÁ NHÂN -->
          <div>
            <h5 class="text-blue-600 font-semibold mb-4">Thông tin cá nhân</h5>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label class="block text-sm font-medium mb-1">Họ và đệm</label>
                <InputField v-model="form.first_name" placeholder="VD: Nguyễn Văn" />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">Tên</label>
                <InputField v-model="form.last_name" placeholder="VD: An" />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">Số điện thoại</label>
                <InputField v-model="form.phone" placeholder="VD: 0987654321" />
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
              <div>
                <label class="block text-sm font-medium mb-1">Ngày sinh</label>
                <InputField v-model="form.dob" type="date" />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">Giới tính</label>
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
              <div>
                <label class="block text-sm font-medium mb-1">Email</label>
                <InputField v-model="form.email" type="email" placeholder="VD: nva@phenikaa-uni.edu.vn" />
              </div>
            </div>
          </div>

          <!-- THÔNG TIN CÔNG TÁC -->
          <div>
            <h5 class="text-blue-600 font-semibold mb-4">Thông tin công tác</h5>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label class="block text-sm font-medium mb-1">Khoa/Bộ môn</label>
                <InputField v-model="form.department" placeholder="VD: Khoa Công nghệ Thông tin" />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">Học vị</label>
                <DropDown
                  id="degree"
                  placeholder="Chọn học vị"
                  v-model="form.degree"
                  :options="[
                    { label: 'Tiến sĩ', value: 'Tiến sĩ' },
                    { label: 'Thạc sĩ', value: 'Thạc sĩ' },
                    { label: 'Kỹ sư', value: 'Kỹ sư' },
                    { label: 'Cử nhân', value: 'Cử nhân' }
                  ]"
                />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">Chức vụ</label>
                <DropDown
                  id="position"
                  placeholder="Chọn chức vụ"
                  v-model="form.position"
                  :options="[
                    { label: 'Giảng viên', value: 'Giảng viên' },
                    { label: 'Trưởng bộ môn', value: 'Trưởng bộ môn' },
                    { label: 'Phó trưởng bộ môn', value: 'Phó trưởng bộ môn' },
                    { label: 'Trưởng khoa', value: 'Trưởng khoa' },
                    { label: 'Phó trưởng khoa', value: 'Phó trưởng khoa' }
                  ]"
                />
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
              <div>
                <label class="block text-sm font-medium mb-1">Chuyên ngành</label>
                <InputField v-model="form.specialization" placeholder="VD: Kỹ thuật phần mềm" />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">Năm kinh nghiệm</label>
                <InputField v-model="form.experience_years" type="number" placeholder="VD: 5" />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">Trạng thái</label>
                <DropDown
                  id="status"
                  placeholder="Chọn trạng thái"
                  v-model="form.status"
                  :options="[
                    { label: 'Đang công tác', value: 'Đang công tác' },
                    { label: 'Tạm nghỉ', value: 'Tạm nghỉ' },
                    { label: 'Đã nghỉ việc', value: 'Đã nghỉ việc' }
                  ]"
                />
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
              <div>
                <label class=" block text-sm font-medium mb-1">Ngày bắt đầu làm việc</label>
                <InputField v-model="form.start_date" type="date" />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">Ảnh đại diện</label>
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
            <button type="reset" class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400" @click="resetForm">Làm mới</button>
            <CButton type="submit">Lưu giảng viên</CButton>
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
  email: "",
  dob: "",
  gender: "",
  department: "",
  degree: "",
  position: "",
  specialization: "",
  experience_years: "",
  start_date: "",
  status: "Đang công tác",
  avatar: null,
});

const handleFileUpload = (event) => {
  form.value.avatar = event.target.files[0];
};

const resetForm = () => {
  Object.keys(form.value).forEach((key) => {
    if (key === 'status') {
      form.value[key] = 'Đang công tác';
    } else if (key === 'avatar') {
      form.value[key] = null;
    } else {
      form.value[key] = '';
    }
  });
};

const handleSubmit = async () => {
  try {
    const { avatar, ...teacherData } = form.value;

    const response = await fetch("http://localhost:8000/api/teachers", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(teacherData),
    });

    if (!response.ok) {
      throw new Error("Lỗi khi thêm giảng viên");
    }

    const data = await response.json();
    alert("Thêm giảng viên thành công! Mã GV: " + data.teacher_code);

    // reset form
    resetForm();
  } catch (err) {
    console.error(err);
    alert("Có lỗi xảy ra khi lưu giảng viên");
  }
};

definePageMeta({
  layout: 'dashboard'
})
</script>
