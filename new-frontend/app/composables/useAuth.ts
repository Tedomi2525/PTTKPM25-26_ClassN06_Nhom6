import { ref } from "vue";
import { useRouter } from "vue-router";

export function useAuth() {
  const username = ref("");
  const password = ref("");
  const router = useRouter();
  const token = ref(localStorage.getItem("token") || "");
  const loginError = ref("");

  const login = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: username.value, password: password.value }),
      });

      if (!res.ok) throw new Error("Sai tài khoản hoặc mật khẩu!");

      const data = await res.json();
      token.value = data.access_token;
      localStorage.setItem("token", token.value);

      router.push("/Admin/dashboard");
    } catch (err: unknown) {
      // You'll need to emit an error or use a reactive error state
      // Add this at the top of useAuth function:
      // const loginError = ref("");
      
      // Then replace the alert with:
      loginError.value = "Sai thông tin đăng nhập";
    }
  };

  const logout = () => {
    token.value = "";
    localStorage.removeItem("token");
    router.push("/login");
  };

  const isAuthenticated = () => !!token.value;

  return { username, password, token, login, logout, isAuthenticated, loginError };
}
