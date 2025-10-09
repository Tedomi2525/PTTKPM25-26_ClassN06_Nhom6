<!-- TeacherModal.vue -->
<template>
  <div>
    <!-- Nút mở modal -->
    <button
      class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      @click="open = true"
    >
      Thêm Giảng Viên
    </button>

    <!-- Modal -->
    <div
      v-if="open"
      class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50"
    >
      <div class="bg-white rounded-lg shadow-lg w-full max-w-5xl max-h-[90vh] overflow-y-auto">
        <!-- Header -->
        <div class="flex justify-between items-center bg-[#09f] text-white px-6 py-3 rounded-t-lg">
          <h4 class="text-lg font-semibold">Thêm Giảng Viên</h4>
          <button @click="close" class="text-white text-xl font-bold">&times;</button>
        </div>

        <!-- Nội dung form -->
        <div class="p-6">
          <TeacherForm @success="handleSuccess" @cancel="close" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import TeacherForm from "./TeacherForm.vue";

const open = ref(false);

const close = () => {
  open.value = false;
};

const handleSuccess = () => {
  close();
};
</script>
