<template>
  <!-- Nếu có props.to → dùng RouterLink -->
  <component
    :is="to ? 'RouterLink' : 'button'"
    :to="to"
    :type="buttonType"
    :class="buttonClass"
    :disabled="props.disabled"
    @click="handleClick"
  >
    <span class="flex items-center justify-center gap-2">
      <!-- Icon động -->
      <span v-if="icon" v-html="icon" class="w-4 h-4"></span>
      <slot />
    </span>
  </component>
</template>

<script setup lang="ts">
import { computed } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()

const props = defineProps<{
  type?: "button" | "submit" | "reset" | "back" | "edit" | "delete"
  variant?: "primary" | "secondary" | "danger" | "gray" | "edit" | "delete"
  to?: string
  disabled?: boolean
}>()

const emit = defineEmits<{
  (e: "click", event: MouseEvent): void
  (e: "edit", event: MouseEvent): void
  (e: "delete", event: MouseEvent): void
}>()

// ✅ Tự xác định loại nút
const buttonType = computed(() =>
  ["back", "edit", "delete"].includes(props.type || "")
    ? "button"
    : props.type || "button"
)

// ✅ CSS theo variant
const buttonClass = computed(() => {
  const base =
    "inline-flex items-center gap-2 px-3 py-2 rounded transition font-medium text-center text-sm select-none"

  const variants: Record<string, string> = {
    primary: "bg-[#09f] text-white hover:bg-blue-700",
    secondary: "bg-gray-500 text-white hover:bg-gray-600",
    danger: "bg-red-500 text-white hover:bg-red-600",
    gray: "bg-gray-300 text-black hover:bg-gray-400",
    edit: "bg-yellow-400 text-black hover:bg-yellow-500",
    delete: "bg-red-500 text-white hover:bg-red-600",
  }

  const disabledClass = props.disabled 
    ? "opacity-50 cursor-not-allowed pointer-events-none" 
    : "cursor-pointer"

  return `${base} ${variants[props.variant || props.type || "primary"]} ${disabledClass}`
})

// ✅ Icon theo loại
const icon = computed(() => {
  switch (props.variant || props.type) {
    case "edit":
      return `<svg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M11 4H4a2 2 0 00-2 2v14l4-4h5m7.586-9.586a2 2 0 112.828 2.828L11.828 19H9v-2.828l9.586-9.586z' /></svg>`
    case "delete":
      return `<svg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16' /></svg>`
    default:
      return null
  }
})

// ✅ Hành vi khi click
function handleClick(event: MouseEvent) {
  if (props.disabled) {
    event.preventDefault()
    return
  }

  if (props.type === "back") {
    event.preventDefault()
    router.back()
  } else if (props.type === "edit" || props.variant === "edit") {
    emit("edit", event)
  } else if (props.type === "delete" || props.variant === "delete") {
    emit("delete", event)
  } else {
    emit("click", event)
  }
}
</script>
