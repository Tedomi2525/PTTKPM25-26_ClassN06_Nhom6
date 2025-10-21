<template>
  <transition
    enter-active-class="transition-all duration-300 ease-out"
    enter-from-class="opacity-0 transform translate-y-[-10px]"
    enter-to-class="opacity-100 transform translate-y-0"
    leave-active-class="transition-all duration-200 ease-in"
    leave-from-class="opacity-100 transform translate-y-0"
    leave-to-class="opacity-0 transform translate-y-[-10px]"
  >
    <div
      v-if="show && message"
      class="mt-2 px-4 py-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg shadow-sm"
    >
      <div class="flex items-start">
        <!-- Error Icon -->
        <div class="flex-shrink-0">
          <svg 
            class="h-5 w-5 text-red-500 dark:text-red-400 mt-0.5" 
            viewBox="0 0 20 20" 
            fill="currentColor"
          >
            <path 
              fill-rule="evenodd" 
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" 
              clip-rule="evenodd" 
            />
          </svg>
        </div>

        <!-- Error Message -->
        <div class="ml-3 flex-1">
          <p class="text-sm text-red-700 dark:text-red-300 font-medium">
            {{ message }}
          </p>
          
          <p v-if="details" class="text-xs text-red-600 dark:text-red-400 mt-1 opacity-80">
            {{ details }}
          </p>
        </div>

        <!-- Close Button -->
        <div v-if="closable" class="ml-2 flex-shrink-0">
          <button
            @click="$emit('close')"
            class="text-red-500 dark:text-red-400 hover:text-red-700 dark:hover:text-red-200 transition-colors duration-150"
          >
            <svg class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
              <path 
                fill-rule="evenodd" 
                d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" 
                clip-rule="evenodd" 
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
defineProps({
  message: { type: String, default: '' },
  details: { type: String, default: '' },
  show: { type: Boolean, default: true },
  closable: { type: Boolean, default: false }
})

defineEmits(['close'])
</script>
