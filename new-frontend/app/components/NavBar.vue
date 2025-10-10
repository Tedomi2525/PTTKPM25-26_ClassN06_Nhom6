<template>
  <nav>
    <div class="max-w-2xl mx-auto px-4">
      <div class="flex justify-center space-x-8 h-12">

<NuxtLink
  v-for="(item, index) in items"
  :key="index"
  :to="item.href"
  @click="$emit('menu-click', item)"
  :class="[ 
    'px-3 py-3 text-sm font-medium border-b-4 transition-colors duration-200 whitespace-nowrap',
    route.path === item.href || route.path.startsWith(item.href + '/')
      ? 'text-white border-white'
      : 'text-gray-300 hover:text-white border-transparent hover:border-white'
  ]"
>
  {{ item.label }}
</NuxtLink>


      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

defineProps({
  items: {
    type: Array,
    default: () => []
  }
})

// khai báo sự kiện
defineEmits(["menu-click"])
</script>
