// middleware/auth.global.ts
export default defineNuxtRouteMiddleware(async (to, from) => {
  const { isLoggedIn, validateToken, initAuth, isChecking } = useAuth()

  console.log(`🔄 Middleware: Navigating to ${to.path}`)
  console.log(`🔄 Middleware: isLoggedIn: ${isLoggedIn.value}, isChecking: ${isChecking.value}`)

  // Đợi nếu đang trong quá trình checking
  if (isChecking.value) {
    console.log('⏳ Middleware: Waiting for auth check to complete...')
    let attempts = 0
    while (isChecking.value && attempts < 50) {
      await new Promise(resolve => setTimeout(resolve, 100))
      attempts++
    }
    console.log(`🔄 Middleware: Auth check completed, isLoggedIn: ${isLoggedIn.value}`)
  }

  // Nếu chưa có user, thử khởi tạo lại từ cookie
  if (!isLoggedIn.value) {
    console.log('🔄 Middleware: Initializing auth...')
    await initAuth()
    console.log(`🔄 Middleware: After init, isLoggedIn: ${isLoggedIn.value}`)
  }

  // Nếu vẫn chưa đăng nhập, kiểm tra các trang yêu cầu login
  const requiresAuth = !['/', '/Login'].includes(to.path)

  if (requiresAuth && !isLoggedIn.value) {
    console.log('⚠️ Middleware: Page requires auth but not logged in')
    console.log('⚠️ Middleware: Final validation attempt...')
    const valid = await validateToken()
    if (!valid) {
      console.warn('⚠️ Auth validation failed, redirecting to login')
      return navigateTo('/')
    }
    console.log('✅ Middleware: Token validation successful')
  }

  console.log(`✅ Middleware: Allowing navigation to ${to.path}`)
})
