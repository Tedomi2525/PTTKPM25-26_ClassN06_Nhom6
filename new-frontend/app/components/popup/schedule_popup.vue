<template>
  <div
    v-if="show"
    class="fixed inset-0 bg-black/50 backdrop-blur-md flex justify-center items-center z-50 transition-all duration-300"
    @click.self="close"
  >
    <div
      class="bg-white rounded-lg shadow-lg w-[800px] max-h-[80vh] overflow-y-auto relative p-6"
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
        <p><strong>Mã học phần:</strong> {{ event.extendedProps?.courseCode }}</p>
        <p><strong>Giảng viên:</strong> {{ event.extendedProps?.teacher }}</p>
        <p><strong>Số tín chỉ:</strong> {{ event.extendedProps?.credits }}</p>
        <p><strong>Thời gian:</strong> {{ formatTime(event.start, event.end) }}</p>

        <h3 class="font-semibold mt-4 mb-2">Danh sách sinh viên tham dự:</h3>

        <div v-if="loadingStudents" class="text-sm text-gray-600">
          Đang tải danh sách sinh viên...
        </div>

        <div v-else-if="studentsList.length">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-gray-100">
                <th class="px-3 py-2 border">STT</th>
                <th class="px-3 py-2 border">Mã số</th>
                <th class="px-3 py-2 border">Họ đệm</th>
                <th class="px-3 py-2 border">Tên</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(s, idx) in studentsList"
                :key="idx"
                class="even:bg-gray-50"
              >
                <td class="px-3 py-2 border">{{ idx + 1 }}</td>
                <td class="px-3 py-2 border">{{ s.studentCode }}</td>
                <td class="px-3 py-2 border">{{ s.lastName }}</td>
                <td class="px-3 py-2 border">{{ s.firstName }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-else class="text-sm text-gray-600">
          Chưa có sinh viên tham dự.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from "vue";

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
