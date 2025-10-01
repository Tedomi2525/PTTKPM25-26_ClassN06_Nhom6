<template>
  <div>
    <label v-if="label" class="block text-sm font-medium mb-1">{{ label }}</label>

    <!-- Input file ẩn -->
    <input
      :id="id"
      type="file"
      accept="image/*"
      class="hidden"
      @change="onFileChange"
    />

    <!-- Nút chọn ảnh -->
    <label
      :for="id"
      class="mt-1 h-11 inline-block  cursor-pointer px-4 py-2 bg-[#09f] text-white rounded-lg shadow hover:bg-blue-600 transition"
    >
      {{ buttonText }}
    </label>

    <!-- Hiển thị tên file -->
    <span v-if="fileName" class="ml-3 text-sm text-gray-600">{{ fileName }}</span>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue"

const props = defineProps<{
  id: string
  label?: string
  buttonText?: string
}>()

const emit = defineEmits<{
  (e: "update:file", file: File | null): void
}>()

const fileName = ref("")

function onFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0] || null
  fileName.value = file ? file.name : ""
  emit("update:file", file)
}
</script>
