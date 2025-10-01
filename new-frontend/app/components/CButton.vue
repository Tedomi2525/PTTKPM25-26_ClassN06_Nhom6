<template>
  <button
    :type="type"
    class="px-4 py-2 bg-[#09f] text-white rounded hover:bg-blue-700 transition"
    @click="onClick"
  >
    <slot>Lưu</slot>
  </button>
</template>

<script setup lang="ts">
const props = defineProps<{
  type?: "button" | "submit" | "reset"
}>()

const emit = defineEmits<{
  (e: "click", event: MouseEvent): void
}>()

function onClick(event: MouseEvent) {
  emit("click", event)
}
</script>
