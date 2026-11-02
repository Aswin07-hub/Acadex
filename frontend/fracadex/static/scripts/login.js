
// ======================================
// 1. Show and Hide Password
// ======================================

const passwordInput = document.getElementById("password");

const togglePassword = document.getElementById("togglePassword");

togglePassword.addEventListener("click", function () {

    if (passwordInput.type === "password") {

        passwordInput.type = "text";

        togglePassword.textContent = "Hide";

        togglePassword.setAttribute(
            "aria-label",
            "Hide password"
        );

    } else {

        passwordInput.type = "password";

        togglePassword.textContent = "Show";

        togglePassword.setAttribute(
            "aria-label",
            "Show password"
        );

    }

});


// ======================================
// 2. Login Form Validation
// ======================================

const loginForm = document.getElementById("loginForm");

const message = document.getElementById("message");

loginForm.addEventListener("submit", function (event) {

    const role = document.getElementById("role").value;

    const username = document.getElementById("username").value.trim();

    const password = passwordInput.value;

    if (
        role === "" ||
        username === "" ||
        password === ""
    ) {

        event.preventDefault();

        message.textContent = "Please fill in all fields.";

        message.style.color = "red";

    }

});


// ======================================
// 3. Login Submission
// ======================================

// The browser submits the form using POST.
// Frontend Django views.py receives the request.
// Python requests performs GET and POST
// communication with the backend API.
