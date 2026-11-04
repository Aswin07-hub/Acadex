
// ======================================
// 1. Show / Hide Password
// ======================================

const toggleButtons = document.querySelectorAll(".toggle-password");

toggleButtons.forEach(function(button) {

    button.addEventListener("click", function() {

        const targetId = button.dataset.target;
        const passwordInput = document.getElementById(targetId);

        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            button.textContent = "Hide";
        } else {
            passwordInput.type = "password";
            button.textContent = "Show";
        }

    });

});


// ======================================
// 2. Registration Form Validation
// ======================================

const registerForm = document.getElementById("registerForm");
const formMessage = document.getElementById("formMessage");

registerForm.addEventListener("submit", function(event) {

    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm_password").value;
    const phone = document.getElementById("phone").value.trim();

    formMessage.textContent = "";

    if (password.length < 8) {

        event.preventDefault();

        formMessage.textContent =
            "Password must contain at least 8 characters.";

        return;
    }

    if (password !== confirmPassword) {

        event.preventDefault();

        formMessage.textContent =
            "Password and confirm password do not match.";

        return;
    }

    if (!/^[0-9]{10,15}$/.test(phone)) {

        event.preventDefault();

        formMessage.textContent =
            "Please enter a valid phone number.";

        return;
    }

});
