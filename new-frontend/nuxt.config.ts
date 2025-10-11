import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  
  // Đảm bảo SSR được bật (mặc định là true nhưng khai báo rõ ràng)
  ssr: true,
  
  // Cấu hình router
  router: {
    options: {
      // Đảm bảo hash mode không được bật
      hashMode: false,
    }
  },
  
  // Cấu hình Nitro để handle SPA fallback
  nitro: {
    prerender: {
      // Crawl tất cả các routes
      crawlLinks: true,
      // Fallback về index.html cho các routes không tồn tại
      failOnError: false,
    }
  },
  
  vite: {
    plugins: [
      tailwindcss(),
    ],
  },
});