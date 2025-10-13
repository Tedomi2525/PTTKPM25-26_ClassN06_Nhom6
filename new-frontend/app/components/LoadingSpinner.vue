<template>
  <div :class="containerClass">
    <div class="text-center space-y-4">
      <!-- Spinner -->
      <div :class="spinnerClass"></div>
      
      <!-- Loading text -->
      <div v-if="message || $slots.default">
        <p :class="messageClass">
          <slot>{{ message }}</slot>
        </p>
        <p v-if="subMessage" :class="subMessageClass">{{ subMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  /**
   * Kích thước của spinner
   * - 'small': 8x8 (32px)
   * - 'medium': 12x12 (48px)
   * - 'large': 20x20 (80px)
   */
  size?: 'small' | 'medium' | 'large'
  
  /**
   * Thông điệp chính hiển thị dưới spinner
   */
  message?: string
  
  /**
   * Thông điệp phụ (nhỏ hơn, màu nhạt hơn)
   */
  subMessage?: string
  
  /**
   * Chiều cao tối thiểu của container
   */
  minHeight?: string
  
  /**
   * Có hiển thị full height hay không
   */
  fullHeight?: boolean
  
  /**
   * Màu của spinner (default: blue)
   */
  color?: 'blue' | 'green' | 'red' | 'gray' | 'purple'
}

const props = withDefaults(defineProps<Props>(), {
  size: 'medium',
  message: 'Đang tải...',
  subMessage: '',
  minHeight: '400px',
  fullHeight: false,
  color: 'blue'
})

// Computed classes
const containerClass = computed(() => {
  const base = 'flex justify-center items-center'
  const height = props.fullHeight ? 'flex-1' : `min-h-[${props.minHeight}]`
  return `${base} ${height}`
})

const spinnerClass = computed(() => {
  const sizeClasses = {
    small: 'h-8 w-8',
    medium: 'h-12 w-12', 
    large: 'h-20 w-20'
  }
  
  const colorClasses = {
    blue: 'border-t-blue-600 border-r-transparent border-b-blue-600 border-l-transparent',
    green: 'border-t-green-600 border-r-transparent border-b-green-600 border-l-transparent',
    red: 'border-t-red-600 border-r-transparent border-b-red-600 border-l-transparent',
    gray: 'border-t-gray-600 border-r-transparent border-b-gray-600 border-l-transparent',
    purple: 'border-t-purple-600 border-r-transparent border-b-purple-600 border-l-transparent'
  }
  
  const borderWidth = props.size === 'small' ? 'border-2' : 'border-4'
  
  return `inline-block animate-spin rounded-full ${sizeClasses[props.size]} ${borderWidth} ${colorClasses[props.color]}`
})

const messageClass = computed(() => {
  const sizeClasses = {
    small: 'text-sm',
    medium: 'text-base',
    large: 'text-lg'
  }
  
  return `text-gray-700 font-semibold ${sizeClasses[props.size]} mt-4`
})

const subMessageClass = computed(() => {
  const sizeClasses = {
    small: 'text-xs',
    medium: 'text-sm', 
    large: 'text-base'
  }
  
  return `text-gray-500 ${sizeClasses[props.size]} mt-2`
})
</script>