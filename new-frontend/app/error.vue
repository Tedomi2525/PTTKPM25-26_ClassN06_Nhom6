<script setup lang="ts">
import FuzzyText from '@/components/FuzzyText/FuzzyText.vue';
import CustomButton from '@/components/Custombutton/CustomButton.vue';
import { ref, onMounted } from 'vue';

// Danh sách lỗi phổ biến
const errorMap: Record<number, { message: string}> = {
  400: { message: 'Bad Request' },
  401: { message: 'Unauthorized' },
  402: { message: 'Payment Required' },
  403: { message: 'Forbidden' },
  404: { message: 'Not Found' },
  405: { message: 'Method Not Allowed' },
  408: { message: 'Request Timeout' },
  500: { message: 'Internal Server Error' },
  502: { message: 'Bad Gateway' },
  503: { message: 'Service Unavailable' },
  504: { message: 'Gateway Timeout' }
};

const errorCode = ref<number>(404);
const errorMessage = ref<string>('Not Found');
const errorColor = ref<string>('#000');

onMounted(() => {
  const win = typeof window !== 'undefined' ? window : undefined;
  if (!win) return;

  const params = new URLSearchParams(win.location.search);
  const code = parseInt(params.get('code') || '404');
  errorCode.value = code;

  if (errorMap[code]) {
    errorMessage.value = errorMap[code].message;
  } else {
    errorMessage.value = 'Unknown Error';
  }
});

</script>

<template>
  <div class="flex justify-center items-center flex-col h-screen gap-8">
    <FuzzyText
      :text="errorCode.toString()"
      :font-size="140"
      font-weight="900"
      :color="errorColor"
      :enable-hover="true"
      :base-intensity="0.18"
      :hover-intensity="0.5"
    />
    <FuzzyText
      :text="errorMessage"
      :font-size="40"
      font-weight="900"
      color="#000"
      :enable-hover="true"
      :base-intensity="0.18"
      :hover-intensity="0.5"
    />
    <CustomButton @click="() => window.location.href='/'" />
  </div>
</template>
