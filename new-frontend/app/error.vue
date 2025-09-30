<script setup lang="ts">
import { useRoute } from "vue-router"
import FuzzyText from "@/components/FuzzyText/FuzzyText.vue"

// Lấy code lỗi từ query hoặc default = 404
const route = useRoute()
const errorCode = Number(route.query.code) || 404

// Map code → message
const messages: Record<number, string> = {
  404: "Không tìm thấy trang",
  500: "Lỗi máy chủ",
  403: "Truy cập bị từ chối",
  401: "Chưa xác thực",
  400: "Yêu cầu không hợp lệ"
}

const message = messages[errorCode] || "Đã xảy ra lỗi"
</script>

<template>
  <div class="flex h-screen w-full flex-col items-center justify-center gap-6 bg-white text-center">
    <!-- Hiển thị mã lỗi -->
    <FuzzyText
      :text="String(errorCode)"
      :font-size="120"
      font-weight="900"
      color="#000"
      :enable-hover="true"
      :base-intensity="0.18"
      :hover-intensity="0.5"
    />

    <!-- Hiển thị thông báo -->
    <FuzzyText
      :text="message"
      :font-size="32"
      font-weight="700"
      color="#555"
      :enable-hover="true"
      :base-intensity="0.15"
      :hover-intensity="0.4"
    />

    <!-- Nút quay về trang chủ -->
    <NuxtLink
      to="/"
      class="mt-4 inline-block rounded bg-[#09f] px-6 py-3 text-white hover:bg-blue-600 transition"
    >
      Quay về trang chủ
    </NuxtLink>
  </div>
</template>
