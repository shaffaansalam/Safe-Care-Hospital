document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("registerForm");
  const patientFields = document.getElementById("patientFields");
  const doctorFields = document.getElementById("doctorFields");

  // ✅ ADDING SAFE ELEMENT REFERENCES (ONLY THIS ADDED)
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
  // ✅ END OF ADDED PART

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

    const data = {
      role,
      first_name: firstName.value.trim(),
      last_name: lastName.value.trim(),
      email: email.value.trim(),
      password: password.value.trim(),
      username: `${firstName.value}_${lastName.value}`.toLowerCase(),
    };

    if (role === "patient") {
      if (phone.value.trim()) data.phone = phone.value.trim();
      data.gender = gender.value;
      data.dob = dob.value;
      data.blood_group = bloodGroup.value;
    }

if (role === "doctor") {
  data.specialization = specialization.value.trim();
  data.qualification = qualification.value.trim();
  data.experience = Number(experience.value);
  data.consultation_fee = Number(fee.value);
}

    console.log(" Sending data to backend:", data);

    try {
      console.log("🚀 Sending request...");

      const res = await axios.post(
        "http://127.0.0.1:8001/auth/register/",
        data,
      );

      console.log("✅ Response received");
      console.log(" ✅Full response:", res);
      console.log("Status:", res.status);
      // console.log("Data:", res.data);

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
      console.log("✅ Form reset done");

      console.log("➡ Redirecting NOW");
      window.location.href= "login.html";
      
    } catch (err) {
      // console.error("❌ Registration error:", err);
      console.error("❌ Registration error:", err.response?.data);

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

//   function toggleRoleFields(role) {
//     patientFields.style.display = role === "patient" ? "block" : "none";
//     doctorFields.style.display = role === "doctor" ? "block" : "none";
//   }

//   //  Run once on load (VERY IMPORTANT)
//   toggleRoleFields(
//     document.querySelector('input[name="roleToggle"]:checked').value,
//   );

//   //  Listen for toggle change
//   document.querySelectorAll('input[name="roleToggle"]').forEach((radio) => {
//     radio.addEventListener("change", (e) => {
//       toggleRoleFields(e.target.value);
//     });
//   });

//   // ================= SUBMIT =================
//   form.addEventListener("submit", async (e) => {
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
//     }

//     if (role === "doctor") {
//       data.specialization = specialization.value;
//       data.qualification = qualification.value;
//       data.experience = experience.value;
//       data.consultation_fee = fee.value;
//     }

//     console.log(" Sending data to backend:", data);

// try {
//   console.log("🚀 Sending request...");

//   const res = await axios.post(
//     "http://127.0.0.1:8001/auth/register/",
//     data
//   );

// console.log("Full response:", res);
// console.log("Status:", res.status);
// console.log("Data:", res.data);

//   console.log("✅ Response received");
//   console.log("Full response:", res);

//   const userRole = role.toLowerCase();

//   let successMessage = "";

//   if (userRole === "patient") {
//     successMessage = "Patient registered successfully!";
//   } else if (userRole === "doctor") {
//     successMessage = "Doctor registered successfully!";
//   } else {
//     successMessage = "User registered successfully!";
//   }

//   console.log("🎉", successMessage);

//   form.reset();
//   console.log("✅ Form reset done");

//   console.log("➡ Redirecting NOW");
//   window.location.href = "login.html";

//   return;

// } catch (err) {
//   console.error("❌ Registration error:", err);

//   const msg =
//     err.response?.data?.message ||
//     err.response?.data?.non_field_errors?.[0] ||
//     "Registration failed";

//   alert(msg);
// }

// });
// });

// document.addEventListener("DOMContentLoaded", () => {
//   console.log("✅ Register JS Loaded");

//   const form = document.getElementById("registerForm");

//   if (!form) return;

//   form.addEventListener("submit", async (e) => {
//     e.preventDefault();

//     try {
//       const role = document.querySelector(
//         'input[name="roleToggle"]:checked'
//       ).value;

//       // SAFE FIELD ACCESS
//       const getValue = (id) =>
//         document.getElementById(id)?.value?.trim() || "";

//       const data = {
//         role,
//         first_name: getValue("firstName"),
//         last_name: getValue("lastName"),
//         email: getValue("email"),
//         password: getValue("password"),
//         username: `${getValue("firstName")}_${getValue("lastName")}`.toLowerCase(),
//       };

//       if (role === "patient") {
//         data.phone = getValue("phone");
//         data.gender = getValue("gender");
//         data.dob = getValue("dob");
//         data.blood_group = getValue("bloodGroup");
//       }

//       if (role === "doctor") {
//         data.specialization = getValue("specialization");
//         data.qualification = getValue("qualification");
//         data.experience = getValue("experience");
//         data.consultation_fee = getValue("fee");
//       }

//       console.log("📤 Sending data:", data);

//       const res = await axios.post(
//         "http://127.0.0.1:8001/auth/register/",
//         data
//       );

//       console.log("✅ Registration success:", res.data);

//       form.reset();

//       console.log("➡ Redirecting to login page...");
//       window.location.href = "login.html";
//       return;

//     } catch (err) {
//       console.error("❌ Registration failed:", err);

//       if (err.response) {
//         console.error("Server message:", err.response.data);
//       }
//     }
//   });
// });
