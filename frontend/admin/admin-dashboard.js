const api = axios.create({
  baseURL: "http://127.0.0.1:8001/auth/",
  headers: {
    Authorization: "Bearer " + localStorage.getItem("access"),
  },
});

// console.log("ACCESS TOKEN:", localStorage.getItem("access"));

async function loadDashboard() {
  try {
    const response = await api.get("admin/dashboard/");

    const data = response.data;

    // console.log("DASHBOARD:", data);

    document.getElementById("totalDoctors").innerText = data.total_doctors || 0;

    document.getElementById("totalPatients").innerText =
      data.total_patients || 0;

    document.getElementById("totalDepartments").innerText =
      data.total_departments || 0;

    document.getElementById("totalPayments").innerText =
      data.total_payments || 0;
  } catch (error) {
    // console.log("Dashboard Error:", error.response?.data || error);
  }
}

function showSection(sectionId) {
  document
    .querySelectorAll(
      "#dashboardSection,#doctorSection,#patientSection,#departmentSection,#appointmentSection,#paymentSection",
    )
    .forEach((section) => {
      section.style.display = "none";
    });

  document.getElementById(sectionId).style.display = "block";
}

function logoutAdmin() {
  localStorage.clear();

  window.location.href = "../login.html";
}

async function loadDoctors() {
  try {
    const response = await api.get("admin/doctors/");

    // console.log("DOCTORS:", response.data);

    const doctors = response.data.doctors;

    let html = "";

    doctors.forEach((doctor) => {
      html += `

            <tr>

                <td>${doctor.user?.name || "-"}</td>

                <td>${doctor.user?.email || "-"}</td>

                <td>${doctor.department || "-"}</td>

                <td>${doctor.specialization}</td>

                <td>

                    ${doctor.is_approved ? "Approved" : "Pending"}

                </td>

                <td>

                ${
                  !doctor.is_approved
                    ? `<button
                        class="btn btn-success btn-sm"
                        onclick="approveDoctor(${doctor.id})">

                        Approve

                    </button>`
                    : ""
                }

                </td>

            </tr>

            `;
    });

    document.getElementById("doctorTable").innerHTML = html;

    document.getElementById("pendingDoctorTable").innerHTML = html;
  } catch (error) {
    // console.log("Doctor Error:", error.response?.data || error);
  }
}

async function approveDoctor(id) {
  try {
    const response = await api.put(`admin/doctors/approve/${id}/`);

    alert(response.data.message);

    loadDoctors();
  } catch (error) {
    // console.log(error.response?.data || error);
  }
}

async function loadPatients() {
  try {
    const response = await api.get("admin/patients/");

    const patients = response.data.patients;

    let html = "";

    patients.forEach((patient) => {
      html += `

            <tr>

               <td>
${patient.user?.first_name || ""}
${patient.user?.last_name || ""}
</td>

                <td>${patient.user?.email || "-"}</td>

                <td>${patient.phone || "-"}</td>

                <td>

                    <button
                        class="btn btn-danger btn-sm">

                        Delete

                    </button>

                </td>

            </tr>

            `;
    });

   

    document.getElementById("patientTable").innerHTML = html;
  } catch (error) {
    // console.log("PATIENT ERROR:", error.response?.data);
  }
}

async function loadDepartments() {
  try {
    const response = await api.get("admin/departments/");

    const departments = response.data.departments;

    let html = "";

    departments.forEach((department) => {
      html += `

            <tr>

                <td>${department.id}</td>

                <td>${department.name}</td>

                <td>

                    <button
                        class="btn btn-primary btn-sm">

                        Edit

                    </button>

                </td>

            </tr>

            `;
    });

   

    document.getElementById("departmentTable").innerHTML = html;
  } catch (error) {
    // console.log("DEPARTMENT ERROR:", error.response?.data);
  }
}

async function loadAppointments() {
  try {
    const response = await api.get("admin/appointments/");

    // console.log("APPOINTMENTS:", response.data);

    const appointments = response.data.appointments;

    let html = "";

    appointments.forEach((appointment) => {
      html += `

            <tr>

                <td>
                    ${appointment.patient_name || "-"}
                </td>

                <td>
                    ${appointment.doctor_name || "-"}
                </td>

                <td>
                    ${appointment.appointment_date || "-"}
                </td>

                <td>
                    ${appointment.status || "-"}
                </td>

            </tr>

            `;
    });

    document.getElementById("appointmentTable").innerHTML = html;
  } catch (error) {
    // console.log("APPOINTMENT ERROR:", error.response?.data || error);
  }
}

async function loadPayments() {
  try {
    const response = await api.get("admin/payments/");
    // console.log("PAYMENTS RESPONSE:",response.data);

    let html = "";

    response.data.payments.forEach((payment) => {
      html += `

        <tr>

          <td>${payment.id}</td>

          <td>
            ${payment.patient_name || payment.patient}
          </td>

          <td>
            ₹ ${payment.amount}
          </td>

          <td>
            <span class="badge bg-success">
              ${payment.payment_status}
            </span>
          </td>

        </tr>

        `;
    });

    document.getElementById("paymentTable").innerHTML = html;
  } catch (error) {
    // console.log("Payment Error:", error.response?.data || error);
  }
}

loadDashboard();

loadDoctors();

loadPatients();

loadDepartments();

loadAppointments();

loadPayments();
