<template>
  <div class="container mx-auto mt-4">
    <div class="grid grid-cols-4 gap-6 items-start">
      <!-- 📅 Lịch học chính -->
      <div class="col-span-3 bg-white rounded-lg shadow p-3">
        <FullCalendar ref="calendarRef" :options="calendarOptions" />
      </div>

      <!-- 🗓️ Lịch chọn ngày -->
      <div
        id="datepicker"
        class="bg-blue-100 rounded-lg shadow max-h-[320px] max-w-[310px] flex flex-col items-center"
      >
        <div
          class="w-full bg-blue-900 text-white font-semibold text-sm text-center px-3 py-2 rounded-t-lg border-b border-white/20"
        >
          Chọn ngày trong tuần
        </div>
        <div id="calendarPicker" class="scale-90 origin-top"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import FullCalendar from "@fullcalendar/vue3";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import viLocale from "@fullcalendar/core/locales/vi";
import flatpickr from "flatpickr";
import "flatpickr/dist/flatpickr.css";
import { Vietnamese as vn } from "flatpickr/dist/l10n/vn.js";
import { useAuth } from "@/composables/useAuth"; // import composable auth

const { schoolId } = useAuth(); // 👈 reactive schoolId / studentId

const calendarRef = ref(null);

// 🧩 Tuỳ chỉnh lịch hiển thị
const calendarOptions = ref({
  plugins: [timeGridPlugin, interactionPlugin],
  initialView: "timeGridWeek",
  locale: viLocale,
  slotMinTime: "06:00:00",
  slotMaxTime: "22:00:00",
  headerToolbar: false,
  allDaySlot: false,
  firstDay: 0,
  height: "auto",
  expandRows: true,
  slotLabelFormat: {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  },
  dayHeaderContent: (arg) => {
    const date = arg.date;
    const d = String(date.getDate()).padStart(2, "0");
    const m = String(date.getMonth() + 1).padStart(2, "0");
    const y = date.getFullYear();
    const weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    const thu = weekdays[date.getDay()];

    return {
      html: `<div class="text-center">
               <div>${d}/${m}/${y}</div>
               <small>${thu}</small>
             </div>`,
    };
  },
  events: [],
});

// 🔹 Hàm chuyển ngày sang format YYYY-MM-DD
const formatDateToYYYYMMDD = (date) => {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
};

// 🔹 Hàm tìm ngày Chủ nhật của tuần chứa ngày được chọn
const getSundayOfWeek = (date) => {
  const day = date.getDay(); // 0 = Sunday, 1 = Monday, ..., 6 = Saturday
  const diff = date.getDate() - day; // Số ngày cần trừ để về Chủ nhật
  const sunday = new Date(date.setDate(diff));
  return sunday;
};

const loadStudentSchedule = async (studentId, sundayDate) => {
  if (!studentId) {
    console.warn("❌ Student ID không hợp lệ");
    return;
  }

  try {
    console.log(`🔄 Đang tải lịch học cho sinh viên ${studentId}, tuần bắt đầu: ${sundayDate}`);
    
    const res = await axios.get(
      `http://localhost:8000/api/students/${studentId}/schedule`,
      { params: { sunday_date: sundayDate } }
    );

    if (res.data.success) {
      console.log("✅ Lịch học tải về:", res.data);

      const schedules = res.data.data.schedules || [];
      
      if (schedules.length === 0) {
        console.log("📭 Không có lịch học cho tuần này");
        calendarOptions.value.events = [];
        return;
      }

      calendarOptions.value.events = schedules.map((item) => {
        // 🔹 Chuyển đổi từ DD/MM/YYYY sang YYYY-MM-DD cho FullCalendar
        const [day, month, year] = item.specific_date.split('/');
        const isoDate = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
        
        console.log(`📚 Môn học: ${item.course.course_name} - Ngày: ${item.specific_date} -> ${isoDate}`);
        
        return {
          title: `${item.course.course_name} (${item.course_class.section}) - ${item.room.room_name}`,
          start: `${isoDate}T${item.time.period_start.start_time}`,
          end: `${isoDate}T${item.time.period_end.end_time}`,
          backgroundColor: "#2563eb",
          borderColor: "#1e40af",
          textColor: "#fff",
          extendedProps: {
            teacher: item.course_class.teacher.full_name,
            courseCode: item.course.course_code,
            credits: item.course.credits,
          },
        };
      });
    } else {
      console.warn("❌ API trả về không thành công:", res.data);
      calendarOptions.value.events = [];
    }
  } catch (err) {
    console.error("❌ Lỗi khi tải lịch học:", err);
    if (err.response) {
      console.error("Response data:", err.response.data);
      console.error("Response status:", err.response.status);
    }
    calendarOptions.value.events = [];
  }
};


// 🔹 Khởi tạo Flatpickr chọn ngày
const initDatePicker = (studentId) => {
  flatpickr("#calendarPicker", {
    locale: vn,
    inline: true,
    dateFormat: "d/m/Y",
    onChange: async (selectedDates) => {
      if (!selectedDates.length) return;
      const selected = selectedDates[0];
      
      // 🔹 Tìm ngày Chủ nhật của tuần chứa ngày được chọn
      const sundayOfWeek = getSundayOfWeek(new Date(selected));
      const sundayDate = formatDateToYYYYMMDD(sundayOfWeek); // ✅ YYYY-MM-DD format của Chủ nhật
      
      console.log(`📅 Ngày được chọn: ${selected.toLocaleDateString('vi-VN')}`);
      console.log(`📅 Chủ nhật của tuần: ${sundayOfWeek.toLocaleDateString('vi-VN')}`);
      console.log(`📅 Sunday date gửi API: ${sundayDate}`);
      
      await loadStudentSchedule(studentId, sundayDate);

      // Di chuyển lịch chính tới ngày Chủ nhật của tuần
      if (calendarRef.value) {
        const api = calendarRef.value.getApi();
        api.gotoDate(sundayOfWeek);
      }
    },
  });
};

// 🚀 Khi component mount
onMounted(async () => {
  const studentId = schoolId.value || localStorage.getItem("schoolId"); // fallback từ localStorage
  
  // 🔹 Tìm Chủ nhật của tuần hiện tại thay vì ngày hiện tại
  const today = new Date();
  const sundayOfCurrentWeek = getSundayOfWeek(new Date(today));
  const sundayDate = formatDateToYYYYMMDD(sundayOfCurrentWeek);
  
  console.log(`📅 Hôm nay: ${today.toLocaleDateString('vi-VN')}`);
  console.log(`📅 Chủ nhật tuần hiện tại: ${sundayOfCurrentWeek.toLocaleDateString('vi-VN')}`);
  console.log(`📅 Sunday date khởi tạo: ${sundayDate}`);

  await loadStudentSchedule(studentId, sundayDate);
  initDatePicker(studentId);
});
</script>
