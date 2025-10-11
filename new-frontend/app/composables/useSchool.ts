import { ref } from 'vue'
import axios from 'axios'

export interface Student {
  id: number
  studentCode: string
  firstName: string
  lastName: string
  fullName: string
  dob: string | null
  gender: string
  email: string
  phone: string | null
  className: string | null
  trainingProgram: string | null
  courseYears: string | null
  educationType: string | null
  faculty: string | null
  major: string | null
  status: string
  position: string | null
  avatar: string | null
  createdAt?: string
  updatedAt?: string
}

/**
 * Quản lý thông tin sinh viên
 */
export function useSchool() {
  const student = ref<Student | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  /**
   * 🔹 Lấy thông tin sinh viên theo ID
   */
  async function studentInit(studentId: number | string) {
    isLoading.value = true
    error.value = null

    try {
      const response = await axios.get(`http://localhost:8000/api/students?student_id=${studentId}`)

      const data = Array.isArray(response.data) ? response.data[0] : response.data
      if (!data) throw new Error('Không tìm thấy dữ liệu sinh viên')

      student.value = {
        id: data.studentId,
        studentCode: data.studentCode,
        firstName: data.firstName,
        lastName: data.lastName,
        fullName: `${data.lastName} ${data.firstName}`.trim(),
        dob: data.dob,
        gender: data.gender,
        email: data.email,
        phone: data.phone,
        className: data.className,
        trainingProgram: data.trainingProgram,
        courseYears: data.courseYears,
        educationType: data.educationType,
        faculty: data.faculty,
        major: data.major,
        status: data.status,
        position: data.position,
        avatar: data.avatar ? `http://localhost:8000${data.avatar}` : null,
        createdAt: data.createdAt,
        updatedAt: data.updatedAt,
      }

      return student.value
    } catch (err: any) {
      error.value = err.message || 'Không thể tải thông tin sinh viên'
      console.error('❌ Student init error:', err)
      return null
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 🔹 Cập nhật dữ liệu sinh viên cục bộ (không gọi API)
   */
  async function updateStudent(data: Partial<Student>) {
    if (!student.value) return null
    try {
      Object.assign(student.value, data)
      return student.value
    } catch (err: any) {
      error.value = err.message || 'Không thể cập nhật thông tin sinh viên'
      console.error('❌ Update student error:', err)
      return null
    }
  }

  return {
    student,
    isLoading,
    error,
    studentInit,
    updateStudent
  }
}
