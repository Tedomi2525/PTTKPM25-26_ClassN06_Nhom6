import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  
  // SSR mode để xử lý routing đúng khi F5
  ssr: true,
  
  vite: {
    plugins: [
      tailwindcss(),
    ],
  },
});