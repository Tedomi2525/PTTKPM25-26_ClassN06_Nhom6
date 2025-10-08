<template>
  <div class="px-4">
    <CButton type="back" variant="secondary" @click="$router.back()">Trở lại</CButton>
  </div>
  <div class="max-w-6xl mx-auto mt-8 px-4">
    <div class="bg-white shadow-lg rounded-lg overflow-hidden">
      <div class="bg-[#09f] text-white px-6 py-3">
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
                <label for="email" class="block text-sm font-medium mb-1">Email *</label>
                <InputField id="email" v-model="form.email" placeholder="VD: phapdang@email.com" type="email" required />
              </div>
              <div>
                <label for="phone" class="block text-sm font-medium mb-1">Số điện thoại *</label>
                <InputField id="phone" v-model="form.phone" placeholder="VD: 0987654321" type="tel" required />
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
              <div>
                <label for="dob" class="block text-sm font-medium mb-1">Ngày sinh *</label>
                <InputField id="dob" v-model="form.dob" type="date" required />
              </div>
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
                    { label: 'Tạm dừng', value: 'Tạm dừng' },
                    { label: 'Tốt nghiệp', value: 'Tốt nghiệp' }
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
import DropDown from "~/components/DropDown.vue";
import { useRouter } from "vue-router"; 

definePageMeta({
  layout: 'dashboard'
});

const router = useRouter();

const form = ref({
  firstName: "", 
  lastName: "", 
  email: "",
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
});

const isSubmitting = ref(false);
const errorMessage = ref(null);
const validationErrors = ref(null);

const handleFileUpload = (fileObject) => {
  // Giả định component ImageAddButton emit ra file object hoặc File
  if (fileObject instanceof File) {
    form.value.avatar = fileObject;
  } else if (fileObject && fileObject.file instanceof File) {
    form.value.avatar = fileObject.file;
  } else {
    form.value.avatar = fileObject;
  }
  console.log('Avatar file selected:', form.value.avatar);
};

const resetForm = () => {
  // Đặt lại các trường về giá trị mặc định/rỗng
  form.value = {
    firstName: "", 
    lastName: "", 
    email: "",
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


const handleSubmit = async () => {
  errorMessage.value = null;
  validationErrors.value = null;
  isSubmitting.value = true;
  
  // 1. Chuẩn bị FormData (Dùng cho API hỗ trợ upload File và dữ liệu cùng lúc)
  const formData = new FormData();
  let usesFormData = false;

  // Lặp qua các trường form
  for (const key in form.value) {
    if (key === 'avatar' && form.value[key] instanceof File) {
      formData.append('avatar', form.value[key]); // Use 'avatar' as the field name (backend expects this)
      usesFormData = true;
      console.log('Added avatar file to FormData:', form.value[key].name);
    } else if (key !== 'avatar' && form.value[key] !== null && form.value[key] !== '') {
      // Đảm bảo DOB được gửi ở định dạng string 'YYYY-MM-DD'
      if (key === 'dob' && form.value[key]) {
         formData.append(key, new Date(form.value[key]).toISOString().split('T')[0]);
      } else {
         formData.append(key, form.value[key]);
      }
    }
  }

  // Chọn phương thức gửi: FormData (nếu có file) hoặc JSON (nếu không có file hoặc API chỉ nhận JSON)
  const fetchOptions = {
    method: "POST",
  };

  if (usesFormData) {
    fetchOptions.body = formData;
    // Không cần set 'Content-Type': 'multipart/form-data', trình duyệt tự làm
  } else {
    // Nếu API chỉ nhận JSON, ngay cả khi có file (avatar là URL string), ta cần gửi JSON
    const payload = { ...form.value };
    if (payload.avatar instanceof File) {
      // Loại bỏ File nếu API không hỗ trợ Form-data hoặc File chưa được upload
      delete payload.avatar;
    }
    
    // Đảm bảo DOB ở định dạng 'YYYY-MM-DD'
    if (payload.dob) {
        payload.dob = new Date(payload.dob).toISOString().split('T')[0];
    }
    
    fetchOptions.headers = { "Content-Type": "application/json" };
    fetchOptions.body = JSON.stringify(payload);
  }
  
  try {
    console.log('Sending request with FormData:', usesFormData ? 'Yes' : 'No');
    if (usesFormData) {
      console.log('FormData contents:');
      for (let [key, value] of formData.entries()) {
        console.log(key, value);
      }
    }
    
    const response = await fetch("http://localhost:8000/api/students", fetchOptions);

    if (response.status === 422) {
      const errorData = await response.json();
      errorMessage.value = 'Dữ liệu nhập vào không hợp lệ. Vui lòng kiểm tra các trường bị lỗi.';
      if (errorData.errors) {
        validationErrors.value = errorData.errors;
      }
      return; 
    }

    if (!response.ok) {
      throw new Error(`Lỗi HTTP: ${response.status} - ${response.statusText}`);
    }

    const data = await response.json();
    
    let successMessage = "Thêm sinh viên thành công! Mã SV: " + (data.studentCode || data.id);
    if (data.avatar) {
      successMessage += "\nẢnh đại diện đã được lưu: " + data.avatar;
    }
    
    alert(successMessage);

    // Reset form after successful submission
    resetForm();
    
    // Navigate to student list
    router.push('/admin/dashboard/student_list');
    
  } catch (err) {
    console.error(err);
    errorMessage.value = err.message || "Có lỗi xảy ra khi lưu sinh viên";
  } finally {
    isSubmitting.value = false;
  }
};
</script>