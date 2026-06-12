document.addEventListener("DOMContentLoaded", () => {
  const notificationNav = document.getElementById("notificationNav");

  if (!notificationNav) return;

  notificationNav.style.display = "block";

  loadNotifications();
});

async function loadNotifications() {
  try {
    const response = await axios.get(
      "http://127.0.0.1:8001/auth/patient/notifications/",

      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access")}`,
        },
      },
    );

    const notifications = response.data;

    console.log("Notifications:", notifications);

    document.getElementById("notificationCount").innerText =
      notifications.length;

    let html = "";

    if (notifications.length === 0) {
      html = `

    <div class="notification-item">

        <strong>
        No Notifications
        </strong>

    </div>

    `;
    } else {
      notifications.forEach((item) => {
        html += `

        <div class="notification-item">

            <strong>${item.title}</strong>

            <p>${item.message}</p>

        </div>

        `;
      });
    }

    document.getElementById("notificationList").innerHTML = html;
  } catch (error) {
    console.log(error);
  }
}

document.addEventListener("click", (e) => {
  const bell = document.getElementById("notificationBell");

  const dropdown = document.getElementById("notificationDropdown");

  if (!bell || !dropdown) return;

  if (bell.contains(e.target)) {
    e.preventDefault();

    dropdown.classList.toggle("show");
  } else {
    dropdown.classList.remove("show");
  }
});
