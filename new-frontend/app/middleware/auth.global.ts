// middleware/auth.global.ts
export default defineNuxtRouteMiddleware(async (to, from) => {
  const { isLoggedIn, validateToken, initAuth, isChecking } = useAuth()

  // Đợi nếu đang trong quá trình checking
  if (isChecking.value) {
    let attempts = 0
    while (isChecking.value && attempts < 50) {
      await new Promise(resolve => setTimeout(resolve, 100))
      attempts++
    }
  }

  // Nếu chưa có user, thử khởi tạo lại từ cookie
  if (!isLoggedIn.value) {
    await initAuth()
  }

  // Nếu vẫn chưa đăng nhập, kiểm tra các trang yêu cầu login
  const requiresAuth = !['/', '/Login'].includes(to.path)

  if (requiresAuth && !isLoggedIn.value) {

    const valid = await validateToken()
    if (!valid) {
      return navigateTo('/')
    }
    
  }
})
