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
    document.querySelector('input[name="roleToggle"]:checked').value
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

    // PATIENT DATA
    if (role === "patient") {
      if (phone.value.trim()) data.phone = phone.value.trim();
      data.gender = gender.value;
      data.dob = dob.value;
      data.blood_group = bloodGroup.value;
      data.address = document.getElementById("address").value;
    }

    // DOCTOR DATA
    if (role === "doctor") {
      data.specialization = specialization.value.trim();
      data.qualification = qualification.value.trim();
      data.experience = parseInt(experience.value) || 0;
      data.consultation_fee = parseFloat(fee.value) || 0;

      if (doctorPhone.value.trim()) {
        data.phone = doctorPhone.value.trim();
      }

      if (bio.value.trim()) {
        data.bio = bio.value.trim();
      }

      if (availableStart.value) {
        data.available_start_time = `${availableStart.value}:00`;
      }

      if (availableEnd.value) {
        data.available_end_time = `${availableEnd.value}:00`;
      }
    }

    console.log("Sending data:", JSON.stringify(data, null, 2));
    // console.log("Sending data to backend:", data);

    try {
      console.log("🚀 Sending request...");

      const res = await axios.post(
        "http://127.0.0.1:8001/auth/register/",
        data
      );

      // console.log("✅ Response received");
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
      // console.log("Form reset done");

      // console.log("Current page:", window.location.href);
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










// document.addEventListener("DOMContentLoaded", () => {
//   const form = document.getElementById("registerForm");
//   const patientFields = document.getElementById("patientFields");
//   const doctorFields = document.getElementById("doctorFields");

//   // ✅ ADDING SAFE ELEMENT REFERENCES (ONLY THIS ADDED)
//   const firstName = document.getElementById("firstName");
//   const lastName = document.getElementById("lastName");
//   const email = document.getElementById("email");
//   const password = document.getElementById("password");

//   const phone = document.getElementById("phone");
//   const gender = document.getElementById("gender");
//   const dob = document.getElementById("dob");
//   const bloodGroup = document.getElementById("bloodGroup");
//   // const address = document.getElementById("address");

//   const specialization = document.getElementById("specialization");
//   const qualification = document.getElementById("qualification");
//   const experience = document.getElementById("experience");
//   const fee = document.getElementById("fee");

//   const doctorPhone = document.getElementById("doctorPhone");
//   const bio = document.getElementById("bio");
//   const availableStart = document.getElementById("availableStart");
//   const availableEnd = document.getElementById("availableEnd");


//   // ✅ END OF ADDED PART

//   function toggleRoleFields(role) {
//     patientFields.style.display = role === "patient" ? "block" : "none";
//     doctorFields.style.display = role === "doctor" ? "block" : "none";
//   }

//   toggleRoleFields(
//     document.querySelector('input[name="roleToggle"]:checked').value,
//   );

//   document.querySelectorAll('input[name="roleToggle"]').forEach((radio) => {
//     radio.addEventListener("change", (e) => {
//       toggleRoleFields(e.target.value);
//     });
//   });

//   // ================= SUBMIT =================
//   form.addEventListener("submit", async (e) => {
//     // document.getElementById("registerBtn").addEventListener("click", async (e) => {
//     e.preventDefault();

//     const role = document.querySelector(
//       'input[name="roleToggle"]:checked',
//     ).value;

//     const data = {
//       role,
//       first_name: firstName.value.trim(),
//       last_name: lastName.value.trim(),
//       email: email.value.trim(),
//       password: password.value.trim(),
//       username: `${firstName.value}_${lastName.value}`.toLowerCase(),
//     };

//     if (role === "patient") {
//       if (phone.value.trim()) data.phone = phone.value.trim();
//       data.gender = gender.value;
//       data.dob = dob.value;
//       data.blood_group = bloodGroup.value;
//       // data.address = address.value.trim();
//       data.address = document.getElementById("address").value;
//     }

//     // if (role === "doctor") {
//     //   data.specialization = specialization.value.trim();
//     //   data.qualification = qualification.value.trim();
//     //   data.experience = Number(experience.value);
//     //   data.consultation_fee = Number(fee.value);
//     //     data.doctorPhone = document.getElementById("doctorPhone").value.trim();
//     //     data.bio = document.getElementById("bio").value.trim();
//     //     data.availableStart = document.getElementById("availableStart").value;
//     //     data.availableEnd = document.getElementById("availableEnd").value;

//     //     data.available_start_time = availableStart.value ? `${availableStart.value}:00` : null;
//     //     data.available_end_time = availableEnd.value ? `${availableEnd.value}:00` : null;


//       if (role === "doctor") {
//   data.specialization = specialization.value.trim();
//   data.qualification = qualification.value.trim();
//   data.experience = parseInt(experience.value) || 0;
//   data.consultation_fee = parseFloat(fee.value) || 0;

//   const doctorPhone = document.getElementById("doctorPhone").value.trim();
//   const bio = document.getElementById("bio").value.trim();
//   const start = document.getElementById("availableStart").value;
//   const end = document.getElementById("availableEnd").value;

//   if (doctorPhone) data.phone = doctorPhone;
//   if (bio) data.bio = bio;

//   if (start) data.available_start_time = `${start}:00`;
//   if (end) data.available_end_time = `${end}:00`;


//     console.log("Sending data:", JSON.stringify(data, null, 2));
//     console.log(" Sending data to backend:", data);

//     try {
//       console.log("🚀 Sending request...");

//       const res = await axios.post(
//         "http://127.0.0.1:8001/auth/register/",
//         data,
//       );

//       console.log("✅ Response received");
//       console.log(" ✅Full response:", res);
//       console.log("Status:", res.status);
//       // console.log("Data:", res.data);

//       const userRole = role.toLowerCase();

//       let successMessage = "";

//       if (userRole === "patient") {
//         successMessage = "Patient registered successfully!";
//       } else if (userRole === "doctor") {
//         successMessage = "Doctor registered successfully!";
//       } else {
//         successMessage = "User registered successfully!";
//       }

//       console.log("🎉", successMessage);

//       form.reset();
//       console.log("✅ Form reset done");

//       console.log("Current page:", window.location.href);
//       console.log("Redirecting to login.html...");

    
//         window.location.href = "login.html";
     

//     } catch (err) {
  
//       console.error("❌ Registration error:", err.response?.data);

//       const msg =
//         err.response?.data?.message ||
//         err.response?.data?.non_field_errors?.[0] ||
//         "Registration failed";

//       alert(msg);
//     }
//   });
// });
