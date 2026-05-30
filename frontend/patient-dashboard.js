

const token = localStorage.getItem("access_token");
const storedUser = JSON.parse(localStorage.getItem("user"));

document.addEventListener("DOMContentLoaded", () => {

  console.log("Patient dashboard JS loaded ✅");

  const loginNav = document.getElementById("loginNav");
  const logoutNav = document.getElementById("logoutNav");
  const registerNav = document.getElementById("registerNav");

  // NAVBAR TOGGLE
if (token) {

  loginNav.style.display = "none";

  logoutNav.style.display = "block";

  registerNav.style.display = "none";

} else {

  loginNav.style.display = "block";

  logoutNav.style.display = "none";

  registerNav.style.display = "block";
}

  // ROLE VALIDATION
  let role = storedUser?.role;

  if (Array.isArray(role)) {
    role = role[0];
  }

  role = role?.toLowerCase().trim();

  if (!token || !storedUser || role !== "patient") {

    window.location.href = "login.html";

    return;
  }

  showToast(`Welcome Patient : ${storedUser.name}`, "#16a34a");

  document.getElementById("welcomeUser").innerHTML = `

    <p class="text-lg font-semibold text-green-600">
      Welcome, ${storedUser.name}
    </p>

  `;

  loadPatientDashboard();
  loadPrescriptions();
  loadTests();
  loadReports();
});



// =====================================
// LOAD PATIENT DASHBOARD
// =====================================

async function loadPatientDashboard() {

  try {

    const response = await axios.get(

      "http://127.0.0.1:8001/auth/dashboard/patient/",

      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );

    const data = response.data;

    let imageUrl = data.profile_image;

    if (imageUrl && !imageUrl.startsWith("http")) {

      imageUrl = `http://127.0.0.1:8001${imageUrl}`;

    } else if (!imageUrl) {

      imageUrl =
        "https://ui-avatars.com/api/?name=" + data.user.name;
    }

    document.getElementById("patientData").innerHTML = `

      <p><strong>Name :</strong> ${data.user.name}</p>

      <p><strong>Email :</strong> ${data.user.email}</p>

      <p><strong>Phone :</strong> ${data.phone || "N/A"}</p>

      <p><strong>Gender :</strong> ${data.gender || "N/A"}</p>

      <p><strong>Age :</strong> ${data.age || "N/A"}</p>

      <p><strong>Blood Group :</strong> ${data.blood_group || "N/A"}</p>

      <p><strong>Address :</strong> ${data.address || "N/A"}</p>

      <p><strong>Medical History :</strong> ${data.medical_history || "N/A"}</p>

      <img
        src="${imageUrl}"
        class="w-32 h-32 rounded-full object-cover border mt-4"
      />

    `;

  } catch(error) {

    console.log(error);

    alert("Failed to load patient dashboard");
  }
}



// =====================================
// LOAD PRESCRIPTIONS
// =====================================

async function loadPrescriptions() {

  try {

    const response = await axios.get(

      "http://127.0.0.1:8001/auth/patient/prescriptions/",

      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );

    let html = "";

    response.data.forEach(item => {

      html += `

      <div class="border p-4 rounded mb-4">

        <p>
          <strong>Diagnosis:</strong>
          ${item.diagnosis}
        </p>

        <p>
          <strong>Medicines:</strong>
          ${item.medicines}
        </p>

        <p>
          <strong>Notes:</strong>
          ${item.notes}
        </p>

      </div>

      `;
    });

    document.getElementById(
      "prescriptionsContainer"
    ).innerHTML = html;

  } catch(error) {

    console.log(error);

    alert("Failed to load prescriptions");
  }
}



// =====================================
// LOAD TEST REQUESTS
// =====================================

async function loadTests() {

  try {

    const response = await axios.get(

      "http://127.0.0.1:8001/auth/patient/test-requests/",

      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );

    let html = "";

    response.data.forEach(item => {

      html += `

      <div class="border p-4 rounded mb-4">

        <p>
          <strong>Test:</strong>
          ${item.test_name}
        </p>

        <p>
          <strong>Instructions:</strong>
          ${item.instructions}
        </p>

        <p>
          <strong>Status:</strong>
          ${item.status}
        </p>

        <p>
          <strong>Test Request ID:</strong>
          ${item.id}
        </p>

      </div>

      `;
    });

    document.getElementById(
      "testsContainer"
    ).innerHTML = html;

  } catch(error) {

    console.log(error);

    alert("Failed to load tests");
  }
}



// =====================================
// UPLOAD REPORT
// =====================================

async function uploadReport() {

  const file =
    document.getElementById("reportFile").files[0];

  const report_title =
    document.getElementById("reportTitle").value;

  const testRequestId =
    document.getElementById("testRequestId").value;

  if (!file || !report_title || !testRequestId) {

    alert("Please fill all fields");

    return;
  }

  const formData = new FormData();

  formData.append("report_title", report_title);

  formData.append("report_file", file);

  try {

    await axios.post(

      `http://127.0.0.1:8001/auth/patient/upload-report/${testRequestId}/`,

      formData,

      {
        headers: {

          Authorization: `Bearer ${token}`,

          "Content-Type": "multipart/form-data"
        }
      }
    );

    alert("Report Uploaded Successfully");

    loadReports();
    

  } catch(error) {

    console.log(error);

    console.log(error.response?.data);

    alert("Upload Failed");
  }
}



// =====================================
// LOAD REPORTS
// =====================================

async function loadReports() {

  try {

    const response = await axios.get(

      "http://127.0.0.1:8001/auth/patient/reports/",

      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );

    let html = "";

    response.data.forEach(report => {

      let reportUrl = report.report_file;

      if (reportUrl && !reportUrl.startsWith("http")) {

        reportUrl =
          `http://127.0.0.1:8001${reportUrl}`;
      }

      html += `

      <div class="border p-4 rounded mb-4">

        <p class="font-bold">
          ${report.report_title}
        </p>

        <a
          href="${reportUrl}"
          target="_blank"
          class="text-blue-600 underline">

          View Report

        </a>

      </div>

      `;
    });

    document.getElementById(
      "reportsContainer"
    ).innerHTML = html;

  } catch(error) {

    console.log(error);

    alert("Failed to load reports");
  }
}



// =====================================
// LOGOUT
// =====================================

async function logoutUser() {

  const refreshToken =
    localStorage.getItem("refresh_token");

  try {

    await axios.post(

      "http://127.0.0.1:8001/auth/logout/",

      {
        refresh: refreshToken
      },

      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );

  } catch(error) {

    console.log(error);
  }

  localStorage.clear();

  window.location.href = "login.html";
}



// =====================================
// TOAST
// =====================================

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
  toast.style.zIndex = "9999";

  document.body.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 3000);
}

