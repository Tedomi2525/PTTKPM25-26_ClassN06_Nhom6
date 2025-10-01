<template>
  <div>
    <label
      v-if="label"
      :for="id"
      class="block text-sm font-medium text-gray-700 mb-1"
    >
      {{ label }}
    </label>
    <select
      :id="id"
      :value="modelValue"
      required
      class="mt-1 w-full border border-gray-300 rounded-lg p-3 text-sm focus:outline-none focus:ring-2 focus:ring-[#09f] bg-white"
      @change="onChange"
    >
      <option disabled value="">{{ placeholder }}</option>
      <option
        v-for="(opt, index) in options"
        :key="index"
        :value="opt.value"
      >
        {{ opt.label }}
      </option>
    </select>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  id: string
  modelValue: string
  label?: string
  placeholder?: string
  options: { label: string; value: string }[]
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

function onChange(event: Event) {
  const target = event.target as HTMLSelectElement
  emit('update:modelValue', target.value)
}
</script>
