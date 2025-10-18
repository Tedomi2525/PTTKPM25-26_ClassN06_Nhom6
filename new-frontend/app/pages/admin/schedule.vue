<template>
  <div class="h-[95vh] w-full bg-gradient-to-br from-blue-50 to-cyan-50 overflow-hidden">
    <div class="h-full w-full px-4 py-3 lg:px-6 lg:py-4 flex flex-col">
      <LoadingSpinner v-if="isLoading" size="large" color="blue" message="Đang tải lịch học..."
        sub-message="Vui lòng đợi trong giây lát" full-height />

      <div v-else class="animate-fade-in flex-1 flex flex-col overflow-hidden">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-4 flex-1 overflow-hidden">
          <div class="hidden lg:block lg:col-span-1"></div>

          <div class="lg:col-span-2 flex flex-col gap-3 overflow-y-auto">
            <div class="flex items-start gap-2 mb-3 relative">
              <div class="flex-1 relative">
                <input v-model="inputId"
                       @input="handleInput"
                       @keydown.enter="checkSchedule"
                       type="text"
                       placeholder="Nhập mã (VD: SV25000001 hoặc GV25000001)"
                       class="w-full px-3 py-2 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400" />
                
                <ul v-if="suggestions.length"
                    class="absolute z-50 w-full bg-white border border-gray-200 rounded-lg shadow-xl mt-1 max-h-60 overflow-y-auto">
                  <li v-for="(suggestion, index) in suggestions"
                      :key="index"
                      @click="selectSuggestion(suggestion)"
                      class="px-3 py-2 cursor-pointer hover:bg-blue-50 transition-colors text-sm border-b border-gray-100 last:border-b-0">
                    <div class="font-medium text-gray-800">{{ suggestion.code }}</div>
                    <div class="text-xs text-gray-500">{{ suggestion.name }}</div>
                  </li>
                </ul>
              </div>

              <button @click="checkSchedule"
                      :disabled="isChecking"
                      class="flex-shrink-0 px-4 py-2 bg-[#09f] text-white rounded-xl hover:bg-[#0088dd] transition-all duration-200 font-medium disabled:opacity-50 disabled:cursor-not-allowed">
                <span v-if="isChecking">...</span>
                <span v-else>Kiểm tra</span>
              </button>
            </div>
            <div
              class="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden flex-shrink-0">
              <div class="bg-[#09f] px-4 py-2.5">
                <h3 class="text-base font-semibold text-white">
                  Chọn ngày
                </h3>
              </div>
              <div class="p-3">
                <div id="calendarPicker" class="w-full"></div>
              </div>

              <div class="px-3 pb-3">
                <div class="grid grid-cols-3 gap-2">
                  <button @click="goToPreviousWeek"
                    class="px-3 py-2.5 bg-gray-50 hover:bg-gray-100 text-gray-700 rounded-xl shadow-sm hover:shadow-md transition-all duration-200 flex items-center justify-center gap-1.5 font-medium"
                    title="Tuần trước">
                    <span class="text-lg">←</span>
                    <span class="hidden xl:inline text-sm">Trước</span>
                  </button>
                  <button @click="goToCurrentWeek"
                    class="px-3 py-2.5 bg-[#09f] hover:bg-[#0088dd] text-white rounded-xl shadow-md hover:shadow-lg transition-all duration-200 font-medium text-sm">
                    Hôm nay
                  </button>
                  <button @click="goToNextWeek"
                    class="px-3 py-2.5 bg-gray-50 hover:bg-gray-100 text-gray-700 rounded-xl shadow-sm hover:shadow-md transition-all duration-200 flex items-center justify-center gap-1.5 font-medium"
                    title="Tuần sau">
                    <span class="hidden xl:inline text-sm">Sau</span>
                    <span class="text-lg">→</span>
                  </button>
                </div>
              </div>
            </div>

            <div
              class="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden flex-shrink-0">
              <div class="bg-[#09f] px-4 py-2.5">
                <h4 class="text-base font-semibold text-white">
                  Thống kê tuần
                </h4>
              </div>
              <div class="p-3">
                <div class="space-y-2">
                  <div
                    class="flex justify-between items-center p-2 bg-[#09f]/10 rounded-lg hover:bg-[#09f]/15 transition-colors">
                    <span class="text-xs font-medium text-gray-700">Tổng số buổi học</span>
                    <span class="text-xl font-bold text-[#09f]">{{ totalClasses }}</span>
                  </div>
                  <div
                    class="flex justify-between items-center p-2 bg-[#09f]/10 rounded-lg hover:bg-[#09f]/15 transition-colors">
                    <span class="text-xs font-medium text-gray-700">Số môn học</span>
                    <span class="text-xl font-bold text-[#09f]">{{ uniqueCourses }}</span>
                  </div>
                  <div
                    class="flex justify-between items-center p-2 bg-[#09f]/10 rounded-lg hover:bg-[#09f]/15 transition-colors">
                    <span class="text-xs font-medium text-gray-700">Tổng số tiết</span>
                    <span class="text-xl font-bold text-[#09f]">{{ totalPeriods }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="lg:col-span-8 flex flex-col overflow-hidden">
            <div
              class="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden flex flex-col">
              <div class="bg-[#09f] px-4 py-2.5 flex-shrink-0">
                <h3 class="text-base font-semibold text-white">
                  Lịch học/Giảng dạy trong tuần
                  <span v-if="currentLoadedId" class="text-sm font-normal ml-3"> (Mã: {{ currentLoadedId }})</span>
                </h3>
              </div>
              <div class="p-3 flex-1 overflow-y-auto">
                <FullCalendar ref="calendarRef" :options="plainOptions" />
              </div>
            </div>
          </div>

          <SchedulePopup :show="showPopup" :event="selectedEvent" @close="showPopup = false" />
          <div class="hidden lg:block lg:col-span-1"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue"
import axios from "axios"
import FullCalendar from "@fullcalendar/vue3"
import type { CalendarApi } from '@fullcalendar/core'
import timeGridPlugin from "@fullcalendar/timegrid"
import interactionPlugin from "@fullcalendar/interaction"
import viLocale from "@fullcalendar/core/locales/vi"
import flatpickr from "flatpickr"
import "flatpickr/dist/flatpickr.css"
import { Vietnamese as vn } from "flatpickr/dist/l10n/vn.js"
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import SchedulePopup from "@/components/popup/schedule_popup.vue"

definePageMeta({
  layout: "default",
})

// === BIẾN STATE MỚI CHO AUTOSUGGEST ===
interface Suggestion {
  id: string; // studentId hoặc teacherId (dùng để gọi API load lịch)
  code: string; // Mã code (SVxxxxxx hoặc GVxxxxxx) (dùng để hiển thị)
  name: string; // Họ tên
  type: 'SV' | 'GV';
}
const suggestions = ref<Suggestion[]>([]);
let searchTimeout: NodeJS.Timeout | null = null;
// =======================================

const isLoading = ref(false)
const isChecking = ref(false)
const currentWeekStart = ref(getSundayOfWeek(new Date()))
const currentLoadedId = ref<string | null>(null)
const showPopup = ref(false)
const selectedEvent = ref<any>(null)
const inputId = ref("")

// Computed properties cho thống kê (Giữ nguyên)
const currentWeekDisplay = computed(() => {
  const start = new Date(currentWeekStart.value)
  const end = new Date(start)
  end.setDate(end.getDate() + 6)

  const formatDate = (d: Date) => {
    return `${String(d.getDate()).padStart(2, '0')}/${String(d.getMonth() + 1).padStart(2, '0')}`
  }

  return `Tuần ${formatDate(start)} - ${formatDate(end)}`
})

const totalClasses = computed(() => {
  return calendarOptions.value.events.length
})

const uniqueCourses = computed(() => {
  const courses = new Set(
    calendarOptions.value.events.map((event: any) => event.extendedProps?.courseCode)
  )
  return courses.size
})

const totalPeriods = computed(() => {
  return calendarOptions.value.events.reduce((total: number, event: any) => {
    // Mỗi ca học kéo dài 2h45p và bao gồm 3 tiết học
    const start = new Date(event.start)
    const end = new Date(event.end)
    const hours = (end.getTime() - start.getTime()) / (1000 * 60 * 60)

    // Nếu ca học kéo dài 2h45p (2.75 giờ) thì tính 3 tiết
    if (hours >= 2.5 && hours <= 3) {
      return total + 3
    }

    // Tính theo tỷ lệ cho các ca học khác (nếu có)
    return total + Math.ceil(hours / 0.92) // 2.75h / 3 tiết = 0.92h/tiết
  }, 0)
})

const calendarRef = ref<InstanceType<typeof FullCalendar> | null>(null)
const calendarOptions = ref({
  plugins: [timeGridPlugin, interactionPlugin],
  initialView: "timeGridWeek",
  locale: viLocale,
  slotMinTime: "06:00:00",
  slotMaxTime: "22:00:00",
  slotDuration: "00:30:00",
  slotLabelInterval: "01:00:00",
  headerToolbar: false as const,
  allDaySlot: false,
  firstDay: 0,
  height: "100%",
  expandRows: false,
  eventClick: (info: any) => {
    selectedEvent.value = {
      title: info.event.title,
      start: info.event.start,
      end: info.event.end,
      extendedProps: info.event.extendedProps,
      roomName: info.event.extendedProps.room,
      className: info.event.extendedProps.section,
    }
    showPopup.value = true
  },
  eventDidMount: (info: any) => {
    // Lấy phần tử chính của event
    const el = info.el.querySelector('.fc-event-main-frame') || info.el;

    // Cho phép hover + click
    el.style.cursor = 'pointer';
    el.style.pointerEvents = 'auto';
    el.style.transition = 'all 0.2s ease';
    el.style.borderRadius = '6px';
    el.style.position = 'relative';
    el.style.zIndex = '10';

    // Hiệu ứng hover
    el.addEventListener('mouseenter', () => {
      el.style.transform = 'scale(1.03)';
      el.style.boxShadow = '0 6px 15px rgba(0, 0, 0, 0.15)';
      el.style.zIndex = '999';
    });

    el.addEventListener('mouseleave', () => {
      el.style.transform = 'scale(1)';
      el.style.boxShadow = 'none';
      el.style.zIndex = '10';
    });

    // Bắt sự kiện click để mở popup
    el.addEventListener('click', () => {
      selectedEvent.value = {
        title: info.event.title,
        start: info.event.start,
        end: info.event.end,
        extendedProps: info.event.extendedProps,
        roomName: info.event.extendedProps.room,
        className: info.event.extendedProps.section,
      };
      showPopup.value = true;
    });
  },
  contentHeight: "auto",
  aspectRatio: 1.5,
  nowIndicator: true,
  now: new Date(),
  slotLabelFormat: {
    hour: "2-digit" as const,
    minute: "2-digit" as const,
    hour12: false,
  },
  dayHeaderContent: (arg: any) => {
    const date = arg.date
    const d = String(date.getDate()).padStart(2, "0")
    const m = String(date.getMonth() + 1).padStart(2, "0")
    const weekdays = ["Chủ nhật", "Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7"]
    const thu = weekdays[date.getDay()]
    return {
      html: `<div class="text-center">
               <div class="text-xs font-semibold text-gray-800">${thu}</div>
               <div class="text-lg font-bold text-gray-800">${d}/${m}</div>
             </div>`,
    }
  },
  eventContent: (arg: any) => {
    const { event } = arg
    const { teacher, courseCode, room } = event.extendedProps
    const subInfo = teacher ? `<div>${teacher}</div>` : ''
    const locationInfo = room ? `<div class="mt-1">${room}</div>` : ''

    return {
      html: `
      <div class="fc-event-main-frame p-2 transition-transform duration-200" title="${event.title} - ${courseCode}" tabindex="0">
        <div class="font-bold text-sm mb-1">${event.title.split(' - ')[0]}</div>
        <div class="text-xs opacity-90">
          ${subInfo}
          ${locationInfo}
        </div>
      </div>
    `
    }
  },

  events: [],
})

const plainOptions = computed(() => calendarOptions.value)

// === LOGIC AUTOSUGGEST ===

/**
 * Hàm tìm kiếm gợi ý từ API
 * @param query Mã sinh viên/giảng viên hoặc tên
 */
async function fetchSuggestions(query: string) {
  const q = query.trim().toUpperCase();
  if (q.length < 3) {
    suggestions.value = [];
    return;
  }

  try {
    let url = '';
    let isStudent = false;
    
    // Tự động tìm kiếm nếu query bắt đầu bằng SV hoặc GV
    if (q.startsWith('SV')) {
      url = `http://localhost:8000/api/students/search`;
      isStudent = true;
    } else if (q.startsWith('GV')) {
      url = `http://localhost:8000/api/teachers/search`;
      isStudent = false;
    } else {
      suggestions.value = [];
      return;
    }

    const res = await axios.get(url, { params: { q } });
    
    // Xử lý kết quả trả về:
    if (isStudent && Array.isArray(res.data)) {
        suggestions.value = res.data.map((item: any) => ({
            id: item.studentId,
            code: item.studentCode,
            name: item.full_name,
            type: 'SV',
        })).filter((s: Suggestion) => s.id && s.code).slice(0, 10);
    } else if (!isStudent && Array.isArray(res.data)) { // Giả định API giảng viên cũng trả về mảng
        suggestions.value = res.data.map((item: any) => ({
            id: item.teacherId,
            code: item.teacherCode,
            name: item.full_name,
            type: 'GV',
        })).filter((s: Suggestion) => s.id && s.code).slice(0, 10);
    } else if (!isStudent && res.data.teacherId) {
       // Xử lý trường hợp API giảng viên trả về 1 đối tượng duy nhất (như API cũ của bạn)
        suggestions.value = [{
            id: res.data.teacherId,
            code: res.data.teacherCode,
            name: res.data.full_name,
            type: 'GV',
        }].filter((s: Suggestion) => s.id && s.code);
    } 
    else {
        suggestions.value = [];
    }

  } catch (error) {
    console.error("Lỗi khi fetch gợi ý:", error);
    suggestions.value = [];
  }
}

/**
 * Xử lý sự kiện input với debounce (Giới hạn gọi API)
 */
function handleInput() {
  if (searchTimeout) {
    clearTimeout(searchTimeout);
  }
  searchTimeout = setTimeout(() => {
    fetchSuggestions(inputId.value);
  }, 300); // Debounce 300ms
}

/**
 * Xử lý khi người dùng chọn một gợi ý
 */
function selectSuggestion(suggestion: Suggestion) {
  inputId.value = suggestion.code; // Điền mã code vào ô input
  suggestions.value = []; // Đóng danh sách gợi ý
  // Tự động kiểm tra lịch sau khi chọn
  checkSchedule();
}
// =======================================

function formatDateToYYYYMMDD(date: Date) {
  const y = date.getFullYear()
  const m = String(date.getMonth() + 1).padStart(2, "0")
  const d = String(date.getDate()).padStart(2, "0")
  return `${y}-${m}-${d}`
}

function getSundayOfWeek(date: Date): Date {
  const day = date.getDay()
  const diff = date.getDate() - day
  const sunday = new Date(date)
  sunday.setDate(diff)
  sunday.setHours(0, 0, 0, 0)
  return sunday
}

// Hàm điều hướng tuần (Giữ nguyên)
function goToPreviousWeek() {
  const api = (calendarRef.value as any)?.getApi() as CalendarApi
  if (api) {
    api.prev()
    const newDate = api.getDate()
    currentWeekStart.value = getSundayOfWeek(new Date(newDate))
    loadScheduleForCurrentWeek()
  }
}

function goToCurrentWeek() {
  const api = (calendarRef.value as any)?.getApi() as CalendarApi
  if (api) {
    api.today()
    const today = new Date()
    currentWeekStart.value = getSundayOfWeek(today)
    loadScheduleForCurrentWeek()
  }
}

function goToNextWeek() {
  const api = (calendarRef.value as any)?.getApi() as CalendarApi
  if (api) {
    api.next()
    const newDate = api.getDate()
    currentWeekStart.value = getSundayOfWeek(new Date(newDate))
    loadScheduleForCurrentWeek()
  }
}

async function loadScheduleForCurrentWeek() {
  const id = currentLoadedId.value
  if (!id) return

  const sundayDate = formatDateToYYYYMMDD(currentWeekStart.value)
  if (id.toUpperCase().startsWith("SV")) {
    await loadStudentSchedule(id, sundayDate)
  } else if (id.toUpperCase().startsWith("GV")) {
    await loadTeacherSchedule(id, sundayDate)
  }
}

async function loadTeacherSchedule(teacherId: string, sundayDate: string) {
  if (!teacherId) {
    console.warn("❌ Teacher ID không hợp lệ")
    return
  }

  isChecking.value = true
  try {
    const res = await axios.get(`http://localhost:8000/api/teachers/weekly-schedule`, {
      params: { 
        teacher_id: teacherId,
        sunday_date: sundayDate
      },
    })

    if (res.data.success) {
      const schedules = res.data.data.schedules || []
      
      calendarOptions.value.events = schedules.map((item: any) => {
        const [day, month, year] = item.specific_date.split("/")
        const isoDate = `${year}-${month.padStart(2, "0")}-${day.padStart(2, "0")}`
        
        // Tạo màu sắc khác nhau cho từng môn học
        const courseColors = [
          { bg: "#3b82f6", border: "#2563eb" }, // Blue
          { bg: "#10b981", border: "#059669" }, // Green
          { bg: "#f59e0b", border: "#d97706" }, // Yellow
          { bg: "#ef4444", border: "#dc2626" }, // Red
          { bg: "#8b5cf6", border: "#7c3aed" }, // Purple
          { bg: "#06b6d4", border: "#0891b2" }, // Cyan
          { bg: "#ec4899", border: "#db2777" }, // Pink
          { bg: "#84cc16", border: "#65a30d" }, // Lime
        ]
        
        const colorIndex = item.course.course_id % courseColors.length
        const color = courseColors[colorIndex] || courseColors[0]
        
        return {
          title: `${item.course.course_name} (${item.course_class.section}) - ${item.room.room_name}`,
          start: `${isoDate}T${item.time.period_start.start_time}`,
          end: `${isoDate}T${item.time.period_start.end_time}`,
          backgroundColor: color?.bg || "#3b82f6",
          borderColor: color?.border || "#2563eb",
          textColor: "#fff",
          extendedProps: {
            room: item.room.room_name,
            courseCode: item.course.course_code,
            credits: item.course.credits,
            section: item.course_class.section,
            semester: item.semester?.semester_name || "N/A",
            studentCount: `${item.course_class.min_students}-${item.course_class.max_students}`,
            scheduleId: item.schedule_id,
            dayName: item.day_name
          },
        }
      })
      currentLoadedId.value = teacherId
    } else {
      console.warn("❌ API trả về không thành công:", res.data)
      calendarOptions.value.events = []
    }
  } catch (err: any) {
    console.error("❌ Lỗi khi tải lịch giảng dạy:", err)
    calendarOptions.value.events = []
    alert("Không tìm thấy lịch giảng dạy hoặc lỗi kết nối API.")
  } finally {
    isChecking.value = false
  }
}

async function loadStudentSchedule(studentId: string, sundayDate: string) {
  if (!studentId) {
    console.warn("❌ Student ID không hợp lệ")
    return
  }

  isChecking.value = true
  try {
    const res = await axios.get(`http://localhost:8000/api/students/${studentId}/schedule`, {
      params: { sunday_date: sundayDate },
    })

    if (res.data.success) {
      const schedules = res.data.data.schedules || []
      
      calendarOptions.value.events = schedules.map((item: any) => {
        const [day, month, year] = item.specific_date.split("/")
        const isoDate = `${year}-${month.padStart(2, "0")}-${day.padStart(2, "0")}`

        return {
          id: item.course_class.course_class_id,
          title: `${item.course.course_name} (${item.course_class.section}) - ${item.room.room_name}`,
          start: `${isoDate}T${item.time.period_start.start_time}`,
          end: `${isoDate}T${item.time.period_end.end_time}`,
          backgroundColor: "#09f",
          borderColor: "#0088dd",
          textColor: "#fff",
          extendedProps: {
            courseClassId: item.course_class.course_class_id,
            teacher: item.course_class.teacher.full_name,
            courseCode: item.course.course_code,
            credits: item.course.credits,
            students: item.course_class.students,
            section: item.course_class.section,
            room: item.room.room_name,
          },
        }
      })
      currentLoadedId.value = studentId

    } else {
      console.warn("❌ API trả về không thành công:", res.data)
      calendarOptions.value.events = []
    }
  } catch (err: any) {
    console.error("❌ Lỗi khi tải lịch học:", err)
    calendarOptions.value.events = []
    alert("Không tìm thấy lịch học hoặc lỗi kết nối API.")
  } finally {
    isChecking.value = false
  }
}

function initDatePicker() {
  flatpickr("#calendarPicker", {
    locale: vn,
    inline: true,
    dateFormat: "d/m/Y",
    onChange: async (selectedDates) => {
      if (!selectedDates.length || !currentLoadedId.value) return
      
      const selected = selectedDates[0]
      if (!selected) return

      const sundayOfWeek = getSundayOfWeek(new Date(selected))
      currentWeekStart.value = sundayOfWeek
      const sundayDate = formatDateToYYYYMMDD(sundayOfWeek)

      const idToLoad = currentLoadedId.value
      if (idToLoad.toUpperCase().startsWith("SV")) {
        await loadStudentSchedule(idToLoad, sundayDate)
      } else if (idToLoad.toUpperCase().startsWith("GV")) {
        await loadTeacherSchedule(idToLoad, sundayDate)
      }

      if (calendarRef.value) {
        const api = (calendarRef.value as any).getApi() as CalendarApi
        api.gotoDate(sundayOfWeek)
      }
    },
  })
}

// Hàm khởi tạo ban đầu, chỉ set ngày và date picker, không load dữ liệu
async function initComponent() {
  const today = new Date()
  const sundayOfCurrentWeek = getSundayOfWeek(new Date(today))
  currentWeekStart.value = sundayOfCurrentWeek

  initDatePicker()

  isLoading.value = false
}

async function checkSchedule() {
  const id = inputId.value.trim()
  if (!id) {
    alert("Vui lòng nhập mã sinh viên hoặc giảng viên")
    return
  }

  // Xóa danh sách gợi ý khi bắt đầu kiểm tra
  suggestions.value = [];
  
  isChecking.value = true
  isLoading.value = true
  const today = new Date()
  const sunday = getSundayOfWeek(today)
  const sundayDate = formatDateToYYYYMMDD(sunday)
  
  currentWeekStart.value = sunday 
  if (calendarRef.value) {
      const api = (calendarRef.value as any).getApi() as CalendarApi
      api.gotoDate(sunday)
  }

  try {
    let actualId = id
    console.log("🔍 Đang tìm kiếm mã:", id)
    
    if (id.toUpperCase().startsWith("SV")) {
      const res = await axios.get(`http://localhost:8000/api/students/search`, {
        params: { q: id }
      })
      const studentData = res.data[0]
      // 🔥 Thay vì dùng studentCode, ta cần dùng studentId để gọi API load schedule
      if (!studentData || !studentData.studentId) throw new Error("Không tìm thấy sinh viên với mã đã nhập")
      
      actualId = studentData.studentId
      await loadStudentSchedule(actualId, sundayDate)

    } else if (id.toUpperCase().startsWith("GV")) {
      const res = await axios.get(`http://localhost:8000/api/teachers/search`, {
        params: { q: id }
      })
      const teacherData = res.data
      // 🔥 Thay vì dùng teacherCode, ta cần dùng teacherId để gọi API load schedule
      if (!teacherData || !teacherData.teacherId) throw new Error("Không tìm thấy giảng viên với mã đã nhập")
      
      actualId = teacherData.teacherId
      await loadTeacherSchedule(actualId, sundayDate)
      
    } else {
      alert("Mã không hợp lệ. Vui lòng nhập mã sinh viên (SV...) hoặc giảng viên (GV...)")
      calendarOptions.value.events = []
      currentLoadedId.value = null
      isChecking.value = false
      isLoading.value = false
      return
    }
    
    currentLoadedId.value = actualId

  } catch (err: any) {
    console.error("❌ Lỗi khi tải TKB:", err.message || err)
    alert(err.message || "Không thể tải TKB. Kiểm tra lại mã hoặc API.")
    calendarOptions.value.events = []
    currentLoadedId.value = null
  } finally {
    isChecking.value = false
    isLoading.value = false
  }
}

onMounted(() => {
  initComponent()
})
</script>

<style>
/* Animation */
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.5s ease-out;
}

/* FullCalendar Customization */
.fc {
  font-family: inherit;
}

/* Grid */
.fc .fc-scrollgrid {
  border-radius: 12px;
  overflow: hidden;
  border: none !important;
}

.fc .fc-timegrid-slot {
  height: 30px !important;
  border-color: #e5e7eb !important;
}

/* Event styling */
.fc-event {
  border-radius: 8px !important;
  border-left-width: 4px !important;
  padding: 2px 4px !important;
  margin: 2px 4px !important;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
}

.fc-event:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
  z-index: 100 !important;
}

.fc-event-main {
  padding: 4px !important;
}

/* Force pointer events on inner event content and ensure it sits above overlays */
.fc-event,
.fc-event *,
.fc-event-main-frame {
  pointer-events: auto !important;
}

.fc-event {
  z-index: 50 !important;
}

.fc-event-main-frame {
  z-index: 60 !important;
}

/* Hover affordance for the inner event content */
.fc-event-main-frame.hovering {
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.15);
  z-index: 999 !important;
}


.fc-event-main-frame:focus {
  outline: 2px solid rgba(9, 132, 255, 0.25);
  outline-offset: 2px;
}

/* Helper class toggled by JS so hover styles can be applied even when :hover
   is not triggered due to stacking contexts/overlays. */
.fc-event-main-frame--hover {
  transform: translateY(-3px) scale(1.02) !important;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.12) !important;
}

/* Time labels */
.fc .fc-timegrid-axis {
  background: #f9fafb !important;
  font-weight: 600;
  color: #6b7280 !important;
}

.fc .fc-timegrid-slot-label {
  color: #6b7280 !important;
  font-size: 0.875rem;
  font-weight: 500;
}

/* Now indicator - dòng chỉ thời gian hiện tại */
.fc .fc-timegrid-now-indicator-line {
  border-color: #ef4444 !important;
  border-width: 3px !important;
  border-style: solid !important;
  box-shadow: 0 0 12px rgba(239, 68, 68, 0.6) !important;
  z-index: 10 !important;
}

.fc .fc-timegrid-now-indicator-arrow {
  border-color: #ef4444 !important;
  border-top-color: transparent !important;
  border-bottom-color: transparent !important;
  border-left-color: #ef4444 !important;
  border-width: 10px 0 10px 10px !important;
  margin-top: -10px !important;
}

.fc .fc-timegrid-now-indicator-container {
  /* z-index: 10 !important; */
}

/* Flatpickr customization */
.flatpickr-calendar {
  box-shadow: none !important;
  border: none !important;
  width: 100% !important;
}

.flatpickr-calendar .flatpickr-innerContainer {
  width: 100% !important;
}

.flatpickr-calendar .flatpickr-rContainer {
  width: 100% !important;
}

.flatpickr-calendar .flatpickr-days {
  width: 100% !important;
}

.flatpickr-calendar .dayContainer {
  width: 100% !important;
  min-width: 100% !important;
  max-width: 100% !important;
}

.flatpickr-day {
  max-width: none !important;
  height: 28px !important;
  line-height: 28px !important;
  flex-basis: 14.285% !important;
  width: 14.285% !important;
}

.flatpickr-months {
  background: #09f !important;
  color: white !important;
  border-radius: 12px 12px 0 0;
}

.flatpickr-current-month .flatpickr-monthDropdown-months {
  color: white !important;
  font-weight: 600;
  cursor: pointer !important;
  transition: all 0.2s ease !important;
}

.flatpickr-current-month .flatpickr-monthDropdown-months:hover {
  background: rgba(255, 255, 255, 0.3) !important;
  border-color: rgba(255, 255, 255, 0.5) !important;
}

.flatpickr-current-month .flatpickr-monthDropdown-months option {
  background: white !important;
  color: #374151 !important;
  padding: 4px !important;
}

.flatpickr-current-month .numInputWrapper {
  color: white !important;
  font-weight: 600;
}

.flatpickr-current-month .numInputWrapper input {
  color: white !important;
}

.flatpickr-current-month .numInputWrapper input:hover {
  background: rgba(255, 255, 255, 0.3) !important;
}

.flatpickr-weekdays {
  background: #f3f4f6 !important;
}

.flatpickr-weekday {
  font-size: 0.7rem !important;
  font-weight: 600 !important;
}

.flatpickr-day.selected {
  background: #09f !important;
  border-color: #09f !important;
  font-weight: 700 !important;
}

.flatpickr-day.today {
  border-color: #09f !important;
  background: #09f1 !important;
  color: #09f !important;
}

.flatpickr-day:hover {
  background: #09f2 !important;
  border-color: #09f !important;
}

/* Scrollbar styling */
.fc-scroller::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.fc-scroller::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 10px;
}

.fc-scroller::-webkit-scrollbar-thumb {
  background: #09f;
  border-radius: 10px;
}

.fc-scroller::-webkit-scrollbar-thumb:hover {
  background: #0088dd;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .fc-event {
    font-size: 0.75rem !important;
  }

  .fc .fc-col-header-cell {
    font-size: 0.75rem !important;
    padding: 6px 2px !important;
  }
}
</style>