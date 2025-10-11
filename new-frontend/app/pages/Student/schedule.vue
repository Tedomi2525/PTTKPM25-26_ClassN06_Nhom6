<template>
  <div class="container mx-auto mt-4 px-4">
    <!-- Loading state -->
    <div v-if="isLoading" class="flex justify-center items-center min-h-[500px]">
      <div class="text-center">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">Đang tải lịch học...</p>
      </div>
    </div>

    <!-- Content khi đã load xong -->
    <div v-else class="flex flex-col lg:grid lg:grid-cols-4 gap-6 items-start w-full">
      <!-- 🗓️ Lịch chọn ngày - Mobile first -->
      <div
        id="datepicker"
        class="order-1 lg:order-2 lg:col-span-1 bg-blue-100 rounded-lg shadow w-full max-w-[310px] mx-auto lg:mx-0 flex flex-col items-center"
      >
        <div id="calendarPicker" class="scale-90 origin-top w-full"></div>
      </div>

      <!-- 📅 Lịch học chính -->
      <div class="order-2 lg:order-1 lg:col-span-3 bg-white rounded-lg shadow p-2 sm:p-3 w-full min-h-[400px] lg:min-h-[500px]">
        <FullCalendar ref="calendarRef" :options="calendarOptions" />
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted, watch } from "vue"
import axios from "axios"
import FullCalendar from "@fullcalendar/vue3"
import type { CalendarApi } from '@fullcalendar/core'
import timeGridPlugin from "@fullcalendar/timegrid"
import interactionPlugin from "@fullcalendar/interaction"
import viLocale from "@fullcalendar/core/locales/vi"
import flatpickr from "flatpickr"
import "flatpickr/dist/flatpickr.css"
import { Vietnamese as vn } from "flatpickr/dist/l10n/vn.js"
import { useAuth } from "@/composables/useAuth"


definePageMeta({
  layout: "default",
})

const { schoolId, initAuth, isChecking } = useAuth()
const isLoading = ref(true)

const calendarRef = ref<InstanceType<typeof FullCalendar> | null>(null)
const calendarOptions = ref({
  plugins: [timeGridPlugin, interactionPlugin],
  initialView: "timeGridWeek",
  locale: viLocale,
  slotMinTime: "06:00:00",
  slotMaxTime: "22:00:00",
  headerToolbar: false as const,
  allDaySlot: false,
  firstDay: 0,
  height: "85vh",
  expandRows: true,
  slotLabelFormat: {
    hour: "2-digit" as const,
    minute: "2-digit" as const,
    hour12: false,
  },
  dayHeaderContent: (arg: any) => {
    const date = arg.date
    const d = String(date.getDate()).padStart(2, "0")
    const m = String(date.getMonth() + 1).padStart(2, "0")
    const y = date.getFullYear()
    const weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    const thu = weekdays[date.getDay()]
    return {
      html: `<div class="text-center">
               <div>${d}/${m}/${y}</div>
               <small>${thu}</small>
             </div>`,
    }
  },
  events: [],
})

function formatDateToYYYYMMDD(date: Date) {
  const y = date.getFullYear()
  const m = String(date.getMonth() + 1).padStart(2, "0")
  const d = String(date.getDate()).padStart(2, "0")
  return `${y}-${m}-${d}`
}

function getSundayOfWeek(date: Date) {
  const day = date.getDay()
  const diff = date.getDate() - day
  const sunday = new Date(date.setDate(diff))
  return sunday
}

async function loadStudentSchedule(studentId: string, sundayDate: string) {
  if (!studentId) {
    console.warn("❌ Student ID không hợp lệ")
    return
  }

  try {
    const res = await axios.get(`http://localhost:8000/api/students/${studentId}/schedule`, {
      params: { sunday_date: sundayDate },
    })

    if (res.data.success) {
      const schedules = res.data.data.schedules || []
      if (!schedules.length) {
        calendarOptions.value.events = []
        return
      }

      calendarOptions.value.events = schedules.map((item: any) => {
        const [day, month, year] = item.specific_date.split("/")
        const isoDate = `${year}-${month.padStart(2, "0")}-${day.padStart(2, "0")}`
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
        }
      })
    } else {
      console.warn("❌ API trả về không thành công:", res.data)
      calendarOptions.value.events = []
    }
  } catch (err: any) {
    console.error("❌ Lỗi khi tải lịch học:", err)
    calendarOptions.value.events = []
  }
}

function initDatePicker(studentId: string) {
  flatpickr("#calendarPicker", {
    locale: vn,
    inline: true,
    dateFormat: "d/m/Y",
    onChange: async (selectedDates) => {
      if (!selectedDates.length) return
      const selected = selectedDates[0]
      if (!selected) return
      const sundayOfWeek = getSundayOfWeek(new Date(selected))
      const sundayDate = formatDateToYYYYMMDD(sundayOfWeek)
      await loadStudentSchedule(studentId, sundayDate)
      if (calendarRef.value) {
        const api = (calendarRef.value as any).getApi() as CalendarApi
        api.gotoDate(sundayOfWeek)
      }
    },
  })
}

// Hàm khởi tạo lịch học
async function initSchedule() {
  const studentId = schoolId.value || localStorage.getItem("schoolId")
  if (!studentId) {
    console.error("❌ Không tìm thấy student ID")
    isLoading.value = false
    return
  }
  
  console.log("📅 Đang tải lịch học cho student:", studentId)
  
  const today = new Date()
  const sundayOfCurrentWeek = getSundayOfWeek(new Date(today))
  const sundayDate = formatDateToYYYYMMDD(sundayOfCurrentWeek)
  
  // Load lịch học
  await loadStudentSchedule(studentId, sundayDate)
  
  // Khởi tạo date picker
  initDatePicker(studentId)
  
  isLoading.value = false
}

// Watch schoolId để tự động load khi có dữ liệu
watch(schoolId, (newId) => {
  if (newId && !isChecking.value) {
    console.log("✅ School ID đã sẵn sàng:", newId)
    initSchedule()
  }
}, { immediate: true })

onMounted(async () => {
  // Đảm bảo auth đã được khởi tạo
  if (!schoolId.value) {
    console.log("🔄 Đang khởi tạo auth...")
    await initAuth()
  }
  
  // Nếu đã có schoolId, load ngay
  if (schoolId.value) {
    await initSchedule()
  }
})
</script>
