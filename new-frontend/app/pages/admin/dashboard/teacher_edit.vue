<template>
  <div class="max-w-6xl mx-auto mt-4 px-4">
    <CButton type="back" variant="secondary" @click="$router.back()">Trở lại</CButton>
  </div>

  <div class="max-w-6xl mx-auto mt-4 px-4">
    <div class="bg-white shadow-lg rounded-lg overflow-hidden">
      <div class="bg-[#09f] border-b border-[#09f] rounded-t-lg text-white px-6 py-3">
        <h4 class="text-lg font-semibold">Chỉnh sửa Giảng Viên</h4>
      </div>

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
                <InputField v-model="form.specialization" placeholder="VD: Kỹ thuật phần mềm" />
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
          <div class="flex justify-end space-x-2">
            <CButton type="reset" variant="secondary" @click="resetForm">Khôi phục</CButton>
            <CButton type="submit" variant="primary" :disabled="isSubmitting">
              {{ isSubmitting ? 'Đang cập nhật...' : 'Cập nhật giảng viên' }}
            </CButton>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import DropDown from "~/components/DropDown.vue";
import { useAuth } from "~/composables/useAuth";

const { token } = useAuth();
const router = useRouter();
const teacherId = localStorage.getItem("editTeacherId"); // ✅ lấy từ localStorage

const isSubmitting = ref(false);
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

const fetchTeacher = async () => {
  try {
    const res = await fetch(`http://localhost:8000/api/teachers/${teacherId}`, {
      headers: {
        "Authorization": `Bearer ${token.value}`,
      },
    });
    if (!res.ok) throw new Error("Không tải được dữ liệu giảng viên");
    const data = await res.json();

    if (data.dob) data.dob = data.dob.split("T")[0];
    form.value = { ...data };
  } catch (err) {
    console.error(err);
    alert("Không thể tải thông tin giảng viên");
  }
};

const resetForm = () => {
  fetchTeacher();
};

const handleSubmit = async () => {
  isSubmitting.value = true;
  try {
    const res = await fetch(`http://localhost:8000/api/teachers/${teacherId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token.value}`,
      },
      body: JSON.stringify(form.value),
    });

    const data = await res.json();

    if (!res.ok) {
      console.error("Lỗi server:", data);
      alert("Cập nhật thất bại: " + (data.detail || JSON.stringify(data)));
      return;
    }

    alert("✅ Cập nhật giảng viên thành công!");
    router.push("/Admin/dashboard/teacher_list"); // ✅ trở lại danh sách
  } catch (err) {
    console.error("Lỗi:", err);
    alert("Không thể cập nhật giảng viên");
  } finally {
    isSubmitting.value = false;
  }
};

onMounted(async () => {
  if (!teacherId) {
    alert("Không tìm thấy ID giảng viên!");
    router.push("/Admin/dashboard/teacher_list");
    return;
  }
  await fetchTeacher();
});

definePageMeta({
  layout: "dashboard",
});
</script>
