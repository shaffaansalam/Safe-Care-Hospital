document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("registerForm");
  const patientFields = document.getElementById("patientFields");
  const doctorFields = document.getElementById("doctorFields");

  // SAFE ELEMENT REFERENCES
  const firstName = document.getElementById("firstName");
  const lastName = document.getElementById("lastName");
  const email = document.getElementById("email");
  const password = document.getElementById("password");

  const phone = document.getElementById("phone");
  const gender = document.getElementById("gender");
  const dob = document.getElementById("dob");
  const bloodGroup = document.getElementById("bloodGroup");
  const medical_history = document.getElementById("medical_history");
  const profile_image = document.getElementById("profile_image");

  const specialization = document.getElementById("specialization");
  const qualification = document.getElementById("qualification");
  const experience = document.getElementById("experience");
  const fee = document.getElementById("fee");

  const doctorPhone = document.getElementById("doctorPhone");
  const bio = document.getElementById("bio");
  const availableStart = document.getElementById("availableStart");
  const availableEnd = document.getElementById("availableEnd");

  function toggleRoleFields(role) {
    patientFields.style.display = role === "patient" ? "block" : "none";
    doctorFields.style.display = role === "doctor" ? "block" : "none";
  }

  toggleRoleFields(
    document.querySelector('input[name="roleToggle"]:checked').value,
  );

  document.querySelectorAll('input[name="roleToggle"]').forEach((radio) => {
    radio.addEventListener("change", (e) => {
      toggleRoleFields(e.target.value);
    });
  });

  // ================= SUBMIT =================
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const role = document.querySelector(
      'input[name="roleToggle"]:checked',
    ).value;

    const data = new FormData();

    data.append("role", role);

    data.append("first_name", firstName.value.trim());

    data.append("last_name", lastName.value.trim());

    data.append("email", email.value.trim());

    data.append("password", password.value.trim());

    data.append(
      "username",
      `${firstName.value}_${lastName.value}`.toLowerCase(),
    );

    if (role === "patient") {
      if (phone.value.trim()) {
        data.append("phone", phone.value.trim());
      }

      data.append("gender", gender.value);

      data.append("dob", dob.value);

      data.append("blood_group", bloodGroup.value);

      data.append("address", document.getElementById("address").value);

      data.append("medical_history", medical_history.value.trim());

      if (profile_image.files.length > 0) {
        data.append("profile_image", profile_image.files[0]);
      }
    }

    // DOCTOR DATA
    if (role === "doctor") {
      data.append("specialization", specialization.value.trim());

      data.append("qualification", qualification.value.trim());

      data.append("experience", parseInt(experience.value) || 0);

      data.append("consultation_fee", parseFloat(fee.value) || 0);

      data.append("phone", doctorPhone.value.trim());

      data.append("bio", bio.value.trim());

      data.append("available_start_time", availableStart.value + ":00");

      data.append("available_end_time", availableEnd.value + ":00");

      if (profile_image.files.length > 0) {
        data.append("profile_image", profile_image.files[0]);
      }
    }

    for (let pair of data.entries()) {
      console.log(pair[0], pair[1]);
    }

    try {
      console.log("🚀 Sending request...");

      const res = await axios.post(
        "http://127.0.0.1:8001/auth/register/",
        data,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        },
      );

      console.log("Full response:", res);
      console.log("Status:", res.status);

      const userRole = role.toLowerCase();

      let successMessage = "";

      if (userRole === "patient") {
        successMessage = "Patient registered successfully!";
      } else if (userRole === "doctor") {
        successMessage = "Doctor registered successfully!";
      } else {
        successMessage = "User registered successfully!";
      }

      console.log("🎉", successMessage);

      form.reset();

      console.log("Redirecting to login.html...");

      window.location.href = "login.html";
    } catch (err) {
      console.error("Registration error:", err.response?.data);

      const msg =
        err.response?.data?.message ||
        err.response?.data?.non_field_errors?.[0] ||
        "Registration failed";

      alert(msg);
    }
  });
});
