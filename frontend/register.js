document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("registerForm");
  const patientFields = document.getElementById("patientFields");
  const doctorFields = document.getElementById("doctorFields");

  function toggleRoleFields(role) {
    patientFields.style.display = role === "patient" ? "block" : "none";
    doctorFields.style.display = role === "doctor" ? "block" : "none";
  }

  //  Run once on load (VERY IMPORTANT)
  toggleRoleFields(
    document.querySelector('input[name="roleToggle"]:checked').value
  );

  //  Listen for toggle change
  document.querySelectorAll('input[name="roleToggle"]').forEach(radio => {
    radio.addEventListener("change", e => {
      toggleRoleFields(e.target.value);
    });
  });

  // ================= SUBMIT =================
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

     

    const role = document.querySelector(
      'input[name="roleToggle"]:checked'
    ).value;

    const data = {
      role,
      first_name: firstName.value.trim(),
      last_name: lastName.value.trim(),
      email: email.value.trim(),
      password: password.value.trim(),
      username: `${firstName.value}_${lastName.value}`.toLowerCase(),
    };

    if (role === "patient") {
      data.phone = phone.value;
      data.gender = gender.value;
      data.dob = dob.value;
      data.blood_group = bloodGroup.value;
    }

    if (role === "doctor") {
      data.specialization = specialization.value;
      data.qualification = qualification.value;
      data.experience = experience.value;
      data.consultation_fee = fee.value;
    }

        console.log(" Sending data to backend:", data);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8001/auth/register/",
        data
      );

    //   console.log("Backend response:", response.data);
      alert(res.data.message);
      form.reset();
      
      window.location.href = "login.html";

                  
    //    console.log(" Backend response:", response.data);
    //   alert(response.data.message);              

    } catch (err) {
  const msg =
    err.response?.data?.message ||
    err.response?.data?.non_field_errors?.[0] ||
    "Registration failed";

  alert(msg);
}
  });
});
