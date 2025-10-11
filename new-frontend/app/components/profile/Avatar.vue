<template>
  <div class="flex flex-col items-center gap-6 p-6 font-semibold">
    <!-- Ảnh đại diện -->
    <div
      class="relative w-32 h-32 rounded-full overflow-hidden border-4 border-blue-300
             bg-white shadow-md transition-all duration-300 hover:translate-y-[-2px] hover:shadow-lg"
    >
      <img
        :src="avatarPreview || (imageError ? defaultAvatarUrl : currentAvatar)"
        alt="avatar"
        class="w-full h-full object-cover block"
        @error="handleImageError"
        @load="imageError = false"
      />

      <!-- Overlay khi hover -->
      <div
        class="absolute inset-0 bg-black/0 hover:bg-black/20 transition-all duration-300
               flex items-center justify-center cursor-pointer"
      >
        <span
          class="text-white text-sm font-medium opacity-0 hover:opacity-100 transition-opacity duration-300 drop-shadow"
        >
          Thay đổi
        </span>
      </div>
    </div>

    <!-- Nút upload và save -->
    <div class="flex gap-4 w-full max-w-[360px]">
      <!-- Nút upload -->
      <label
        class="flex items-center justify-center gap-2 px-4 py-2 text-sm font-medium
               text-gray-700 bg-gray-100 border border-gray-300 rounded-md
               hover:bg-gray-200 hover:border-gray-400 transition-all cursor-pointer flex-1"
      >
        <svg
          class="w-4 h-4 flex-shrink-0"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
        </svg>
        Chọn ảnh
        <input
          type="file"
          @change="handleFileSelect"
          accept="image/*"
          class="hidden"
        />
      </label>

      <!-- Nút lưu -->
      <CButton
        @click="handleSave"
        :disabled="!selectedFile"
        variant="primary"
        class="flex-1"
      >
        <svg
          class="w-4 h-4 flex-shrink-0"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
        </svg>
        Lưu
      </CButton>
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, computed } from 'vue';
import CButton from '@/components/CButton.vue';

const { user, avatar, updateProfile } = useAuth();

// Default avatar
const defaultAvatarUrl = 'https://via.placeholder.com/150/cccccc/666666?text=Avatar';
const selectedFile = ref<File | null>(null);
const avatarPreview = ref<string | null>(null);
const imageError = ref<boolean>(false);

const currentAvatar = computed(() => {
  if (!avatar.value) {
    return defaultAvatarUrl;
  }

  if (avatar.value.startsWith('http')) {
    return avatar.value;
  }

  return `http://127.0.0.1:8000${avatar.value.startsWith('/') ? avatar.value : '/' + avatar.value}`;
});

const handleImageError = () => {
  imageError.value = true;
};

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];

  if (file && file.type.startsWith('image/')) {
    selectedFile.value = file;

    const reader = new FileReader();
    reader.onload = (e) => {
      avatarPreview.value = e.target?.result as string;
    };
    reader.readAsDataURL(file);
  } else {
    selectedFile.value = null;
    avatarPreview.value = null;
    if (file) {
      alert('Vui lòng chọn file ảnh hợp lệ');
    }
  }
};

const handleSave = async () => {
  if (selectedFile.value && avatarPreview.value) {
    try {
      await updateProfile({ avatar: avatarPreview.value });
      selectedFile.value = null;
      avatarPreview.value = null;
      alert('Ảnh đại diện đã được thay đổi!');
    } catch (error) {
      console.error('Lỗi khi cập nhật avatar:', error);
      alert('Có lỗi xảy ra khi cập nhật ảnh đại diện');
    }
  }
};
</script>
