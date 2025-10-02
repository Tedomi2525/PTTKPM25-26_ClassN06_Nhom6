<template>
  <div class="container mt-4">
    <div class="calendar-container">
      <!-- Lịch chính -->
      <FullCalendar ref="calendarRef" :options="calendarOptions" />

      <!-- Lịch nhỏ -->
      <div id="datepicker">
        <div class="datepicker-header">Chọn ngày</div>
        <div id="calendarPicker"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import FullCalendar from "@fullcalendar/vue3";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import viLocale from "@fullcalendar/core/locales/vi";

import flatpickr from "flatpickr";
import "flatpickr/dist/flatpickr.css";
import { Vietnamese as vn } from "flatpickr/dist/l10n/vn.js";

const calendarRef = ref(null);

const calendarOptions = {
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
    let weekdays = ["CN", "T2", "T3", "T4", "T5", "T6", "T7"];
    let thu = weekdays[date.getDay()];

    return {
      html: `<div style="text-align:center">
               <div>${d}/${m}</div>
               <small>${thu}</small>
             </div>`,
    };
  },
  events: [
    {
      title: "Phân tích & thiết kế hệ thống\nTiết 1-2\nPhòng A6-07\nGV: Cô Mai",
      start: "2025-09-08T06:45:00",
      end: "2025-09-08T09:25:00",
      color: "#1e88e5",
    },
    {
      title: "An toàn & bảo mật\nTiết 1-2\nPhòng A8-104\nGV: Thầy Ngữ",
      start: "2025-09-10T06:45:00",
      end: "2025-09-10T09:25:00",
      color: "#fb8c00",
    },
    {
      title: "Điện toán đám mây\nTiết 1-2\nPhòng A6-02\nGV: Thầy Phạm",
      start: "2025-09-11T06:45:00",
      end: "2025-09-11T09:25:00",
      color: "#e53935",
    },
    {
      title: "Tiếng Anh 2\nTiết 7-8\nPhòng A2-201\nGV: Cô Hằng",
      start: "2025-09-09T13:00:00",
      end: "2025-09-09T14:40:00",
      color: "#43a047",
    },
  ],
};

onMounted(() => {
  // Date Picker đồng bộ với calendar
  flatpickr("#calendarPicker", {
    inline: true,
    locale: vn,
    onChange: (selectedDates) => {
      if (selectedDates.length > 0 && calendarRef.value) {
        calendarRef.value.getApi().gotoDate(selectedDates[0]);
      }
    },
  });
});
</script>

<style scoped>
:root {
      --bg: #f0f3fa;
      --white: #fff;
      --blue-light: #e3f2fd;
      --blue-dark: #1e3a8a;
      --shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      --radius: 8px;
      --sp-1: 15px;
      --font-sm: 0.75rem;
      --font-md: 0.85rem;
      --font-lg: 1.25rem;
    }

    body {
      background: var(--bg);
    }

    /* layout 2 cột */
    .calendar-container {
      display: grid;
      grid-template-columns: 3fr 1fr;
      gap: 20px;
      align-items: start;
    }

    /* lịch chính */
    #calendar {
      background: var(--white);
      border-radius: var(--radius);
      padding: var(--sp-1);
      box-shadow: var(--shadow);
      width: 100%;
      overflow: hidden;
    }

    /* tiêu đề ngày (trên cùng của cột) */
    .fc-col-header-cell {
      background: var(--blue-light);
      color: var(--blue-dark);
      font-weight: 600;
      font-size: 0.9rem;
      padding: 6px 0;
      border: 1px solid #e0e0e0;
    }

    /* giờ bên trái */
    .fc-timegrid-slot-label {
      font-size: 0.8rem;
      color: #444;
      padding-right: 6px;
    }

    /* từng ô trong lịch */
    .fc-timegrid-slot {
      border-color: #f1f1f1;
    }

    /* event (môn học) */
    .fc-event {
      border-radius: 6px;
      padding: 4px 6px;
      font-size: 0.8rem;
      font-weight: 500;
      border: none;
      box-shadow: 0 1px 4px rgba(0, 0, 0, 0.15);
      color: #fff;
      transition: 0.2s ease-in-out;
    }

    /* chữ trong event */
    .fc-event-title {
      white-space: pre-line;
      line-height: 1.2;
    }

    /* hiệu ứng hover cho event */
    .fc-event:hover {
      opacity: 0.9;
      cursor: pointer;
      transform: scale(1.02);
    }

    /* dòng kẻ ngày hiện tại */
    .fc-day-today {
      background-color: rgba(30, 58, 138, 0.05) !important;
    }

    /* thanh trục giờ (GMT+7 custom) */
    .fc-timegrid-axis {
      background: #fafafa;
      border-right: 1px solid #e0e0e0;
    }

    /* lịch nhỏ */
    #datepicker {
      background: var(--blue-light);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      width: 100%;
      max-height: 300px;
      max-block-size: 290px;
      max-width: 310px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    /* header cho lịch nhỏ */
    #datepicker .datepicker-header {
      border-top-left-radius: 6px;
      border-top-right-radius: 6px;
      background: var(--blue-dark);
      color: #fff;
      padding: 6px 10px;
      font-weight: 600;
      font-size: 0.9rem;
      text-align: center;
      border-bottom: 1px solid rgba(255, 255, 255, 0.2);
      width: 100%;
    }

    /* container flatpickr */
    #datepicker .flatpickr-calendar {
      box-shadow: none;
      border: none;
      margin: 0 auto;
      transform: scale(0.85);
      transform-origin: top center;
      font-size: 14px;
    }

    /* fullcalendar custom */
    .fc-toolbar-title {
      font-size: var(--font-lg);
      font-weight: 700;
    }

    .fc-timegrid-slot-label {
      font-size: var(--font-md);
    }
</style>
