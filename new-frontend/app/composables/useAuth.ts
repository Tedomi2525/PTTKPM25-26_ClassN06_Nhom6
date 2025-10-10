import { ref } from "vue";
import { useRouter } from "vue-router";

export function useAuth() {
  const username = ref("");
  const password = ref("");
  const router = useRouter();
  const loginError = ref("");
  const token = useCookie<string | null>("token");
  const fullNameCookie = useCookie("full_name");

  const displayName = ref("Admin");
  const role = ref("");
  const schoolId = ref("");

  // ✅ Khôi phục từ localStorage nếu có
  if (typeof window !== "undefined") {
    const storedToken = localStorage.getItem("token");
    const storedFullName = localStorage.getItem("fullName");
    const storedRole = localStorage.getItem("role");
    const storedSchoolId = localStorage.getItem("schoolId");

    if (storedToken) token.value = storedToken;
    if (storedFullName) {
      displayName.value = storedFullName;
      fullNameCookie.value = storedFullName;
    }
    if (storedRole) role.value = storedRole;
    if (storedSchoolId) schoolId.value = storedSchoolId;
  }

  // ✅ Hàm lưu token vào cookie + localStorage
  const setToken = (value: string) => {
    token.value = value;
    if (typeof window !== "undefined") {
      localStorage.setItem("token", value);
    }
  };

  // ✅ Đăng nhập
  const login = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: username.value,
          password: password.value,
        }),
      });

      if (!res.ok) throw new Error("Sai tài khoản hoặc mật khẩu");

      const data = await res.json();
      const accessToken = data.accessToken || data.access_token;
      if (!accessToken) throw new Error("Không nhận được access token từ server");

      setToken(accessToken);

      // Lấy thông tin người dùng
      const meRes = await fetch("http://127.0.0.1:8000/auth/me", {
        method: "GET",
        headers: { Authorization: `Bearer ${accessToken}` },
      });

      if (!meRes.ok) throw new Error("Không thể lấy thông tin người dùng");

      const meData = await meRes.json();

      const fullName = meData.fullName || meData.full_name;
      const userRole = meData.role || meData.user_role || "user";
      const school = meData.schoolId || meData.school_id || "";

      // ✅ Lưu toàn bộ vào cookie + localStorage
      fullNameCookie.value = fullName;
      displayName.value = fullName;
      role.value = userRole;
      schoolId.value = school;

      if (typeof window !== "undefined") {
        localStorage.setItem("fullName", fullName);
        localStorage.setItem("role", userRole);
        localStorage.setItem("schoolId", school);
      }

      console.log(`👤 ${fullName} (${userRole}) - School ID: ${school}`);
      router.push("/Home");
    } catch (err) {
      loginError.value = "Sai thông tin đăng nhập";
      console.error("Login error:", err);
    }
  };

  // ✅ Đăng xuất
  const logout = () => {
    token.value = "";
    fullNameCookie.value = "";
    displayName.value = "Admin";
    role.value = "";
    schoolId.value = "";

    if (typeof window !== "undefined") {
      localStorage.removeItem("token");
      localStorage.removeItem("fullName");
      localStorage.removeItem("role");
      localStorage.removeItem("schoolId");
    }

    router.push("/");
  };

  // ✅ Xác thực token khi reload
  const validateToken = async () => {
    if (!token.value) return false;
    try {
      const res = await fetch("http://127.0.0.1:8000/auth/me", {
        method: "GET",
        headers: { Authorization: `Bearer ${token.value}` },
      });

      if (res.ok) {
        const data = await res.json();
        const fullName = data.fullName || data.full_name;
        const userRole = data.role || data.user_role || "user";
        const school = data.schoolId || data.school_id || "";

        fullNameCookie.value = fullName;
        displayName.value = fullName;
        role.value = userRole;
        schoolId.value = school;

        if (typeof window !== "undefined") {
          localStorage.setItem("fullName", fullName);
          localStorage.setItem("role", userRole);
          localStorage.setItem("schoolId", school);
        }

        console.log("✅ Token hợp lệ - user:", fullName);
        return true;
      }
      return false;
    } catch (error) {
      console.error("❌ Token validation failed:", error);
      return false;
    }
  };

  const isAuthenticated = () => !!token.value;

  return {
    username,
    password,
    token,
    login,
    logout,
    isAuthenticated,
    loginError,
    displayName,
    fullNameCookie,
    validateToken,
    role,
    schoolId,
  };
}
