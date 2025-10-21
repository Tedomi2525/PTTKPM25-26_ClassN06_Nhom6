export default defineNuxtRouteMiddleware(async (to, from) => {
  const { user, role, isLoggedIn, isChecking } = useAuth()
  
  console.log('🔍 Student middleware starting...')
  console.log('🔍 Student middleware - isLoggedIn:', isLoggedIn.value)
  console.log('🔍 Student middleware - isChecking:', isChecking.value)
  
  // Đợi auth checking hoàn tất trước
  if (isChecking.value) {
    console.log('⏳ Student middleware: Waiting for auth check...')
    let attempts = 0
    while (isChecking.value && attempts < 50) {
      await new Promise(resolve => setTimeout(resolve, 100))
      attempts++
    }
  }
  
  // Đợi user data được load (vì middleware auth.global đã chạy trước)
  let attempts = 0
  while (!user.value && isLoggedIn.value && attempts < 30) {
    await new Promise(resolve => setTimeout(resolve, 100))
    attempts++
  }
  
  console.log('🔍 Student middleware - User:', user.value?.fullName || 'none')
  console.log('🔍 Student middleware - Role:', role.value)
  console.log('🔍 Student middleware - IsLoggedIn:', isLoggedIn.value)
  
  // Nếu không đăng nhập thì auth.global sẽ xử lý
  if (!isLoggedIn.value) {
    console.log('ℹ️ Student middleware: Not logged in, letting auth.global handle')
    return
  }
  
  // Kiểm tra role
  if (isLoggedIn.value && role.value !== 'student') {
    console.log('❌ Access denied: User is not a student, role:', role.value)
    
    // Chuyển hướng dựa trên role
    if (role.value === 'teacher') {
      return navigateTo('/teacher', { replace: true })
    } else if (role.value === 'admin') {
      return navigateTo('/admin', { replace: true })
    } else {
      return navigateTo('/home', { replace: true })
    }
  }
  
  if (role.value === 'student') {
    console.log('✅ Student access granted')
  }
})