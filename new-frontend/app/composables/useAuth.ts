import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

/**
 * Kiểu dữ liệu người dùng
 */
export interface User {
  user_id: string | number
  fullName: string
  role: string
  schoolId: string
  programId?: number
  avatar: string
  domain?: string
}

/**
 * Phản hồi từ API đăng nhập
 */
interface LoginResponse {
  accessToken: string
  user: User
}

export function useAuth() {
  const router = useRouter()
  const API_BASE = 'http://localhost:8000' // 👈 domain cố định backend

  // --- STATE ---
  const authToken = useCookie<string | null>('auth_token')
  const user = useState<User | null>('user', () => null)
  const isLoggedIn = useState<boolean>('isLoggedIn', () => !!authToken.value)
  const isChecking = useState<boolean>('isChecking', () => false)
  const loginError = ref<string>('')

  // --- Đồng bộ token với localStorage ---
  if (import.meta.client && !authToken.value) {
    const stored = localStorage.getItem('auth_token')
    if (stored) authToken.value = stored
  }

  // --- Cập nhật token (cookie + localStorage) ---
  function setToken(value: string | null) {
    authToken.value = value
    if (import.meta.client) {
      if (value) localStorage.setItem('auth_token', value)
      else localStorage.removeItem('auth_token')
    }
  }

  // --- Xóa toàn bộ trạng thái đăng nhập ---
  function clearAuthState() {
    setToken(null)
    user.value = null
    isLoggedIn.value = false
  }

  // --- Lấy thông tin người dùng từ token ---
  async function fetchUserInfo(token: string): Promise<User | null> {
    try {
      const res = await fetch(`${API_BASE}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` },
      })

      if (!res.ok) {
        console.error('❌ /auth/me failed:', res.status)
        return null
      }

      const data = await res.json()
      console.log('✅ /auth/me response:', data)

      return {
        user_id: data.user_id || data.userId || '',
        fullName: data.fullName || data.full_name,
        role: data.role || data.user_role || 'user',
        schoolId: data.schoolId || data.school_id || '',
        avatar: data.avatar || '',
        domain: data.domain || '',
        programId: data.programId || data.program_id || null,
      }
    } catch (err) {
      console.error('🚨 Lỗi khi gọi /auth/me:', err)
      return null
    }
  }

  // --- Khởi tạo xác thực ---
  async function initAuth() {
    isChecking.value = true
    try {
      const token = authToken.value
      if (!token) {
        clearAuthState()
        return
      }

      const info = await fetchUserInfo(token)
      if (info) {
        user.value = info
        isLoggedIn.value = true
      } else {
        clearAuthState()
      }
    } finally {
      isChecking.value = false
    }
  }

  // --- Đăng nhập ---
  async function login(payload: { username: string; password: string }) {
    isChecking.value = true
    loginError.value = ''

    try {
      const res = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })

      if (!res.ok) throw new Error('Sai tài khoản hoặc mật khẩu')

      const data = await res.json()
      const accessToken = data.accessToken || data.access_token
      if (!accessToken) throw new Error('Không nhận được access token')

      setToken(accessToken)
      const info = await fetchUserInfo(accessToken)

      if (!info) throw new Error('Không thể lấy thông tin người dùng')

      user.value = info
      isLoggedIn.value = true
      console.log(`👤 Đăng nhập thành công: ${info.fullName}`)
      await router.push('/home')

      return { success: true, user: info }
    } catch (err: any) {
      console.error('❌ Login error:', err)
      clearAuthState()
      loginError.value =
        err.message || 'Đăng nhập thất bại — vui lòng thử lại.'
      return { success: false, message: loginError.value }
    } finally {
      isChecking.value = false
    }
  }

  // --- Đăng xuất ---
  async function logout() {
    try {
      if (authToken.value) {
        await fetch(`${API_BASE}/auth/logout`, {
          method: 'POST',
          headers: { Authorization: `Bearer ${authToken.value}` },
        })
      }
    } catch (e) {
      console.warn('⚠️ Logout API failed — clearing local state.', e)
    } finally {
      clearAuthState()
      await router.push('/')
    }
  }

  // --- Kiểm tra token ---
  async function validateToken(): Promise<boolean> {
    const token = authToken.value
    if (!token) return false

    try {
      const info = await fetchUserInfo(token)
      if (info) {
        user.value = info
        isLoggedIn.value = true
        return true
      }
      clearAuthState()
      return false
    } catch {
      clearAuthState()
      return false
    }
  }

  // --- Cập nhật thông tin người dùng ---
  async function updateProfile(data: Partial<User>): Promise<User | null> {
    const token = authToken.value
    if (!token) return null

    try {
      const res = await fetch(`${API_BASE}/auth/profile`, {
        method: 'PUT',
        headers: { 
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}` 
        },
        body: JSON.stringify(data),
      })

      if (!res.ok) {
        throw new Error('Cập nhật thông tin thất bại')
      }

      const updatedUser = await res.json()
      if (user.value) {
        Object.assign(user.value, updatedUser)
      }
      
      return user.value
    } catch (err) {
      console.error('🚨 Lỗi khi cập nhật thông tin:', err)
      throw err
    }
  }

  // --- Đổi mật khẩu ---
  async function changePassword(currentPassword: string, newPassword: string, confirmPassword: string): Promise<{ success: boolean; message: string }> {
    const token = authToken.value
    if (!token) {
      return { success: false, message: 'Bạn cần đăng nhập để thực hiện chức năng này' }
    }

    // Validation trước khi gửi request
    if (newPassword !== confirmPassword) {
      return { success: false, message: 'Mật khẩu mới và xác nhận mật khẩu không khớp' }
    }

    if (newPassword.length < 8) {
      return { success: false, message: 'Mật khẩu mới phải có ít nhất 8 ký tự' }
    }

    try {
      const res = await fetch(`${API_BASE}/auth/change-password`, {
        method: 'PUT',
        headers: { 
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}` 
        },
        body: JSON.stringify({ 
          currentPassword, 
          newPassword,
          confirmPassword 
        }),
      })

      const data = await res.json()

      if (!res.ok) {
        const errorMessage = data.detail || 'Đổi mật khẩu thất bại'
        return { success: false, message: errorMessage }
      }

      return { success: true, message: data.message || 'Đổi mật khẩu thành công' }
    } catch (err) {
      console.error('🚨 Lỗi khi đổi mật khẩu:', err)
      return { success: false, message: 'Có lỗi xảy ra khi đổi mật khẩu. Vui lòng thử lại.' }
    }
  }

  // --- computed ---
  const schoolId = computed(() => user.value?.schoolId || '')
  const domain = computed(() => user.value?.domain || '')
  const fullName = computed(() => user.value?.fullName || 'Admin')
  const displayName = computed(() => user.value?.fullName || 'Admin')
  const role = computed(() => user.value?.role || '')
  const token = computed(() => authToken.value)
  const avatar = computed(() => user.value?.avatar || '')
  const programId = computed(() => user.value?.programId || '')
  // --- return ---
  return {
    // state
    user,
    authToken,
    isLoggedIn,
    isChecking,
    loginError,

    // methods
    login,
    logout,
    initAuth,
    validateToken,
    updateProfile,
    changePassword,

    // computed
    schoolId,
    domain,
    fullName,
    displayName,
    role,
    token,
    avatar,
    programId,
  }
}
