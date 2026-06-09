

const appointmentId = localStorage.getItem("appointment_id");
console.log(localStorage.getItem("appointment_id"));

async function loadPayment() {
  const response = await axios.post(
    "http://127.0.0.1:8001/auth/payments/create-order/",

    {
      appointment_id: appointmentId,
    },

    {
      headers: {
        Authorization: "Bearer " + localStorage.getItem("access"),
      },
    },
  );

  const data = response.data;

  document.getElementById("patientName").innerText = data.patient;

  document.getElementById("doctorName").innerText = data.doctor;

  document.getElementById("department").innerText = data.department;

  document.getElementById("appointmentDate").innerText = data.date;

  document.getElementById("appointmentTime").innerText = data.time;

  document.getElementById("amount").innerText = "₹ " + data.amount / 100;

  document.getElementById("payBtn").onclick = function () {
    const options = {
      key: data.key,

      amount: data.amount,

      currency: "INR",

      order_id: data.order_id,

      name: "SafeCare HMS",

      handler: async function (response) {
        await axios.post(
          "http://127.0.0.1:8001/auth/payments/verify/",

          {
            appointment_id: appointmentId,

            razorpay_order_id: response.razorpay_order_id,

            razorpay_payment_id: response.razorpay_payment_id,
          },

          {
            headers: {
              Authorization: "Bearer " + localStorage.getItem("access"),
            },
          },
        );

        alert("Payment Successful");
        window.location.href = "patient-dashboard.html";
      },
    };

    const rzp = new Razorpay(options);

    rzp.open();
  };
}

loadPayment();
