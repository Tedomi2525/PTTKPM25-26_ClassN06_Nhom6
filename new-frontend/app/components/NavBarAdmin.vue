<template>
  <nav class="">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-center space-x-8 h-12">
        <NuxtLink 
          v-for="(item, index) in items" 
          :key="index"
          :to="item.href"
          class="text-white hover:text-gray-300 px-3 py-3 text-sm font-medium border-b-2 border-transparent hover:border-gray-300 transition-colors duration-200"
        >
          {{ item.label }}
        </NuxtLink>
      </div>
    </div>
  </nav>
</template>

<script setup>
// Props để component tái sử dụng
defineProps({
  items: {
    type: Array,
    default: () => []
  }
})
</script>
