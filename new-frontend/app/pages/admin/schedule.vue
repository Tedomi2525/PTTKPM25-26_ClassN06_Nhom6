<template>
  <div class="container mx-auto mt-4">
    <div class="grid grid-cols-4 gap-6 items-start">
      <!-- Lịch chính -->
      <div class="col-span-3 bg-white rounded-lg">
        <FullCalendar ref="calendarRef" :options="calendarOptions" />
      </div>

      <!-- Lịch nhỏ -->
      <div
        id="datepicker"
        class="bg-blue-100 rounded-lg shadow max-h-[300px] max-w-[310px] flex flex-col items-center"
      >
        <div
          class="w-full bg-blue-900 text-white font-semibold text-sm text-center px-3 py-2 rounded-t-lg border-b border-white/20"
        >
          Chọn ngày
        </div>
        <div id="calendarPicker" class="scale-90 origin-top"></div>
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
};

onMounted(() => {
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
