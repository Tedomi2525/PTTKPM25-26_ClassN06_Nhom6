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
          Chọn ngày (chủ nhật của tuần)
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
    let date = arg.date;
    let d = String(date.getDate()).padStart(2, "0");
    let m = String(date.getMonth() + 1).padStart(2, "0");
    let y = date.getFullYear();
    let weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    let thu = weekdays[date.getDay()];

    return {
      html: `<div class="text-center">
               <div>${d}/${m}/${y}</div>
               <small>${thu}</small>
             </div>`,
    };
  },
  events: [],
});

// 🧠 Hàm gọi API lấy lịch học sinh viên
const loadStudentSchedule = async (studentId, sundayDate) => {
  try {
    const res = await axios.get(
      "http://localhost:8000/api/students/weekly-schedule",
      {
        params: {
          student_id: studentId,
          sunday_date: sundayDate, // dạng 05/10/2025 hoặc 2025-10-05 đều được
        },
      }
    );

    if (res.data.success) {
      const schedules = res.data.data.schedules || [];

      // 🗓️ Chuyển đổi dữ liệu API thành event cho FullCalendar
      calendarOptions.value.events = schedules.map((item) => ({
        title: `${item.course_name} (${item.room_name})`,
        start: item.start_time,
        end: item.end_time,
        backgroundColor: "#2563eb",
        borderColor: "#1e40af",
        textColor: "#fff",
      }));
    } else {
      console.warn("Không có lịch học cho tuần này.");
      calendarOptions.value.events = [];
    }
  } catch (err) {
    console.error("❌ Lỗi khi tải lịch học:", err);
  }
};

const initDatePicker = (studentId) => {
  flatpickr("#calendarPicker", {
    locale: vn,
    inline: true,
    dateFormat: "d/m/Y",
    onChange: async (selectedDates) => {
      if (selectedDates.length > 0) {
        const selected = selectedDates[0];
        const sundayDate = selected.toLocaleDateString("vi-VN"); // 05/10/2025
        await loadStudentSchedule(studentId, sundayDate);

        // Di chuyển lịch chính tới ngày được chọn
        if (calendarRef.value) {
          const api = calendarRef.value.getApi();
          api.gotoDate(selected);
        }
      }
    },
  });
};

// 🚀 Khi component được mount
onMounted(async () => {
  const studentId = 5;
  const sundayDate = "05/10/2025";

  await loadStudentSchedule(studentId, sundayDate);
  initDatePicker(studentId);
});
</script>
