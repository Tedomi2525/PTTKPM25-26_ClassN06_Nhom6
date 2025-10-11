// middleware/auth.global.ts
export default defineNuxtRouteMiddleware(async (to, from) => {
  const { isLoggedIn, validateToken, initAuth } = useAuth()

  console.log(`🔄 Middleware: Navigating to ${to.path}, isLoggedIn: ${isLoggedIn.value}`)

  // Nếu chưa có user, thử khởi tạo lại từ cookie
  if (!isLoggedIn.value) {
    console.log('🔄 Middleware: Initializing auth...')
    await initAuth()
    console.log(`🔄 Middleware: After init, isLoggedIn: ${isLoggedIn.value}`)
  }

  // Nếu vẫn chưa đăng nhập, chặn vào các trang yêu cầu login
  const requiresAuth = !['/', '/Login'].includes(to.path)

  if (requiresAuth && !isLoggedIn.value) {
    console.log('⚠️ Middleware: Validating token...')
    const valid = await validateToken()
    if (!valid) {
      console.warn('⚠️ Chưa đăng nhập, chuyển hướng về trang Login.')
      return navigateTo('/')
    }
  }

  console.log(`✅ Middleware: Allowing navigation to ${to.path}`)
})
