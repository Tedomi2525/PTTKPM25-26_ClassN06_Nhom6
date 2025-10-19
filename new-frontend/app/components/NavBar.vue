<template>
  <nav>
    <div class="max-w-2xl mx-auto px-4">
      <div class="flex justify-center space-x-8 h-12">
        <!-- Menu items with dropdown support -->
        <template v-for="(item, index) in items" :key="index">
          <!-- Menu item with dropdown -->
          <div 
            v-if="item.dropdown"
            class="relative group"
            @mouseenter="activeDropdown = item.label"
            @mouseleave="activeDropdown = null"
          >
            <button
              :class="[ 
                'px-3 py-3 text-sm font-medium border-b-4 transition-colors duration-200 whitespace-nowrap flex items-center',
                selectedMenu === item.label || isActiveRoute(item) 
                  ? 'text-white border-white'
                  : 'text-gray-300 hover:text-white border-transparent hover:border-white'
              ]"
            >
              {{ item.label }}
              <svg 
                class="w-4 h-4 ml-1 transition-transform duration-200"
                :class="{ 'rotate-180': activeDropdown === item.label }"
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            
            <!-- Dropdown menu -->
            <transition
              enter-active-class="transition ease-out duration-200"
              enter-from-class="opacity-0 transform -translate-y-2"
              enter-to-class="opacity-100 transform translate-y-0"
              leave-active-class="transition ease-in duration-150"
              leave-from-class="opacity-100 transform translate-y-0"
              leave-to-class="opacity-0 transform -translate-y-2"
            >
              <div 
                v-if="activeDropdown === item.label"
                class="absolute top-full left-0 pt-2 w-48 z-50"
              >
                <!-- Triangle pointer -->
                <div class="flex justify-center">
                  <div class="w-0 h-0 border-l-[8px] border-l-transparent border-r-[8px] border-r-transparent border-b-[8px] border-b-white"></div>
                </div>
                <!-- Dropdown content -->
                <div class="bg-white rounded-lg shadow-xl border border-gray-200 overflow-hidden mt-0">
                  <NuxtLink
                    v-for="(subItem, subIndex) in item.dropdown"
                    :key="subIndex"
                    :to="subItem.href"
                    @click="$emit('menu-click', subItem)"
                    class="block px-4 py-2 text-gray-800 hover:bg-blue-100 hover:text-blue-700 transition-colors duration-200"
                  >
                    {{ subItem.label }}
                  </NuxtLink>
                </div>
              </div>
            </transition>
          </div>

          <!-- Regular menu item without dropdown -->
          <NuxtLink
            v-else
            :to="item.href"
            @click="$emit('menu-click', item)"
            :class="[ 
              'px-3 py-3 text-sm font-medium border-b-4 transition-colors duration-200 whitespace-nowrap',
              selectedMenu === item.label || route.path === item.href || route.path.startsWith(item.href + '/')
                ? 'text-white border-white'
                : 'text-gray-300 hover:text-white border-transparent hover:border-white'
            ]"
          >
            {{ item.label }}
          </NuxtLink>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const activeDropdown = ref(null)

defineProps({
  items: {
    type: Array,
    default: () => []
  },
  selectedMenu: {
    type: [String, null],
    default: null
  }
})

// Function to check if route is active for dropdown items
function isActiveRoute(item) {
  if (!item.dropdown) return false
  return item.dropdown.some(subItem => 
    route.path === subItem.href || route.path.startsWith(subItem.href + '/')
  )
}

// khai báo sự kiện
defineEmits(["menu-click"])
</script>
