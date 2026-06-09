document.addEventListener("DOMContentLoaded", () => {
  // console.log("✅ JS Loaded");

  const loginForm = document.getElementById("loginForm");
  const errorMsg = document.getElementById("errorMsg");

  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    // console.log("🚀 Form submitted properly");

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

      const { access, refresh, user, role } = response.data;

      // STORE TOKENS
      localStorage.setItem("access", access);
      localStorage.setItem("refresh", refresh);
      console.log("TOKEN SAVED:", localStorage.getItem("access"));

      localStorage.setItem("user", JSON.stringify(user));
      localStorage.setItem("role", role);
      localStorage.setItem("isLoggedIn", "true");

      // console.log("💾 Tokens stored successfully");

      const userRole = role?.toLowerCase().trim();

      // console.log("🎯 Redirecting as:", userRole);

      // ROLE BASED REDIRECT
      if (userRole === "patient") {

        window.location.href = "patient-dashboard.html";

      } 
      else if (userRole === "doctor") {

        window.location.href = "doctor-dashboard.html";

      } 
      else if (userRole === "admin") {

        window.location.href = "admin/admin-dashboard.html";

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

      } 
      else {

        errorMsg.innerText = "Server not reachable.";

      }

    }

  });

});

