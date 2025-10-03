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
    })

    if (!res.ok) throw new Error("Sai tài khoản hoặc mật khẩu")

    const data = await res.json()
    const accessToken = data.accessToken || data.access_token  // hỗ trợ cả camelCase và snake_case
    
    if (!accessToken) {
      throw new Error("Không nhận được access token từ server")
    }
    
    setToken(accessToken)

    // Gọi API /me để lấy thông tin user
    console.log("Making /auth/me request with token:", accessToken)
    const meRes = await fetch("http://127.0.0.1:8000/auth/me", {
      method: "GET",
      headers: { Authorization: `Bearer ${accessToken}` }
    })

    console.log("/auth/me response status:", meRes.status)
    console.log("/auth/me response headers:", Object.fromEntries(meRes.headers.entries()))

    if (!meRes.ok) {
      const errorText = await meRes.text()
      console.error("/auth/me error response:", errorText)
      throw new Error("Không thể lấy thông tin người dùng")
    }

    const meData = await meRes.json()
    console.log("Full /auth/me response:", meData)
    console.log("typeof meData:", typeof meData)
    console.log("meData keys:", Object.keys(meData))
    
    const fullName = meData.fullName || meData.full_name  // hỗ trợ cả camelCase và snake_case
    const userRole = meData.role || meData.user_role || "user"  // hỗ trợ cả camelCase và snake_case
    
    fullNameCookie.value = fullName  // lưu cookie
    displayName.value = fullName     // cập nhật display
    role.value = userRole            // cập nhật role

    console.log("displayName.value:", displayName.value)
    console.log("fullNameCookie.value:", fullNameCookie.value)
    console.log("fullName extracted:", fullName)
    console.log("role extracted:", userRole)

    router.push("/Home")

  } catch (err) {
    loginError.value = "Sai thông tin đăng nhập"
    console.error("Login error:", err)
  }
}

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

  return { username, password, token, login, logout, isAuthenticated, loginError, displayName, fullNameCookie, validateToken, role };
}
