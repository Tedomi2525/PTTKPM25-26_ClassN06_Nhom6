<template>
  <div class="max-w-6xl mx-auto mt-4">
        <CButton type="back" variant="secondary" @click="$router.back()">Trở lại</CButton>
  </div>
  <div class="max-w-6xl mx-auto mt-4">

    <div class="bg-white shadow-lg rounded-lg overflow-hidden">
      <div class="bg-[#09f] border-b border-[#09f] rounded-t-lg text-white px-6 py-3">
        <h4 class="text-lg font-semibold">Thêm Sinh Viên</h4>
      </div>

      <div class="p-6">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          
          <div v-if="errorMessage" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4" role="alert">
              <p class="font-bold">Lỗi gửi dữ liệu!</p>
              <p>{{ errorMessage }}</p>
              <ul v-if="validationErrors" class="mt-2 list-disc list-inside text-sm">
                  <li v-for="(errors, field) in validationErrors" :key="field">
                      **{{ field }}**: {{ errors.join(', ') }}
                  </li>
              </ul>
          </div>
          <div>
            <h5 class="text-blue-600 font-semibold mb-4">Thông tin cá nhân</h5>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label for="firstName" class="block text-sm font-medium mb-1">Họ và đệm *</label>
                <InputField id="firstName" v-model="form.firstName" placeholder="VD: Đàm Anh" required />
              </div>
              <div>
                <label for="lastName" class="block text-sm font-medium mb-1">Tên *</label>
                <InputField id="lastName" v-model="form.lastName" placeholder="VD: Pháp" required />
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
              <div>
                <label for="phone" class="block text-sm font-medium mb-1">Số điện thoại *</label>
                <InputField id="phone" v-model="form.phone" placeholder="VD: 0987654321" type="tel" required />
              </div>
              <div>
                <label for="dob" class="block text-sm font-medium mb-1">Ngày sinh *</label>
                <InputField id="dob" v-model="form.dob" type="date" required />
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">

              <div>
                <label for="gender" class="block text-sm font-medium mb-1">Giới tính *</label>
                <DropDown
                  id="gender"
                  placeholder="Chọn giới tính"
                  v-model="form.gender"
                  required
                  :options="[
                    { label: 'Nam', value: 'Nam' },
                    { label: 'Nữ', value: 'Nữ' },
                    { label: 'Khác', value: 'Khác' }
                  ]"
                />
              </div>
            </div>
          </div>

          <div>
            <h5 class="text-blue-600 font-semibold mb-4">Thông tin đào tạo & quản lý</h5>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label for="className" class="block text-sm font-medium mb-1">Lớp</label>
                <InputField id="className" v-model="form.className" placeholder="VD: K17-CNTT_4" />
              </div>
              <div>
                <label for="trainingProgram" class="block text-sm font-medium mb-1">Khóa đào tạo</label>
                <InputField id="trainingProgram" v-model="form.trainingProgram" placeholder="VD: DH_K17.40" />
              </div>
                            <div>
                <label for="courseYears" class="block text-sm font-medium mb-1">Niên khóa</label>
                <InputField id="courseYears" v-model="form.courseYears" placeholder="VD: 2023-2027" />
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">

              <div>
                <label for="educationType" class="block text-sm font-medium mb-1">Hệ đào tạo</label>
                <DropDown
                  id="educationType"
                  placeholder="Chọn hệ đào tạo"
                  v-model="form.educationType"
                  :options="[
                    { label: 'Đại học chính quy', value: 'Đại học chính quy' },
                    { label: 'Đại học từ xa', value: 'Đại học từ xa' }
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
                <label for="status" class="block text-sm font-medium mb-1">Trạng thái</label>
                <DropDown
                  id="status"
                  placeholder="Trạng thái"
                  v-model="form.status"
                  :options="[
                    { label: 'Đang học', value: 'Đang học' },
                    { label: 'Bảo lưu', value: 'Bảo lưu' },
                    { label: 'Đã tốt nghiệp', value: 'Đã tốt nghiệp' }
                  ]"
                />
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

          <div class="flex justify-end space-x-2">
            <CButton type="reset" variant="secondary" @click="resetForm">Hủy bỏ</CButton>
            <CButton type="submit" variant="primary" :disabled="isSubmitting">
              {{ isSubmitting ? 'Đang lưu...' : 'Lưu sinh viên' }}
            </CButton>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

definePageMeta({
  layout: "dashboard",
});

const router = useRouter();

const form = ref({
  firstName: "",
  lastName: "",
  phone: "",
  dob: "",
  gender: "",
  className: "",
  trainingProgram: "",
  courseYears: "",
  educationType: "",
  faculty: "",
  major: "",
  status: "Đang học",
  position: "",
  avatar: null, // dùng để chứa File object hoặc null
});

const isSubmitting = ref(false);
const errorMessage = ref(null);
const validationErrors = ref(null);

// =======================================================
// HANDLE FILE UPLOAD
// =======================================================
const handleFileUpload = (fileObject) => {
  if (fileObject instanceof File) {
    form.value.avatar = fileObject;
  } else if (fileObject && fileObject.file instanceof File) {
    form.value.avatar = fileObject.file;
  } else {
    form.value.avatar = null;
  }
  console.log("Avatar selected:", form.value.avatar);
};

// =======================================================
// RESET FORM
// =======================================================
const resetForm = () => {
  form.value = {
    firstName: "",
    lastName: "",
    phone: "",
    dob: "",
    gender: "",
    className: "",
    trainingProgram: "",
    courseYears: "",
    educationType: "",
    faculty: "",
    major: "",
    status: "Đang học",
    position: "",
    avatar: null,
  };
};

// =======================================================
// SUBMIT FORM
// =======================================================
const handleSubmit = async () => {
  errorMessage.value = null;
  validationErrors.value = null;
  isSubmitting.value = true;

  try {
    // 🔹 Tạo FormData (chỉ dùng multipart form)
    const formData = new FormData();

    for (const [key, value] of Object.entries(form.value)) {
      if (key === "avatar") {
        if (value instanceof File) {
          formData.append("avatar_file", value); // backend nhận avatar_file
        }
      } else if (value !== null && value !== "") {
        if (key === "dob" && value) {
          const date = new Date(value);
          if (!isNaN(date)) {
            formData.append("dob", date.toISOString().split("T")[0]);
          }
        } else {
          formData.append(key, value);
        }
      }
    }

    console.log("📤 Sending FormData:");
    for (const [key, val] of formData.entries()) {
      console.log(`  ${key}:`, val);
    }

    const response = await fetch("http://localhost:8000/api/students", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error("Server response:", errorData);
      throw new Error(
        errorData.detail?.[0]?.msg || `HTTP ${response.status} - ${response.statusText}`
      );
    }

    const data = await response.json();

    alert(`✅ Thêm sinh viên thành công!\nMã SV: ${data.studentCode || "N/A"}`);

    resetForm();
    router.push("/admin/dashboard/student_list");
  } catch (err) {
    console.error("❌ Error submitting form:", err);
    errorMessage.value = err.message || "Có lỗi xảy ra khi lưu sinh viên.";
  } finally {
    isSubmitting.value = false;
  }
};
</script>
