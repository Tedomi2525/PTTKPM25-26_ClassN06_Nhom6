<template>
  <div class="p-6">
    <CButton type="back" variant="secondary">Trở lại</CButton>
  </div>

  <div class="max-w-5xl mx-auto mt-8 px-4">
    <div class="bg-white shadow-lg rounded-lg overflow-hidden">
      <!-- Header -->
      <div class="bg-blue-600 text-white px-6 py-3">
        <h4 class="text-lg font-semibold">Thêm Giảng Viên</h4>
      </div>

      <!-- Body -->
      <div class="p-6">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- THÔNG TIN CÁ NHÂN -->
          <div>
            <h5 class="text-blue-600 font-semibold mb-4">Thông tin cá nhân</h5>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label class="block text-sm font-medium mb-1">Họ</label>
                <InputField v-model="form.firstName" placeholder="VD: Nguyen" />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">Tên</label>
                <InputField v-model="form.lastName" placeholder="VD: An" />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">Ngày sinh</label>
                <InputField v-model="form.dob" type="date" />
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
              <div>
                <label class="block text-sm font-medium mb-1">Giới tính</label>
                <DropDown
                  v-model="form.gender"
                  placeholder="Chọn giới tính"
                  :options="[
                    { label: 'Nam', value: 1 },
                    { label: 'Nữ', value: 0 },
                  ]"
                />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">Số điện thoại</label>
                <InputField v-model="form.phone" placeholder="VD: 0987654321" />
              </div>
            </div>
          </div>

          <!-- THÔNG TIN CÔNG TÁC -->
          <div>
            <h5 class="text-blue-600 font-semibold mb-4">Thông tin công tác</h5>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label class="block text-sm font-medium mb-1">Khoa</label>
                <InputField v-model="form.faculty" placeholder="VD: Công nghệ" />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">Bộ môn</label>
                <InputField v-model="form.department" placeholder="VD: CNTT" />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">Chuyên ngành</label>
                <InputField
                  v-model="form.specialization"
                  placeholder="VD: Kỹ thuật phần mềm"
                />
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
              <div>
                <label class="block text-sm font-medium mb-1">Học vị</label>
                <DropDown
                  v-model="form.degree"
                  placeholder="Chọn học vị"
                  :options="[
                    { label: 'Cử nhân', value: 'Cử nhân' },
                    { label: 'Kỹ sư', value: 'Kỹ sư' },
                    { label: 'Thạc sĩ', value: 'Thạc sĩ' },
                    { label: 'Tiến sĩ', value: 'Tiến sĩ' }
                  ]"
                />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">Học hàm</label>
                <DropDown
                  v-model="form.academicRank"
                  placeholder="Chọn học hàm"
                  :options="[
                    { label: 'Giảng viên', value: 'Giảng viên' },
                    { label: 'Phó giáo sư', value: 'Phó giáo sư' },
                    { label: 'Giáo sư', value: 'Giáo sư' }
                  ]"
                />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">Trạng thái</label>
                <DropDown
                  v-model="form.status"
                  placeholder="Chọn trạng thái"
                  :options="[
                    { label: 'Đang công tác', value: 'active' },
                    { label: 'Tạm nghỉ', value: 'inactive' },
                    { label: 'Nghỉ hưu', value: 'retired' }
                  ]"
                />
              </div>
            </div>
          </div>

          <!-- NÚT -->
          <div class="flex justify-end space-x-2 mt-8">
            <button
              type="reset"
              class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
              @click="resetForm"
            >
              Làm mới
            </button>
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
import { useAuth } from "~/composables/useAuth"; // 👈 thêm dòng này

const { token } = useAuth(); // 👈 lấy token hiện tại

const form = ref({
  firstName: "",
  lastName: "",
  dob: "",
  gender: "",
  phone: "",
  department: "",
  faculty: "",
  specialization: "",
  degree: "",
  academicRank: "",
  status: "active",
});

const resetForm = () => {
  Object.keys(form.value).forEach((key) => {
    if (key === "status") form.value[key] = "active";
    else form.value[key] = "";
  });
};

const handleSubmit = async () => {
  try {
    console.log("Payload gửi đi:", JSON.stringify(form.value, null, 2));
    console.log("Token dùng để gửi:", token.value);

    const response = await fetch("http://localhost:8000/api/teachers", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token.value}`, // 👈 gửi token ở đây
      },
      body: JSON.stringify(form.value),
    });

    const data = await response.json();

    if (!response.ok) {
      console.error("Lỗi server:", data);
      alert("Lỗi khi thêm giảng viên: " + (data.detail || JSON.stringify(data)));
      return;
    }

    alert("✅ Thêm giảng viên thành công! Mã GV: " + data.teacherCode);
    resetForm();
  } catch (err) {
    console.error("Lỗi kết nối:", err);
    alert("Không thể kết nối đến server");
  }
};

definePageMeta({
  layout: "dashboard",
});
</script>
