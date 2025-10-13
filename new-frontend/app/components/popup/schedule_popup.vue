<template>
    <div v-if="show"
        class="fixed inset-0 bg-black/50 backdrop-blur-md flex justify-center items-center z-50 transition-all duration-300"
        @click.self="close">
        <div class="bg-white rounded-lg shadow-lg w-[800px] max-h-[80vh] overflow-y-auto relative p-6">
            <button @click="close" class="absolute top-3 right-3 text-gray-500 hover:text-gray-700 text-xl">
                ✕
            </button>

            <h2 class="text-2xl font-bold mb-3 text-gray-800">
                {{ event?.title || 'Chi tiết học phần' }}
            </h2>

            <div v-if="event">
                <p><strong>Mã học phần:</strong> {{ event.extendedProps.courseCode }}</p>
                <p><strong>Giảng viên:</strong> {{ event.extendedProps.teacher }}</p>
                <p><strong>Số tín chỉ:</strong> {{ event.extendedProps.credits }}</p>
                <p><strong>Thời gian:</strong> {{ formatTime(event.start, event.end) }}</p>

                <h3 class="font-semibold mt-4 mb-2">Danh sách sinh viên tham dự:</h3>
                <div v-if="loadingStudents" class="text-sm text-gray-600">Đang tải danh sách sinh viên...</div>
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
                            <tr v-for="(s, idx) in studentsList" :key="s.original?.id || s.studentCode || idx" class="even:bg-gray-50">
                                <td class="px-3 py-2 border">{{ idx + 1 }}</td>
                                <td class="px-3 py-2 border">{{ s.studentCode || '-' }}</td>
                                <td class="px-3 py-2 border">{{ s.lastName || '-' }}</td>
                                <td class="px-3 py-2 border">{{ s.firstName || '-' }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div v-else class="text-sm text-gray-600">Chưa có sinh viên tham dự.</div>
                <!-- Debug helper: show extendedProps when no students detected -->
                <div v-if="!studentsList.length" class="mt-3 text-xs text-gray-500">
                    <div>Không tìm thấy danh sách sinh viên. Dữ liệu raw (extendedProps):</div>
                    <pre class="max-h-40 overflow-auto bg-gray-50 p-2 rounded text-xs">{{ rawExtendedPropsPreview }}</pre>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'

const props = defineProps({
    show: Boolean,
    event: Object,
})

const emit = defineEmits(['close'])

function close() {
    emit('close')
}

function formatTime(start: Date, end: Date) {
    if (!start || !end) return ''
    const s = new Date(start).toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
    const e = new Date(end).toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
    return `${s} - ${e}`
}

const fetchedArr = ref<any[]>([])
const loadingStudents = ref(false)
const studentsCache = ref<Record<string, any>>({})

// Normalize students/enrollments into objects with studentCode, firstName, lastName
const studentsList = computed(() => {
    const ev: any = props.event || {}
    const candidates = [
        // first prefer fetchedArr from backend if available
        fetchedArr.value,
        ev.extendedProps?.students,
        ev.extendedProps?.attendees,
        ev.students,
        ev.attendees,
        ev.extendedProps?.participants,
        ev.extendedProps?.enrollments,
        ev.enrollments,
    ]

    let arr: any[] = []
    for (const c of candidates) {
        if (Array.isArray(c)) {
            arr = c
            break
        }
    }

    // fallback: try to parse a JSON string stored on extendedProps
    if (!arr.length) {
        try {
            const maybe = ev.extendedProps?.studentsJson || ev.extendedProps?.students_list
            if (typeof maybe === 'string') {
                const parsed = JSON.parse(maybe)
                if (Array.isArray(parsed)) arr = parsed
            }
        } catch (e) {
            // ignore
        }
    }

    // debug: print candidates and event to console to inspect structure
    try {
        console.debug('schedule_popup: event:', ev)
        console.debug('schedule_popup: candidate array length', arr.length)
    } catch (e) {
        // ignore
    }

    // map/normalize each entry to { studentCode, firstName, lastName }
    return arr.map((item: any) => {
        // if item is an enrollment object with nested student
        const studentNested = item.student || item.sinhvien || item.user || item.profile || null

        // student id may be stored as student_id or studentId
        const studentId = item.student_id || item.studentId || (studentNested && (studentNested.studentId || studentNested.id))

        // try to find full student record from cache when we have an id
        let studentObj: any = null
        if (studentId) {
            studentObj = studentsCache.value[String(studentId)] || studentNested
        } else if (studentNested) {
            studentObj = studentNested
        }

        if (studentObj) {
            const code = studentObj.studentCode || studentObj.student_code || studentObj.code || studentObj.ma || null
            const firstName = studentObj.firstName || studentObj.first_name || studentObj.ten || ''
            const lastName = studentObj.lastName || studentObj.last_name || studentObj.ho || studentObj.familyName || ''
            return {
                original: item,
                studentCode: code,
                firstName: firstName,
                lastName: lastName
            }
        }

        // fallback: enrollment may directly contain name/code
        const code = item.student_code || item.studentCode || item.code || item.ma || null
        const firstName = item.first_name || item.firstName || item.ten || ''
        const lastName = item.last_name || item.lastName || item.ho || item.familyName || ''
        return {
            original: item,
            studentCode: code,
            firstName: firstName,
            lastName: lastName
        }
    })
})

async function loadEnrollments() {
    const ev: any = props.event || {}
    if (!ev) return

    // if we already have students from event or fetchedArr filled, skip
    const hasInline = Array.isArray(ev.extendedProps?.students) || Array.isArray(ev.students) || Array.isArray(ev.extendedProps?.enrollments) || Array.isArray(ev.enrollments)
    if (hasInline || fetchedArr.value.length) return

    // try to infer courseClassId from event
    // try multiple strategies: by class id first, then by courseCode
    const courseClassId = ev.extendedProps?.courseClassId || ev.extendedProps?.courseClass?.id || ev.extendedProps?.id || ev.id || ev.extendedProps?.classId
    const courseCode = ev.extendedProps?.courseCode || ev.extendedProps?.code || ev.courseCode || ev.code

    const queries: Array<{ name: string; value: any }> = []
    if (courseClassId) queries.push({ name: 'courseClassId', value: courseClassId })
    if (courseCode) {
        queries.push({ name: 'courseCode', value: courseCode })
        queries.push({ name: 'course_code', value: courseCode })
        queries.push({ name: 'code', value: courseCode })
    }

    if (!queries.length) return

    loadingStudents.value = true
    try {
        for (const q of queries) {
            try {
                    // If querying by course code, the enrollments endpoint may not accept it (422).
                    // Instead, try to resolve course classes by code and then fetch enrollments by class id.
                    if (q.name === 'courseCode' || q.name === 'course_code' || q.name === 'code') {
                        try {
                            const clsUrl = `http://localhost:8000/api/course_classes?code=${encodeURIComponent(q.value)}`
                            const clsRes = await fetch(clsUrl)
                            if (!clsRes.ok) {
                                console.debug('schedule_popup: fetch course_classes failed', clsUrl, clsRes.status)
                                continue
                            }
                            const classes = await clsRes.json()
                            if (Array.isArray(classes) && classes.length) {
                                // for each class, fetch enrollments by class id and aggregate
                                const allEnrollments: any[] = []
                                for (const cls of classes) {
                                    const id = cls.courseClassId || cls.id || cls.course_class_id || cls.course_classId
                                    if (!id) continue
                                    try {
                                        const eUrl = `http://localhost:8000/api/enrollments?courseClassId=${encodeURIComponent(id)}`
                                        const eRes = await fetch(eUrl)
                                        if (!eRes.ok) continue
                                        const eData = await eRes.json()
                                        if (Array.isArray(eData) && eData.length) allEnrollments.push(...eData)
                                    } catch (ie) {
                                        console.debug('schedule_popup: error fetching enrollments for class', id, ie)
                                        continue
                                    }
                                }
                                if (allEnrollments.length) {
                                    fetchedArr.value = allEnrollments
                                    console.debug('schedule_popup: fetched enrollments aggregated count', allEnrollments.length)
                                    break
                                }
                            }
                        } catch (cErr) {
                            console.debug('schedule_popup: error resolving course classes', cErr)
                            continue
                        }
                    } else {
                        const url = `http://localhost:8000/api/enrollments?${q.name}=${encodeURIComponent(q.value)}`
                        const res = await fetch(url)
                        if (!res.ok) {
                            console.debug('schedule_popup: fetch enrollments failed', url, res.status)
                            continue
                        }
                        const data = await res.json()
                        if (Array.isArray(data) && data.length) {
                            fetchedArr.value = data
                            console.debug('schedule_popup: fetched enrollments count', data.length, 'via', q.name)
                            break
                        }
                    }
            } catch (inner) {
                console.debug('schedule_popup: inner fetch error', inner)
                continue
            }
        }
    } catch (e) {
        console.debug('schedule_popup: error fetching enrollments', e)
    } finally {
        loadingStudents.value = false
    }
}

// If enrollments include student_id/studentId, fetch students and build a lookup map
async function ensureStudentsLoadedForEnrollments() {
    // check enrollments array
    const arr = fetchedArr.value.length ? fetchedArr.value : []
    if (!arr.length) return

    // detect if entries have student_id
    const hasStudentId = arr.some(a => a.student_id || a.studentId || (a.student && (a.student.id || a.student.studentId)))
    if (!hasStudentId) return

    try {
        // collect unique student ids from enrollments
        const idsSet = new Set<string>()
        for (const a of arr) {
            const sid = a.student_id || a.studentId || (a.student && (a.student.id || a.student.studentId))
            if (sid != null) idsSet.add(String(sid))
        }

        const ids = Array.from(idsSet)
        let data: any[] | null = null

        if (ids.length) {
            // try fetching only needed students
            try {
                const url = `http://localhost:8000/api/students?ids=${encodeURIComponent(ids.join(','))}`
                const res = await fetch(url)
                if (res.ok) {
                    const body = await res.json()
                    if (Array.isArray(body)) data = body
                } else {
                    console.debug('schedule_popup: filtered students fetch failed', url, res.status)
                }
            } catch (e) {
                console.debug('schedule_popup: error fetching filtered students', e)
            }
        }

        // fallback to full list if filtered fetch not available/returned nothing
        if (!data) {
            const resAll = await fetch('http://localhost:8000/api/students')
            if (!resAll.ok) {
                console.debug('schedule_popup: fetch students list failed', resAll.status)
                return
            }
            const allBody = await resAll.json()
            if (!Array.isArray(allBody)) return
            data = allBody
        }

        // build map by studentId and also by studentCode for convenience
        const map: Record<string, any> = {}
        for (const s of data) {
            if (s.studentId) map[String(s.studentId)] = s
            if (s.id) map[String(s.id)] = s
            if (s.studentCode) map[String(s.studentCode)] = s
        }
        studentsCache.value = map
    } catch (e) {
        console.debug('schedule_popup: error fetching students', e)
    }
}

// watch fetchedArr to load student details when enrollments arrive
watch(fetchedArr, (nv) => {
    if (nv && nv.length) {
        ensureStudentsLoadedForEnrollments()
    }
})

// watch for event changes and try to load students when popup opens
watch(() => props.event, (nv) => {
    if (nv) loadEnrollments()
})

const rawExtendedPropsPreview = computed(() => {
    try {
        return JSON.stringify(props.event?.extendedProps || props.event || {}, null, 2)
    } catch (e) {
        return String(props.event?.extendedProps || props.event || '')
    }
})

</script>
