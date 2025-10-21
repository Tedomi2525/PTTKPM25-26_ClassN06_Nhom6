<template>
  <div class="p-6 space-y-8">
    <h1 class="text-3xl font-bold text-center mb-8">LoadingSpinner Component Demo</h1>
    
    <!-- Demo các size khác nhau -->
    <section class="space-y-4">
      <h2 class="text-xl font-semibold">Kích thước khác nhau</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="border rounded-lg p-4">
          <h3 class="text-center mb-4 font-medium">Small</h3>
          <LoadingSpinner 
            size="small"
            message="Loading small..."
            min-height="200px"
          />
        </div>
        <div class="border rounded-lg p-4">
          <h3 class="text-center mb-4 font-medium">Medium (Default)</h3>
          <LoadingSpinner 
            size="medium"
            message="Loading medium..."
            min-height="200px"
          />
        </div>
        <div class="border rounded-lg p-4">
          <h3 class="text-center mb-4 font-medium">Large</h3>
          <LoadingSpinner 
            size="large"
            message="Loading large..."
            min-height="200px"
          />
        </div>
      </div>
    </section>

    <!-- Demo các màu khác nhau -->
    <section class="space-y-4">
      <h2 class="text-xl font-semibold">Màu sắc khác nhau</h2>
      <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div class="border rounded-lg p-4">
          <h3 class="text-center mb-4 font-medium text-sm">Blue</h3>
          <LoadingSpinner 
            color="blue"
            message="Blue loading"
            min-height="150px"
          />
        </div>
        <div class="border rounded-lg p-4">
          <h3 class="text-center mb-4 font-medium text-sm">Green</h3>
          <LoadingSpinner 
            color="green"
            message="Green loading"
            min-height="150px"
          />
        </div>
        <div class="border rounded-lg p-4">
          <h3 class="text-center mb-4 font-medium text-sm">Red</h3>
          <LoadingSpinner 
            color="red"
            message="Red loading"
            min-height="150px"
          />
        </div>
        <div class="border rounded-lg p-4">
          <h3 class="text-center mb-4 font-medium text-sm">Purple</h3>
          <LoadingSpinner 
            color="purple"
            message="Purple loading"
            min-height="150px"
          />
        </div>
        <div class="border rounded-lg p-4">
          <h3 class="text-center mb-4 font-medium text-sm">Gray</h3>
          <LoadingSpinner 
            color="gray"
            message="Gray loading"
            min-height="150px"
          />
        </div>
      </div>
    </section>

    <!-- Demo với slot -->
    <section class="space-y-4">
      <h2 class="text-xl font-semibold">Sử dụng Slot</h2>
      <div class="border rounded-lg p-4">
        <LoadingSpinner 
          color="blue"
          sub-message="Đang xử lý dữ liệu..."
          min-height="200px"
        >
          <span class="text-lg font-semibold">🔄 Đang tải dữ liệu từ server</span>
        </LoadingSpinner>
      </div>
    </section>

    <!-- Demo fullHeight -->
    <section class="space-y-4">
      <h2 class="text-xl font-semibold">Full Height</h2>
      <div class="border rounded-lg h-96">
        <LoadingSpinner 
          color="purple"
          size="large"
          message="Loading với full height"
          sub-message="Chiếm toàn bộ chiều cao container"
          full-height
        />
      </div>
    </section>

    <!-- Demo toggle loading -->
    <section class="space-y-4">
      <h2 class="text-xl font-semibold">Interactive Demo</h2>
      <div class="space-x-4 mb-4">
        <button 
          @click="toggleLoading"
          class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          {{ isLoading ? 'Dừng Loading' : 'Bắt đầu Loading' }}
        </button>
        <button 
          @click="changeMessage"
          class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
        >
          Đổi thông điệp
        </button>
      </div>
      <div class="border rounded-lg">
        <LoadingSpinner 
          v-if="isLoading"
          :message="currentMessage"
          sub-message="Click button để điều khiển"
          color="blue"
          min-height="300px"
        />
        <div v-else class="flex items-center justify-center min-h-[300px]">
          <p class="text-gray-500 text-lg">Không có loading state</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const isLoading = ref(false)
const currentMessage = ref('Đang tải dữ liệu...')

const messages = [
  'Đang tải dữ liệu...',
  'Đang xử lý yêu cầu...',
  'Đang đồng bộ thông tin...',
  'Đang cập nhật dữ liệu...',
  'Đang kết nối server...'
]

let messageIndex = 0

function toggleLoading() {
  isLoading.value = !isLoading.value
}

function changeMessage() {
  messageIndex = (messageIndex + 1) % messages.length
  currentMessage.value = messages[messageIndex]
}

definePageMeta({
  title: 'LoadingSpinner Demo'
})
</script>