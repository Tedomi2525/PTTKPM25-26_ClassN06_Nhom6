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
          <!-- Nếu có logo thì bỏ comment -->
          <img src="/images/LOGO_WITHTEXTINEN-2-1-e1740932740139-2048x722.png" alt="Logo" class="h-16" />
        </div>

        <!-- Login Form -->
        <form class="space-y-4" @submit.prevent="handleLogin">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700">
              Tên đăng nhập *
            </label>
            <input type="text" id="username" v-model="username" required autocomplete="username"
              class="mt-1 w-full border border-gray-300 rounded-lg p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              Mật khẩu *
            </label>
            <input type="password" id="password" v-model="password" required autocomplete="current-password"
              class="mt-1 w-full border border-gray-300 rounded-lg p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>

          <nav class="flex justify-between text-sm">
            <a href="#" class="text-blue-500 hover:underline">Đổi mật khẩu</a>
            <a href="#" class="text-blue-500 hover:underline">Quên mật khẩu?</a>
          </nav>

          <button type="submit"
            class="w-full py-3 bg-blue-500 hover:bg-blue-600 text-white font-bold rounded-lg transition">
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
import { ref } from "vue";
import { useRouter } from "vue-router";

const username = ref("");
const password = ref("");
const router = useRouter(); // Sử dụng Nuxt Router

const handleLogin = async () => {
  try {
    const response = await fetch("http://127.0.0.1:8000/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: username.value, password: password.value }),
    });

    if (!response.ok) throw new Error("Sai tài khoản hoặc mật khẩu!");

    const data = await response.json();
    console.log("Đăng nhập thành công:", data);

    localStorage.setItem("token", data.access_token);

    // Chuyển hướng dùng Nuxt Router
    router.push("/Admin/dashboard");
  } catch (err) {
    alert(err.message);
  }
};
</script>

