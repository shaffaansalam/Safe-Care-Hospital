document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("access");

  const loginNav = document.getElementById("loginNav");
  const logoutNav = document.getElementById("logoutNav");
  const registerNav = document.getElementById("registerNav");

  if (loginNav && logoutNav) {
    if (token) {
      loginNav.style.display = "none";
      logoutNav.style.display = "block";

      const notificationNav = document.getElementById("notificationNav");

      if (notificationNav) {
        notificationNav.style.display = "block";
      }

      if (registerNav) {
        registerNav.style.display = "none";
      }
    } else {
      loginNav.style.display = "block";
      logoutNav.style.display = "none";

      if (registerNav) {
        registerNav.style.display = "block";
      }
    }
  }

  const menuToggle = document.getElementById("menuToggle");
  const mobileNav = document.getElementById("mobileNav");

  if (menuToggle && mobileNav) {
    menuToggle.addEventListener("click", () => {
      mobileNav.classList.toggle("active");
    });
  }
});

function logoutUser() {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
  localStorage.removeItem("user");
  localStorage.removeItem("role");
  localStorage.removeItem("appointment_id");

  window.location.href = "login.html";
}
