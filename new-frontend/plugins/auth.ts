// file: ~/plugins/auth.ts
export default defineNuxtPlugin(async (nuxtApp) => {
  const { initAuth } = useAuth()

  // Chỉ chạy initAuth lần đầu khi app được tạo
  if (process.server) {
    await initAuth()
  } else {
    // Hoặc có thể đợi nuxtApp sẵn sàng ở client
    nuxtApp.hooks.hook('app:mounted', async () => {
      await initAuth()
    })
  }
})