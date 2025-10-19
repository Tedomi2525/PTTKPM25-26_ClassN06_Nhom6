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

  // --- Cập nhật token (optimized single storage) ---
  function setToken(value: string | null) {
    const startTime = performance.now()
    
    // Ưu tiên cookie (Nuxt SSR-friendly), localStorage làm backup
    authToken.value = value
    
    if (import.meta.client) {
      // Batch localStorage operations để giảm I/O
      requestIdleCallback(() => {
        if (value) {
          localStorage.setItem('auth_token', value)
        } else {
          localStorage.removeItem('auth_token')
        }
        const duration = performance.now() - startTime
        if (duration > 10) {
          console.warn(`🐌 setToken took ${duration.toFixed(1)}ms`)
        }
      }, { timeout: 100 })
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
    // Tránh multiple concurrent init calls với Promise-based approach (faster)
    if (isChecking.value) {
      console.log('⏳ initAuth already running, waiting with timeout...')
      // Chờ tối đa 2 giây thay vì 5 giây, và check mỗi 50ms thay vì 100ms
      return new Promise((resolve) => {
        const startTime = Date.now()
        const checkInterval = setInterval(() => {
          if (!isChecking.value || Date.now() - startTime > 2000) {
            clearInterval(checkInterval)
            resolve(void 0)
          }
        }, 50)
      })
    }

    isChecking.value = true
    console.log('🔄 Starting initAuth...')
    
    try {
      const token = authToken.value
      console.log('🔑 Current token:', token ? 'exists' : 'none')
      
      if (!token) {
        console.log('❌ No token found, clearing auth state')
        clearAuthState()
        return
      }

      console.log('📞 Fetching user info...')
      const info = await fetchUserInfo(token)
      if (info) {
        user.value = info
        isLoggedIn.value = true
        console.log('✅ Auth initialized successfully:', info.fullName)
      } else {
        console.log('❌ Failed to fetch user info, clearing auth state')
        clearAuthState()
      }
    } catch (error) {
      console.error('🚨 Error in initAuth:', error)
      clearAuthState()
    } finally {
      isChecking.value = false
      console.log('🔄 initAuth completed')
    }
  }

  // --- Đăng nhập (optimized) ---
  async function login(payload: { username: string; password: string }) {
    isChecking.value = true
    loginError.value = ''
    
    console.log('🔄 Starting optimized login process...')
    const startTime = performance.now()
    const timings: Record<string, number> = {}

    try {
      // Step 1: Login API
      const loginStart = performance.now()
      const res = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
      timings.loginApi = performance.now() - loginStart

      if (!res.ok) throw new Error('Sai tài khoản hoặc mật khẩu')

      const data = await res.json()
      const accessToken = data.accessToken || data.access_token
      if (!accessToken) throw new Error('Không nhận được access token')

      // Step 2: Save token (non-blocking)
      const tokenStart = performance.now()
      setToken(accessToken)
      timings.saveToken = performance.now() - tokenStart

      // Step 3: Fetch user info
      const userInfoStart = performance.now()
      const info = await fetchUserInfo(accessToken)
      timings.fetchUserInfo = performance.now() - userInfoStart

      if (!info) throw new Error('Không thể lấy thông tin người dùng')

      // Step 4: Update state (batch)
      const stateStart = performance.now()
      user.value = info
      isLoggedIn.value = true
      timings.updateState = performance.now() - stateStart
      
      const endTime = performance.now()
      const totalTime = (endTime - startTime).toFixed(0)
      
      console.log(`👤 Đăng nhập thành công: ${info.fullName} (${totalTime}ms)`)
      console.log(`📊 Timing breakdown:`, {
        loginApi: `${timings.loginApi.toFixed(1)}ms`,
        saveToken: `${timings.saveToken.toFixed(1)}ms`, 
        fetchUserInfo: `${timings.fetchUserInfo.toFixed(1)}ms`,
        updateState: `${timings.updateState.toFixed(1)}ms`
      })

      // Navigate after successful login (don't block return)
      router.push('/home')

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
  const isLoggingOut = ref(false)
  async function logout() {
    if (isLoggingOut.value) {
      return
    }
    
    isLoggingOut.value = true

      // Xóa token phía client (JWT-based logout)
      clearAuthState()
      await router.push('/')
      isLoggingOut.value = false
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
    isLoggingOut,
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
