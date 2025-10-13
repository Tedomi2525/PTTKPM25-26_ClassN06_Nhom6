<template>
  <div
    v-if="show"
    class="fixed inset-0 bg-black/50 backdrop-blur-md flex justify-center items-center z-50 transition-all duration-300"
    @click.self="close"
  >
    <div
      class="bg-white rounded-lg shadow-lg w-[900px] max-h-[85vh] relative p-6"
    >
      <button
        @click="close"
        class="absolute top-3 right-3 text-gray-500 hover:text-gray-700 text-xl"
      >
        ✕
      </button>

      <h2 class="text-2xl font-bold mb-3 text-gray-800">
        {{ event?.title || "Chi tiết học phần" }}
      </h2>

      <div v-if="event">
        <!-- Course Information -->
        <div class="bg-gray-50 rounded-lg p-4 mb-6 space-y-2">
          <div class="grid grid-cols-2 gap-4">
            <p><strong>Mã học phần:</strong> {{ event.extendedProps?.courseCode }}</p>
            <p><strong>Giảng viên:</strong> {{ event.extendedProps?.teacher }}</p>
            <p><strong>Thời gian:</strong> {{ formatTime(event.start, event.end) }}</p>
          </div>
        </div>

        <div class="flex justify-between items-center mt-6 mb-4">
          <h3 class="text-lg font-semibold text-gray-800">Danh sách sinh viên tham dự</h3>
          <span v-if="!loadingStudents" class="text-sm text-gray-600 bg-blue-100 px-3 py-1 rounded-full">
            Tổng: {{ studentsList.length }} sinh viên
          </span>
        </div>

        <LoadingSpinner 
          v-if="loadingStudents"
          size="small"
          message="Đang tải danh sách sinh viên..."
          min-height="200px"
        />

        <div v-else-if="studentsList.length" class="">
          <DataTable
            title=""
            :data="studentsListWithIndex"
            :columns="studentsColumns"
            idKey="studentCode"
            :show-add-button="false"
            :hide-delete-button="true"
            :show-edit-button="false"
            max-height="40vh"
          />
        </div>

        <div v-else class="text-center text-gray-500 py-8">
          <p class="text-sm">Chưa có sinh viên tham dự học phần này.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, computed } from "vue";
import DataTable from "@/components/DataTable.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";

const props = defineProps({
  show: Boolean,
  event: Object,
});

const emit = defineEmits(["close"]);
function close() {
  emit("close");
}

// === Định dạng thời gian ===
function formatTime(start: Date, end: Date) {
  if (!start || !end) return "";
  const s = new Date(start).toLocaleTimeString("vi-VN", {
    hour: "2-digit",
    minute: "2-digit",
  });
  const e = new Date(end).toLocaleTimeString("vi-VN", {
    hour: "2-digit",
    minute: "2-digit",
  });
  return `${s} - ${e}`;
}

// === State ===
const loadingStudents = ref(false);
const studentsList = ref<any[]>([]);

// === DataTable configuration ===
const studentsColumns = [
  { label: "STT", field: "index" },
  { label: "Mã số", field: "studentCode" },
  { label: "Họ đệm", field: "lastName" },
  { label: "Tên", field: "firstName" }
];

// === Computed ===
const studentsListWithIndex = computed(() => {
  return studentsList.value.map((student, index) => ({
    ...student,
    index: index + 1
  }));
});

// === Hàm tải danh sách sinh viên ===
async function loadStudents() {
  const ev: any = props.event || {};
  console.debug("🧠 props.event nhận được:", ev);

  // ✅ Đảm bảo lấy đúng khóa ID từ sự kiện
  const courseClassId =
    ev.extendedProps?.courseClassId ||
    ev.extendedProps?.course_class_id ||
    ev.extendedProps?.id ||
    ev.id;

  if (!courseClassId) {
    console.warn("⚠️ Không có courseClassId để load danh sách sinh viên.");
    return;
  }

  loadingStudents.value = true;
  studentsList.value = [];

  try {
    const url = `http://localhost:8000/api/course_classes/${courseClassId}/students`;
    console.debug("📡 Gọi API:", url);

    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const data = await res.json();
    console.debug("✅ Dữ liệu sinh viên trả về:", data);

    studentsList.value = Array.isArray(data)
      ? data.map((item: any) => ({
          studentCode:
            item.student?.student_code || item.student?.studentCode || "-",
          firstName:
            item.student?.first_name || item.student?.firstName || "-",
          lastName: item.student?.last_name || item.student?.lastName || "-",
        }))
      : [];
  } catch (e) {
    console.error("❌ Lỗi khi tải danh sách sinh viên:", e);
  } finally {
    loadingStudents.value = false;
  }
}

// === Theo dõi props.event hoặc show để tự động load ===
watch(
  () => [props.event, props.show],
  ([ev, show]) => {
    if (show && ev) {
      loadStudents();
    }
  },
  { immediate: true }
);
</script>
