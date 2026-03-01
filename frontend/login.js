

document.addEventListener("DOMContentLoaded", () => {
  console.log("✅ JS Loaded");

  const loginForm = document.getElementById("loginForm");
  const errorMsg = document.getElementById("errorMsg");

  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault(); // 🔥 THIS stops page reload completely

    console.log("🚀 Form submitted properly");

    errorMsg.classList.add("hidden");

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!email || !password) {
      errorMsg.classList.remove("hidden");
      errorMsg.innerText = "Email and password are required.";
      return;
    }

    try {
      const response = await axios.post(
        "http://127.0.0.1:8001/auth/login/",
        { email, password }
      );

      console.log("✅ Login Success:", response.data);

      const { access, refresh, user } = response.data;

      localStorage.setItem("access_token", access);
      localStorage.setItem("refresh_token", refresh);
      localStorage.setItem("user", JSON.stringify(user));
      localStorage.setItem("isLoggedIn", "true");

      console.log("💾 Tokens stored successfully");
      console.log("ACCESS TOKEN:", access);
      console.log("REFRESH TOKEN:", refresh);
      console.log("USER:", user);

      let role = user.role;

      if (Array.isArray(role)) {
        role = role[0];
      }

      role = role?.toLowerCase().trim();

      console.log("🎯 Redirecting as:", role);

      
      if (role === "patient") {
        window.location.href = "patient-dashboard.html";
      } 
      else if (role === "doctor") {
        window.location.href = "doctor-dashboard.html";
      } 
      else {
        window.location.href = "home.html";
      }
     
    
    } catch (error) {
      console.error("❌ Login Failed:", error);
      errorMsg.classList.remove("hidden");

      if (error.response) {
        errorMsg.innerText =
          error.response.data.message ||
          error.response.data.non_field_errors?.[0] ||
          "Invalid credentials.";
      } else {
        errorMsg.innerText = "Server not reachable.";
      }
    }
  });
});






