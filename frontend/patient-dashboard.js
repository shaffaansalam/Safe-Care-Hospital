document.addEventListener("DOMContentLoaded", () => {

  console.log("Patient dashboard JS loaded ✅");

  const token = localStorage.getItem("access_token");
  const storedUser = JSON.parse(localStorage.getItem("user"));

  const loginNav = document.getElementById("loginNav");
  const logoutNav = document.getElementById("logoutNav");

  // ✅ Navbar toggle
  if (token) {
    loginNav.style.display = "none";
    logoutNav.style.display = "block";
  } else {
    loginNav.style.display = "block";
    logoutNav.style.display = "none";
  }

  // ✅ Role validation
  let role = storedUser?.role;

  if (Array.isArray(role)) {
    role = role[0];
  }

  role = role?.toLowerCase().trim();

  if (!token || !storedUser || role !== "patient") {
    window.location.replace("/login/");
    return;
  }

  showToast(`Welcome ${storedUser.name} (${role})`, "#16a34a");

  // ✅ Show welcome
  document.getElementById("welcomeUser").innerHTML = `
    <p class="text-lg font-semibold text-green-600">
      Welcome, ${storedUser.name}
    </p>
  `;

  // ✅ Fetch patient data
  axios.get("http://127.0.0.1:8001/auth/dashboard/patient/", {
    headers: { Authorization: `Bearer ${token}` }
  })
  .then(res => {

    const data = res.data;

    document.getElementById("patientData").innerHTML = `
        <p><strong>Name:</strong> ${data.user.name}</p>
        <p><strong>Email:</strong> ${data.user.email}</p>
        <p><strong>Phone:</strong> ${data.phone || "N/A"}</p>
        <p><strong>Gender:</strong> ${data.gender || "N/A"}</p>
        <p><strong>Date of Birth:</strong> ${data.dob || "N/A"}</p>
        <p><strong>Blood Group:</strong> ${data.blood_group || "N/A"}</p>
    `;

  })
  .catch(() => {
    showToast("Session expired. Please login again.", "#dc2626");
    setTimeout(() => {
      localStorage.clear();
      window.location.replace("/login/");
    }, 2000);
  });

});


// ✅ GLOBAL LOGOUT FUNCTION
async function logoutUser() {

  const refreshToken = localStorage.getItem("refresh_token");
  const accessToken = localStorage.getItem("access_token");

  try {
    if (refreshToken) {
      await axios.post(
        "http://127.0.0.1:8001/auth/logout/",
        { refresh: refreshToken },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`
          }
        }
      );
    }
  } catch (error) {
    console.log("Logout API error:", error);
  }

  localStorage.clear();
  window.location.href = "/";
}


// ✅ Toast function
function showToast(message, color) {

  const toast = document.createElement("div");
  toast.innerText = message;

  toast.style.position = "fixed";
  toast.style.top = "20px";
  toast.style.right = "20px";
  toast.style.padding = "14px 22px";
  toast.style.backgroundColor = color;
  toast.style.color = "white";
  toast.style.fontWeight = "600";
  toast.style.borderRadius = "8px";
  toast.style.boxShadow = "0 5px 15px rgba(0,0,0,0.2)";
  toast.style.zIndex = "9999";
  toast.style.opacity = "0";
  toast.style.transition = "opacity 0.4s ease";

  document.body.appendChild(toast);

  setTimeout(() => toast.style.opacity = "1", 100);

  setTimeout(() => {
    toast.style.opacity = "0";
    setTimeout(() => toast.remove(), 400);
  }, 3000);
}