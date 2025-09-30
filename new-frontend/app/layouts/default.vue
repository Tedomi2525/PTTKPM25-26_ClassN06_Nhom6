<template>
  <div class="bg-gray-100 min-h-screen">
    <!-- HEADER / NAVBAR -->
    <nav class="bg-[#09f] text-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <!-- Logo -->
          <NuxtLink to="/" class="text-xl font-bold">Hệ thống Quản lý</NuxtLink>

          <!-- Menu -->
          <div class="hidden md:flex space-x-6">
            <!-- Dropdown Danh sách -->
            <div class="relative group inline-block">
              <button class="flex items-center gap-1 hover:text-gray-300">
                Danh sách
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              <ul
                class="absolute left-0 top-full mt-0 hidden group-hover:block bg-white text-gray-800 rounded shadow-lg z-10 min-w-[150px]">
                <li>
                  <NuxtLink to="/Admin/student_list" class="block px-4 py-2 hover:bg-gray-100">
                    Sinh viên
                  </NuxtLink>
                </li>
                <li>
                  <NuxtLink to="/Admin/teacher_list" class="block px-4 py-2 hover:bg-gray-100">
                    Giảng viên
                  </NuxtLink>
                </li>
                <li>
                  <NuxtLink to="/Admin/account_list" class="block px-4 py-2 hover:bg-gray-100">
                    Tài khoản
                  </NuxtLink>
                </li>
              </ul>
            </div>

            <NuxtLink to="/Admin/student_add" class="hover:text-gray-300">Thêm sinh viên</NuxtLink>
            <NuxtLink to="/Admin/teacher_add" class="hover:text-gray-300">Thêm giảng viên</NuxtLink>
          </div>

          <!-- User Dropdown -->
          <div class="relative group">
            <button class="px-3 py-1 rounded hover:text-gray-300">
              Xin chào, Admin
            </button>
            <ul class="absolute right-0 hidden group-hover:block bg-white text-gray-800 mt-2 rounded shadow-lg">
              <li>
                <NuxtLink to="/sign-in" class="block px-4 py-2 text-red-600 hover:bg-gray-100">
                  Đăng xuất
                </NuxtLink>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </nav>

    <!-- MAIN CONTENT -->
    <main>
        <slot />
    </main>
  </div>
</template>
