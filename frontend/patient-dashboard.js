const token = localStorage.getItem("access");
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
          Authorization: `Bearer ${token}`,
        },
      },
    );

    const patient = response.data;

    

    let imageUrl = patient.profile_image;

    if (imageUrl && !imageUrl.startsWith("http")) {
      imageUrl = `http://127.0.0.1:8001${imageUrl}`;
    }

    if (!imageUrl) {
      imageUrl = `https://ui-avatars.com/api/?name=${patient.user.name}`;
    }

    document.getElementById("patientData").innerHTML = `

<div class="row align-items-center">

    <div class="col-lg-3 text-center">

        <img
            src="${imageUrl}"
            style="
                width:180px;
                height:180px;
                border-radius:50%;
                object-fit:cover;
                border:4px solid #2563eb;
            "
        >

    </div>

    <div class="col-lg-9">

        <h2 class="mb-3">
            ${patient.user.name}
        </h2>

        <p>
            <strong>Email :</strong>
            ${patient.user.email}
        </p>

        <p>
            <strong>Phone :</strong>
            ${patient.phone || "N/A"}
        </p>

        <p>
            <strong>Gender :</strong>
            ${patient.gender || "N/A"}
        </p>

        <p>
            <strong>DOB :</strong>
            ${patient.dob || "N/A"}
        </p>

        <p>
            <strong>Blood Group :</strong>
            ${patient.blood_group || "N/A"}
        </p>

        <p>
            <strong>Address :</strong>
            ${patient.address || "N/A"}
        </p>

        <p>
            <strong>Medical History :</strong>
            ${patient.medical_history || "None"}
        </p>

        <button
            class="btn btn-primary mt-3"
            onclick="togglePatientEditForm()">

            Edit Profile

        </button>

        <div
    id="patientEditForm"
    style="display:none;"
    class="mt-4 border-top pt-4">
</div>


    </div>

</div>
`;
  } catch (error) {
    console.log(error);

    alert("Failed to load patient dashboard");
  }
}

function togglePatientEditForm() {
  const form = document.getElementById("patientEditForm");

  if (form.style.display === "none") {
    form.style.display = "block";

    loadPatientEditForm();
  } else {
    form.style.display = "none";
  }
}

async function loadPatientEditForm() {
  try {
    const response = await axios.get(
      "http://127.0.0.1:8001/auth/patient/profile/",
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );

    const patient = response.data;

    document.getElementById("patientEditForm").innerHTML = `

        <h4 class="mb-4">
            Update Patient Profile
        </h4>

        <input
            id="patientPhone"
            class="form-control mb-3"
            value="${patient.phone || ""}"
            placeholder="Phone">

        <input
            id="patientAddress"
            class="form-control mb-3"
            value="${patient.address || ""}"
            placeholder="Address">

        <select
    id="patientGender"
    class="form-control mb-3">

    <option value="male"
    ${patient.gender === "male" ? "selected" : ""}>
    Male
    </option>

    <option value="female"
    ${patient.gender === "female" ? "selected" : ""}>
    Female
    </option>

    <option value="other"
    ${patient.gender === "other" ? "selected" : ""}>
    Other
    </option>

</select>

        <input
            type="date"
            id="patientDob"
            class="form-control mb-3"
            value="${patient.dob || ""}">

        <input
            id="patientBloodGroup"
            class="form-control mb-3"
            value="${patient.blood_group || ""}"
            placeholder="Blood Group">

        <textarea
            id="patientHistory"
            class="form-control mb-3"
            placeholder="Medical History">${patient.medical_history || ""}</textarea>

        <input
            type="file"
            id="patientImage"
            class="form-control mb-3">

        <button
            onclick="updatePatientProfile()"
            class="btn btn-success">

            Update Profile

        </button>
        `;
  } catch (error) {
    console.log(error);
  }
}

async function updatePatientProfile() {
  const formData = new FormData();

  formData.append("phone", document.getElementById("patientPhone").value);

  formData.append("address", document.getElementById("patientAddress").value);

  formData.append("gender", document.getElementById("patientGender").value);

  formData.append("dob", document.getElementById("patientDob").value);

  formData.append(
    "blood_group",
    document.getElementById("patientBloodGroup").value,
  );

  formData.append(
    "medical_history",
    document.getElementById("patientHistory").value,
  );

  const image = document.getElementById("patientImage").files[0];

  if (image) {
    formData.append("profile_image", image);
  }

  try {
    await axios.put(
      "http://127.0.0.1:8001/auth/patient/profile/update/",
      formData,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
      },
    );

    alert("Profile Updated Successfully");

    loadPatientDashboard();

    //  → hide edit form after update
    document.getElementById("patientEditForm").style.display = "none";
  } catch (error) {


    console.log(error);

    console.log("Backend Error:", error.response?.data);

    alert(JSON.stringify(error.response?.data || "Update Failed"));
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
          Authorization: `Bearer ${token}`,
        },
      },
    );

    let html = "";

    response.data.forEach((item) => {
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

    document.getElementById("prescriptionsContainer").innerHTML = html;
  } catch (error) {
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
          Authorization: `Bearer ${token}`,
        },
      },
    );

    let html = "";

    response.data.forEach((item) => {
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

    document.getElementById("testsContainer").innerHTML = html;
  } catch (error) {
    console.log(error);

    alert("Failed to load tests");
  }
}

// =====================================
// UPLOAD REPORT
// =====================================

async function uploadReport() {
  const file = document.getElementById("reportFile").files[0];

  const report_title = document.getElementById("reportTitle").value;

  const testRequestId = document.getElementById("testRequestId").value;

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

          "Content-Type": "multipart/form-data",
        },
      },
    );

    alert("Report Uploaded Successfully");

    loadReports();
  } catch (error) {
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
          Authorization: `Bearer ${token}`,
        },
      },
    );

    let html = "";

    response.data.forEach((report) => {
      let reportUrl = report.report_file;

      if (reportUrl && !reportUrl.startsWith("http")) {
        reportUrl = `http://127.0.0.1:8001${reportUrl}`;
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

    document.getElementById("reportsContainer").innerHTML = html;
  } catch (error) {
    console.log(error);

    alert("Failed to load reports");
  }
}

// =====================================
// LOGOUT
// =====================================

async function logoutUser() {
  const refresh = localStorage.getItem("refresh");

  try {
    await axios.post(
      "http://127.0.0.1:8001/auth/logout/",

      {
        refresh: refresh,
      },

      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );
  } catch (error) {
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
