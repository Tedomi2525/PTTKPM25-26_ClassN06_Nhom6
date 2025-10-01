<template>
  <main class="min-h-screen flex">
    <!-- Left Section -->
    <section class="hidden md:flex flex-col justify-center items-center w-1/2 bg-[#09f] p-10">
      <header class="text-right space-y-2">
        <h1 class="text-4xl font-bold text-white pt-20">
          Phân tích thiết kế phần mềm
        </h1>
        <h2 class="text-4xl py-[10px] font-bold text-white">
          Nhóm 6
        </h2>
        <h3 class="text-4xl font-bold text-white">
          Quản lý đào tạo ứng dụng hệ thống điểm danh khuôn mặt
        </h3>
      </header>
        <img src="https://c.animaapp.com/mewurn4ndN2M6v/img/students-pana-fba09de9-1.svg" alt="Students illustration"
          class="max-w-xl mb-6 py-[10px]" />
    </section>

    <!-- Right Section -->
    <section class="flex flex-col justify-center items-center w-full md:w-1/2 p-8 bg-[#f0f0f0]">
      <div class="w-full max-w-md bg-white shadow-lg rounded-2xl p-8 space-y-6">
        <!-- Logo -->
        <div class="flex justify-center">
          <!-- Logo của Edunera -->
          <img src="/images/Sec_Edunera_Logo_512.png" alt="Edunera Logo" class="h-16" />
        </div>
        <p v-if="loginError" class="text-red-500 h-5">{{ loginError }}</p>
        <!-- Login Form -->
        <form class="space-y-4" @submit.prevent="handleLogin">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700">
              Tên đăng nhập
            </label>
            <InputField id="username" v-model="username" placeholder="Nhập tên đăng nhập" />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              Mật khẩu
            </label>
            <InputField id="password" type="password" v-model="password" placeholder="Nhập mật khẩu" />
          </div>

          <nav class="flex justify-between text-sm">
            <a href="#" class="text-black hover:text-[#09f]">Đổi mật khẩu</a>
            <a href="#" class="text-black hover:text-[#09f]">Quên mật khẩu?</a>
          </nav>

          <button type="submit"
            class="w-full py-3 bg-[#09f] hover:bg-blue-600 text-white font-bold rounded-lg transition cursor-pointer">
            Đăng nhập
          </button>
        </form>

        <!-- Footer -->
        <footer class="text-center text-gray-400 text-sm">
          © 2025. Edunera. All rights reserved. Developed by Group 6
        </footer>
      </div>
    </section>
  </main>
</template>

<script setup>
import { onMounted } from "vue";
import { useAuth } from "~/composables/useAuth";

const { username, password, login, loginError, validateToken } = useAuth();

const handleLogin = async () => {
  await login();
};

// Kiểm tra nếu đã đăng nhập thì redirect
onMounted(async () => {
  if (typeof localStorage !== 'undefined') {
    const token = localStorage.getItem('token');
    if (token) {
      // Kiểm tra token hợp lệ
      const isValid = await validateToken();
      if (isValid) {
        await navigateTo('/Admin/dashboard');
        return;
      }
    }
  }
});

definePageMeta({
  layout: false
})

</script>


