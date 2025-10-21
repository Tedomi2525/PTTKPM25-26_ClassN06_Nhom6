<script setup>
definePageMeta({
  layout: "default",
});
</script>

<template>
  <div>
    <!-- Hero / Giới thiệu -->
    <div class="max-w-5xl mx-auto mt-6">
      <!-- Danh sách tin tức -->
      <section class="max-w-6xl mx-auto px-4 section-content mt-5">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Tin lớn bên trái -->
          <div class="bg-white shadow-lg rounded overflow-hidden">
            <div class="relative h-[320px]">
              <NuxtLink
                to="/vi/post/tin-tuc/tin-tuc/tin-tuc-thong-bao/phenikaa-chinh-thuc-tro-thanh-dai-hoc-dau-moc-chien-luoc-khang-dinh-mo-hinh-dai-hoc-doi-moi-sang-tao">
                <img
                  src="https://phenikaa-uni.edu.vn:3600/pu/vi/posts/52298768911997254255255696891619064628533755n.jpg"
                  alt="Phenikaa chính thức trở thành Đại học" class="w-full h-full object-cover" />
              </NuxtLink>
              <div class="absolute bottom-0 right-0 bg-sky-500 text-white text-center px-3 py-2">
                <div class="font-bold text-xl">22</div>
                <div class="h-px bg-white my-1"></div>
                <div class="text-sm">Tháng 7</div>
              </div>
            </div>
            <div class="p-4 flex flex-col justify-between h-[calc(100%-320px)]">
              <div>
                <NuxtLink
                  to="/vi/post/tin-tuc/tin-tuc/tin-tuc-thong-bao/phenikaa-chinh-thuc-tro-thanh-dai-hoc-dau-moc-chien-luoc-khang-dinh-mo-hinh-dai-hoc-doi-moi-sang-tao"
                  class="block text-lg font-semibold mb-2 hover:text-blue-600">
                  Phenikaa chính thức trở thành Đại học: Dấu mốc chiến lược, khẳng định mô hình đại học đổi mới sáng tạo
                </NuxtLink>
                <p class="text-gray-600 text-sm line-clamp-3">
                  Ngày 22/7/2025, Tập đoàn Phenikaa, Đại học Phenikaa long trọng tổ chức Lễ công bố
                  Quyết định chuyển Trường Đại học Phenikaa thành Đại học Phenikaa và Chiến lược đột
                  phá phát triển. Sự kiện được xem là dấu mốc quan trọng, đánh dấu bước chuyển mình
                  mạnh mẽ của Đại học Phenikaa...
                </p>
              </div>
              <NuxtLink
                to="/vi/post/tin-tuc/tin-tuc/tin-tuc-thong-bao/phenikaa-chinh-thuc-tro-thanh-dai-hoc-dau-moc-chien-luoc-khang-dinh-mo-hinh-dai-hoc-doi-moi-sang-tao"
                class="mt-3 inline-flex items-center text-sm text-gray-500 hover:text-blue-600">
                Xem thêm →
              </NuxtLink>
            </div>
          </div>

          <!-- Tin nhỏ bên phải -->
          <div class="flex flex-col gap-6">
            <!-- Tin nhỏ 1 -->
            <div class="flex bg-white shadow p-3 rounded h-[170px]">
              <div class="w-1/2">
                <NuxtLink
                  to="/vi/post/tin-tuc/tin-tuc/tin-tuc-thong-bao/dai-hoc-phenikaa-co-4-nha-khoa-hoc-vao-top-100000-nha-khoa-hoc-anh-huong-nhat-the-gioi-2024">
                  <img src="https://phenikaa-uni.edu.vn:3600/pu/vi/posts/4-nha-khoa-hoc-phenikaa-01.jpg"
                    class="w-full h-full object-cover rounded" alt="Top 100000 nhà khoa học" />
                </NuxtLink>
              </div>
              <div class="w-1/2 pl-3 flex flex-col justify-between">
                <span class="text-gray-400 text-xs">30, tháng 9, 2025</span>
                <NuxtLink
                  to="/vi/post/tin-tuc/tin-tuc/tin-tuc-thong-bao/dai-hoc-phenikaa-co-4-nha-khoa-hoc-vao-top-100000-nha-khoa-hoc-anh-huong-nhat-the-gioi-2024"
                  class="text-sm font-semibold hover:text-blue-600 line-clamp-3">
                  Đại học Phenikaa có 4 nhà khoa học vào Top 100.000 nhà khoa học ảnh hưởng nhất thế giới 2024
                </NuxtLink>
                <NuxtLink
                  to="/vi/post/tin-tuc/tin-tuc/tin-tuc-thong-bao/dai-hoc-phenikaa-co-4-nha-khoa-hoc-vao-top-100000-nha-khoa-hoc-anh-huong-nhat-the-gioi-2024"
                  class="text-xs text-gray-500 hover:text-blue-600">
                  Xem thêm →
                </NuxtLink>
              </div>
            </div>

            <!-- Tin nhỏ 2 -->
            <div class="flex bg-white shadow p-3 rounded h-[170px]">
              <div class="w-1/2">
                <NuxtLink
                  to="/vi/post/tin-tuc/tin-tuc/tin-tuc-thong-bao/sinh-vien-truong-y-duoc-phenikaa-gop-suc-xay-dung-cong-dong-khoe-manh">
                  <img
                    src="https://phenikaa-uni.edu.vn:3600/pu/vi/posts/z70613157091150859ee593af845909453e471b2bf7e79.jpg"
                    class="w-full h-full object-cover rounded" alt="Sinh viên Trường Y - Dược" />
                </NuxtLink>
              </div>
              <div class="w-1/2 pl-3 flex flex-col justify-between">
                <span class="text-gray-400 text-xs">29, tháng 9, 2025</span>
                <NuxtLink
                  to="/vi/post/tin-tuc/tin-tuc/tin-tuc-thong-bao/sinh-vien-truong-y-duoc-phenikaa-gop-suc-xay-dung-cong-dong-khoe-manh"
                  class="text-sm font-semibold hover:text-blue-600 line-clamp-3">
                  Sinh viên Trường Y - Dược Phenikaa góp sức xây dựng cộng đồng khỏe mạnh
                </NuxtLink>
                <NuxtLink
                  to="/vi/post/tin-tuc/tin-tuc/tin-tuc-thong-bao/sinh-vien-truong-y-duoc-phenikaa-gop-suc-xay-dung-cong-dong-khoe-manh"
                  class="text-xs text-gray-500 hover:text-blue-600">
                  Xem thêm →
                </NuxtLink>
              </div>
            </div>

            <!-- Tin nhỏ 3 -->
            <div class="flex bg-white shadow p-3 rounded h-[170px]">
              <div class="w-1/2">
                <NuxtLink
                  to="/vi/post/tin-tuc/tin-tuc/tin-tuc-thong-bao/giang-vien-truong-cong-nghe-thong-tin-phenikaa-cong-bo-nghien-cuu-tai-hoi-nghi-ai-hoc-may-uy-tin-nhat-the-gioi">
                  <img src="https://phenikaa-uni.edu.vn:3600/pu/vi/posts/pka03891.jpg"
                    class="w-full h-full object-cover rounded" alt="Giảng viên CNTT Phenikaa công bố nghiên cứu" />
                </NuxtLink>
              </div>
              <div class="w-1/2 pl-3 flex flex-col justify-between">
                <span class="text-gray-400 text-xs">26, tháng 9, 2025</span>
                <NuxtLink
                  to="/vi/post/tin-tuc/tin-tuc/tin-tuc-thong-bao/giang-vien-truong-cong-nghe-thong-tin-phenikaa-cong-bo-nghien-cuu-tai-hoi-nghi-ai-hoc-may-uy-tin-nhat-the-gioi"
                  class="text-sm font-semibold hover:text-blue-600 line-clamp-3">
                  Giảng viên Trường CNTT Phenikaa công bố nghiên cứu tại hội nghị AI – Học máy uy tín nhất thế giới
                </NuxtLink>
                <NuxtLink
                  to="/vi/post/tin-tuc/tin-tuc/tin-tuc-thong-bao/giang-vien-truong-cong-nghe-thong-tin-phenikaa-cong-bo-nghien-cuu-tai-hoi-nghi-ai-hoc-may-uy-tin-nhat-the-gioi"
                  class="text-xs text-gray-500 hover:text-blue-600">
                  Xem thêm →
                </NuxtLink>
              </div>
            </div>
          </div>
        </div>

        <!-- Nút xem thêm -->
        <div class="text-center mt-6">
          <NuxtLink to="/vi/category/tin-tuc"
            class="inline-block bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 transition">
            Xem thêm
          </NuxtLink>
        </div>
      </section>

    </div>

    <!-- Footer -->
    <footer class="bg-[#335f87] text-white py-10 mt-12">
      <div class="container mx-auto px-4 grid grid-cols-1 md:grid-cols-4 gap-6">
        <!-- Cột Giáo dục -->
        <div>
          <h5 class="font-bold uppercase mb-3">Giáo dục</h5>
          <ul class="space-y-2">
            <li><a href="/vi/category/dam-bao-chat-luong/ba-cong-khai" class="hover:underline">Ba công khai</a></li>
            <li><a href="/vi/page/tra-cuu-van-bang" class="hover:underline">Tra cứu văn bằng</a></li>
            <li><a href="/vi/doc" class="hover:underline">Văn bản</a></li>
          </ul>

          <h5 class="font-bold uppercase mt-6 mb-3">Đơn vị trực thuộc</h5>
          <ul class="space-y-2">
            <li><a href="/vi/page/lien-he" class="hover:underline">Khoa - Trường</a></li>
            <li><a href="/vi/page/lien-he" class="hover:underline">Viện - Trung tâm</a></li>
            <li><a href="/vi/page/lien-he" class="hover:underline">Phòng - Ban</a></li>
          </ul>
        </div>

        <!-- Cột Khoa học -->
        <div>
          <h5 class="font-bold uppercase mb-3">Khoa học công nghệ</h5>
          <ul class="space-y-2">
            <li><a href="/vi/page/cong-bo-khoa-hoc" class="hover:underline">Bài báo ISI/SCOPUS</a></li>
            <li><a href="/vi/post/khoa-hoc-cong-nghe/sang-che-giai-phap-huu-ich/sang-chegiai-phap-huu-ich"
                class="hover:underline">Sáng chế/Giải pháp hữu ích</a></li>
            <li><a href="#" class="hover:underline">Tạp chí khoa học</a></li>
            <li><a href="#" class="hover:underline">Quỹ Khoa học - Công nghệ</a></li>
          </ul>

          <h5 class="font-bold uppercase mt-6 mb-3">Thông tin</h5>
          <ul class="space-y-2">
            <li><a href="/vi/page/lien-he" class="hover:underline">Liên hệ</a></li>
            <li><a href="/vi/category/tuyen-dung" class="hover:underline">Tuyển dụng</a></li>
            <li><a href="#" class="hover:underline">Trải nghiệm</a></li>
            <li><a href="#" class="hover:underline">Sơ đồ trang</a></li>
          </ul>
        </div>

        <!-- Cột Liên hệ -->
        <div class="col-span-2">
          <ul class="space-y-3">
            <li><strong>Địa chỉ:</strong> Đường Nguyễn Trác - Phường Dương Nội - Hà Nội</li>
            <li><strong>Điện thoại:</strong> 024.62918118 | Hotline: 0946511010 - 0969511010 - 0967511010</li>
            <li><strong>Email:</strong> <a href="mailto:Info@phenikaa-uni.edu.vn"
                class="hover:underline">Info@phenikaa-uni.edu.vn</a></li>
            <li>
              <iframe frameborder="0" height="200"
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3725.7845880567393!2d105.74434161492857!3d20.96116409545836!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x313452efff394ce3%3A0x391a39d4325be464!2zVHLGsOG7nW5nIMSQ4bqhaSBo4buNYyBQSEVOSUtBQQ!5e0!3m2!1svi!2s!4v1569472101892!5m2!1svi!2s"
                width="100%"></iframe>
            </li>
          </ul>
        </div>
      </div>

      <!-- Mạng xã hội -->
      <div class="container mx-auto px-4 mt-8">
        <h2 class="font-bold uppercase mb-3">Theo dõi chúng tôi</h2>
        <div class="flex space-x-4">
          <a href="https://www.facebook.com/Daihocphenikaa" target="_blank">📘 Facebook</a>
          <a href="https://www.youtube.com/c/PhenikaaUniversity" target="_blank">▶️ YouTube</a>
          <a href="https://www.tiktok.com/@phenikaa_university" target="_blank">🎵 TikTok</a>
          <a href="https://www.linkedin.com/company/phenikaa-university1/posts/?feedView=all" target="_blank">💼
            LinkedIn</a>
        </div>
      </div>

      <!-- Bản quyền -->
      <div class="text-center mt-6 text-sm italic">
        Copyright © 2025 Đại học PHENIKAA
      </div>
    </footer>
  </div>
</template>
