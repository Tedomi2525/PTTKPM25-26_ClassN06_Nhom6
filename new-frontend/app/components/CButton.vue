<template>
  <!-- Nếu có props.to → dùng RouterLink -->
  <component
    :is="to ? 'RouterLink' : 'button'"
    :to="to"
    :type="buttonType"
    :class="buttonClass"
    @click="handleClick"
  >
    <slot />
  </component>
</template>

<script setup lang="ts">
import { computed } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()

const props = defineProps<{
  type?: "button" | "submit" | "reset" | "back"
  variant?: "primary" | "secondary" | "danger" | "gray"
  to?: string
}>()

const emit = defineEmits<{
  (e: "click", event: MouseEvent): void
}>()

const buttonType = computed(() =>
  props.type === "back" ? "button" : props.type || "button"
)

const buttonClass = computed(() => {
  const base =
    "inline-block px-4 py-2 rounded transition font-medium text-center"

  const variants = {
    primary: "bg-[#09f] text-white hover:bg-blue-700",
    secondary: "bg-gray-500 text-white hover:bg-gray-600",
    danger: "bg-red-500 text-white hover:bg-red-600",
    gray: "bg-gray-300 text-black hover:bg-gray-400",
  }

  return `${base} ${variants[props.variant || "primary"]}`
})

function handleClick(event: MouseEvent) {
  if (props.type === "back") {
    event.preventDefault()
    router.back()
  } else {
    emit("click", event)
  }
}
</script>
