/**
 * Shared utility functions to reduce code duplication
 */

// Common API error handler
export function handleApiError(error: any, context: string = 'API call') {
  console.error(`❌ ${context} failed:`, error)
  
  if (error.name === 'TypeError' && error.message.includes('fetch')) {
    return 'Không thể kết nối đến server. Vui lòng kiểm tra server có đang chạy.'
  }
  
  return error.message || 'Có lỗi không xác định xảy ra'
}

// Common fetch wrapper with error handling
export async function apiCall(url: string, options: RequestInit = {}) {
  try {
    const response = await fetch(url, {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => null)
      const errorMessage = Array.isArray(errorData?.detail) 
        ? errorData.detail.map((err: any) => err.msg).join(', ')
        : errorData?.detail || `HTTP ${response.status}: ${response.statusText}`
      
      throw new Error(errorMessage)
    }

    return await response.json()
  } catch (error) {
    throw new Error(handleApiError(error))
  }
}

// Common success/error notification
export function showNotification(message: string, type: 'success' | 'error' = 'success') {
  const prefix = type === 'success' ? '✅' : '❌'
  alert(`${prefix} ${message}`)
}

// Common confirmation dialog
export function confirmAction(message: string): boolean {
  return confirm(message)
}

// Common data transformer for course/enrollment data
export function transformCourseData(item: any) {
  return {
    ...item,
    courseName: item.courseName || item.course?.name || item.course_name || 'Không có tên môn học',
    courseCode: item.courseCode || item.course?.courseCode || item.course?.course_code || item.course_code || 'N/A',
    credits: item.credits || item.course?.credits || 0,
    section: item.section || 'N/A',
    teacherName: item.teacherName || item.teacher_name || 
      (item.teacher ? `${item.teacher.lastName || item.teacher.last_name} ${item.teacher.firstName || item.teacher.first_name}` : 'Không rõ giảng viên'),
    maxStudents: item.maxStudents || item.max_students || 0,
    enrollmentDate: item.createdAt || item.created_at 
      ? new Date(item.createdAt || item.created_at).toLocaleDateString('vi-VN')
      : undefined
  }
}