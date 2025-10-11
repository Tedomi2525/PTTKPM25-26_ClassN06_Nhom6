export default defineNuxtRouteMiddleware(async (to, from) => {
  const { user, role, isLoggedIn } = useAuth()
  
  // Đợi user data được load (vì middleware auth.global đã chạy trước)
  let attempts = 0
  while (!user.value && isLoggedIn.value && attempts < 30) {
    await new Promise(resolve => setTimeout(resolve, 100))
    attempts++
  }
  
  console.log('🔍 Student middleware - User:', user.value)
  console.log('🔍 Student middleware - Role:', role.value)
  console.log('🔍 Student middleware - IsLoggedIn:', isLoggedIn.value)
  
  // Kiểm tra role
  if (isLoggedIn.value && role.value !== 'student') {
    console.log('❌ Access denied: User is not a student, role:', role.value)
    
    // Sử dụng navigateTo thay vì throw error
    return navigateTo('/home', { replace: true })
  }
  
  if (role.value === 'student') {
    console.log('✅ Student access granted')
  }
})