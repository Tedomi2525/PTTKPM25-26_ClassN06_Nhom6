import { ref } from "vue";
import { useRouter } from "vue-router";

export function useAuth() {
  const username = ref("")
  const password = ref("")
  const router = useRouter()
  const loginError = ref("")
  const token = useCookie<string | null>("token")
  const fullNameCookie = useCookie("full_name") // chỉ lưu cookie
  const role = ref(""); // thêm reactive cho role
  const displayName = ref("Admin")               // reactive cho template
  const schoolId = ref("")                // reactive cho template

  // Khởi tạo token từ localStorage nếu cookie trống
  if (typeof window !== 'undefined' && !token.value) {
    const storedToken = localStorage.getItem("token")
    if (storedToken) {
      token.value = storedToken
    }
  }

  // Khởi tạo displayName từ cookie nếu có
  if (fullNameCookie.value) {
    displayName.value = fullNameCookie.value
  }

  const setToken = (value: string) => {
    token.value = value  // lưu token vào cookie
    // Đồng bộ với localStorage để tương thích
    if (typeof window !== 'undefined') {
      localStorage.setItem("token", value)
    }
  }

const login = async () => {
  try {
    const res = await fetch("http://127.0.0.1:8000/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: username.value, password: password.value }),
    });

    if (!res.ok) throw new Error("Sai tài khoản hoặc mật khẩu");

    const { accessToken, access_token } = await res.json();
    const token = accessToken || access_token;
    if (!token) throw new Error("Không nhận được access token từ server");

    setToken(token);

    // 🧠 Gọi /auth/me để lấy thông tin người dùng
    const meRes = await fetch("http://127.0.0.1:8000/auth/me", {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!meRes.ok) throw new Error("Không thể lấy thông tin người dùng");

    const meData = await meRes.json();
    console.log("✅ /auth/me:", meData);

    // 🔄 Chuẩn hóa dữ liệu (camelCase / snake_case)
    const normalize = (obj, keys) => keys.find(k => obj[k] !== undefined) && obj[keys.find(k => obj[k] !== undefined)];
    const fullName = normalize(meData, ["fullName", "full_name"]) || "Người dùng";
    const userRole = normalize(meData, ["role", "user_role"]) || "user";
    const schoolIdVal = normalize(meData, ["school_id", "schoolId"]) || null;

    // 💾 Lưu thông tin
    fullNameCookie.value = fullName;
    displayName.value = fullName;
    role.value = userRole;
    schoolId.value = schoolIdVal;

    console.log(`👤 ${fullName} (${userRole}) - School ID: ${schoolIdVal}`);

    router.push("/Home");
  } catch (err) {
    console.error("❌ Login error:", err);
    loginError.value = "Sai thông tin đăng nhập";
  }
};


  const logout = () => {
    token.value = "";
    fullNameCookie.value = "";
    displayName.value = "Admin";
    role.value = "";
    if (typeof window !== 'undefined') {
      localStorage.removeItem("token");
    }
    router.push("/");
  };

  const validateToken = async () => {
    if (!token.value) return false;
    
    try {
      const res = await fetch("http://127.0.0.1:8000/auth/me", {
        method: "GET",
        headers: { Authorization: `Bearer ${token.value}` }
      });
      
      if (res.ok) {
        const data = await res.json();
        const fullName = data.fullName || data.full_name;
        const userRole = data.role || data.user_role || "user";
        
        fullNameCookie.value = fullName;
        displayName.value = fullName;
        role.value = userRole;
        
        console.log("validateToken - role:", userRole);
        return true;
      }
      return false;
    } catch (error) {
      console.error("Token validation failed:", error);
      return false;
    }
  };

  const isAuthenticated = () => !!token.value;

  return { username, password, token, login, logout, isAuthenticated, loginError, displayName, fullNameCookie, validateToken, role, schoolId };
}
