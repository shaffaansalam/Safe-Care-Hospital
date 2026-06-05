document.addEventListener("DOMContentLoaded", () => {

    // LOGIN / LOGOUT

    const token = localStorage.getItem("access_token");

    const loginNav = document.getElementById("loginNav");

    const logoutNav = document.getElementById("logoutNav");

    if (loginNav && logoutNav) {

        if (token && token !== "undefined" && token !== "null") {

            loginNav.style.display = "none";

            logoutNav.style.display = "block";

        } else {

            loginNav.style.display = "block";

            logoutNav.style.display = "none";
        }
    }

    // MOBILE MENU

    const menuToggle = document.getElementById("menuToggle");

    const mobileNav = document.getElementById("mobileNav");

    if (menuToggle && mobileNav) {

        menuToggle.addEventListener("click", () => {

            mobileNav.classList.toggle("active");

        });
    }

});


// LOGOUT FUNCTION

function logoutUser() {

    localStorage.clear();

    

    window.location.reload();
}